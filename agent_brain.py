import os
import time
import hashlib
import traceback
import re
import requests
import logging
from typing import Optional, Dict
from dotenv import load_dotenv
from notion_client import Client
from duckduckgo_search import DDGS

from agent_notion import (
    NOTION_TOKEN,
    NOTION_DATABASE_ID,
    validate_env,
    extract_plain_rich_text,
    NotionAgent,
)
from backup_data import backup_notion_data

load_dotenv()

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Configure Logging
class TelegramHandler(logging.Handler):
    """Custom Logging Handler that sends critical logs to Telegram."""
    def emit(self, record):
        if record.levelno >= logging.ERROR:
            try:
                msg = self.format(record)
                send_telegram_message(f"🚨 <b>System Error</b>\n<pre>{msg}</pre>")
            except Exception:
                self.handleError(record)

# Setup Logger
logger = logging.getLogger("NotionAgent")
logger.setLevel(logging.INFO)

# Console Handler
c_handler = logging.StreamHandler()
c_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(c_handler)

# Telegram Handler
if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
    t_handler = TelegramHandler()
    t_handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(t_handler)

def send_telegram_message(message: str) -> None:
    """Send a message to Telegram."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.warning("Telegram configuration missing. Skipping notification.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code != 200:
            logger.error(f"Telegram send failed: {resp.text}")
    except Exception as e:
        logger.error(f"Telegram connection error: {e}")

def md5_of_text(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def search_for_alternative_url(title: str, original_url: str) -> Optional[str]:
    """
    Search for a new URL if the original one is broken.
    Uses title + 'Github' or 'Cursor Rules' as query.
    """
    query = f"{title} Github Cursor Rules"
    logger.info(f"🔎 尝试自动修复链接，搜索关键词: {query}")
    
    try:
        results = DDGS().text(query, max_results=3)
        if not results:
            return None
            
        original_domain = original_url.split('/')[2] if '//' in original_url else ""
        
        for res in results:
            href = res.get('href')
            if not href:
                continue
                
            # Smart Matching Logic
            # 1. Same domain match (likely rename/move)
            if original_domain and original_domain in href:
                logger.info(f"✨ 发现同域名新链接: {href}")
                return href
                
            # 2. Trusted Source Match (GitHub/Official)
            if "github.com" in href:
                logger.info(f"✨ 发现可信源(GitHub): {href}")
                return href
                
    except Exception as e:
        logger.error(f"Search failed: {e}")
        
    return None

def fetch_remote_text(url: str, timeout: int = 15) -> Optional[str]:
    max_retries = 3
    for attempt in range(max_retries):
        try:
            logger.info(f"获取远程内容: {url} (Attempt {attempt+1}/{max_retries})")
            resp = requests.get(url, timeout=timeout)
            if resp.status_code == 200:
                text = resp.text
                if not text:
                    logger.error(f"远程内容为空: {url}")
                    return None
                return text
            elif resp.status_code == 404:
                logger.warning(f"404 Not Found: {url}")
                return None
            else:
                logger.error(f"请求失败 {resp.status_code}: {url}")
        except Exception as e:
            logger.error(f"请求异常 {url}: {e}")
        
        if attempt < max_retries - 1:
            time.sleep(2)
            
    return None

def sync_existing_sources(notion_client: Client, agent: NotionAgent) -> Dict[str, int]:
    logger.info("开始存量更新：基于 Source 链接巡检")
    start_cursor: Optional[str] = None
    stats = {"created": 0, "updated": 0, "skipped": 0, "error": 0}

    while True:
        # Use direct requests to avoid library version issues
        url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
        headers = {
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        
        payload = {"page_size": 100}
        if start_cursor:
            payload["start_cursor"] = start_cursor

        try:
            r = requests.post(url, json=payload, headers=headers, timeout=30)
            if r.status_code != 200:
                logger.error(f"Notion API Error: {r.text}")
                break
            resp = r.json()
        except Exception as e:
            logger.error(f"Notion Request Failed: {e}")
            break

        results = resp.get("results", [])
        if not results:
            break

        for page in results:
            props = page.get("properties", {})
            
            # Extract Title
            name_prop = props.get("Name") or {}
            title_items = name_prop.get("title", [])
            if not title_items:
                continue
            title = title_items[0].get("plain_text") or title_items[0].get("text", {}).get("content", "")
            if not title:
                continue

            # Extract Source URL
            source_prop = props.get("Source")
            source_url = None
            if source_prop and source_prop.get("type") == "url":
                source_url = source_prop.get("url")

            # Extract Tag
            type_prop = props.get("Type")
            tag_name: Optional[str] = None
            if type_prop and type_prop.get("type") == "select":
                sel = type_prop.get("select")
                if sel:
                    tag_name = sel.get("name")
            if tag_name not in ["Skill", "MCP"]:
                tag_name = "Skill"

            # Extract Current Status
            status_prop = props.get("Status")
            current_status = "Active"
            if status_prop:
                current_status = status_prop.get("status", {}).get("name") or "Active"

            # Extract Local Content
            content_prop = props.get("Content") or {}
            local_text = extract_plain_rich_text(content_prop)

            # 1. Self-managed / AI Created (No Source)
            if not source_url:
                if current_status != "Active":
                    logger.info(f"自建内容状态修复: {title} -> Active")
                    res = agent.save_to_notion(
                        title=title, content=local_text, tag=tag_name, url=None, status="Active"
                    )
                    stats[res] = stats.get(res, 0) + 1
                else:
                    # No source, already active, skip
                    pass
                continue

            # 2. Remote Fetch with Retry
            remote_text = fetch_remote_text(source_url)

            # 3. Dead Link / Fetch Failure
            if remote_text is None:
                # Try Self-Healing
                logger.warning(f"⚠️  链接失效，尝试自愈: {title}")
                new_url = search_for_alternative_url(title, source_url)
                
                if new_url:
                    # Healing Success
                    logger.info(f"🚑 自愈成功: {source_url} -> {new_url}")
                    remote_text_healed = fetch_remote_text(new_url)
                    
                    if remote_text_healed:
                        content_healed = f"自动同步自 Source：{new_url}\n\n{remote_text_healed}"
                        res = agent.save_to_notion(
                            title=title, content=content_healed, tag=tag_name, url=new_url, status="Active"
                        )
                        stats[res] = stats.get(res, 0) + 1
                        
                        send_telegram_message(
                            f"🔗 <b>已自动修复死链</b>\n"
                            f"📝 <b>{title}</b>\n"
                            f"❌ 原: {source_url}\n"
                            f"✅ 新: {new_url}"
                        )
                        continue
                
                # Healing Failed
                if current_status != "Broken":
                    logger.error(f"❌ 死链自愈失败: {source_url} -> 标记为 Broken")
                    # Update status to Broken
                    res = agent.save_to_notion(
                        title=title, content=local_text, tag=tag_name, url=source_url, status="Broken"
                    )
                    stats[res] = stats.get(res, 0) + 1
                else:
                    logger.info(f"❌ 死链保持 Broken: {title}")
                    stats["skipped"] += 1
                continue

            # 4. Success - Update Content & Restore Status
            if current_status != "Active":
                logger.info(f"✅ 链接恢复: {title} -> 恢复 Active")
                # Will be updated in save_to_notion call below

            local_md5 = md5_of_text(local_text)
            remote_md5 = md5_of_text(remote_text)

            if local_md5 == remote_md5 and current_status == "Active":
                logger.info(f"⏭️  [MD5 Match] 跳过更新: {title}")
                stats["skipped"] += 1
                continue

            new_content = f"自动同步自 Source：{source_url}\n\n{remote_text}"
            logger.info(f"检测到上游变更或状态修复: {title}")

            res = agent.save_to_notion(
                title=title,
                content=new_content,
                tag=tag_name,
                url=source_url,
                status="Active",
            )
            stats[res] = stats.get(res, 0) + 1

        if not resp.get("has_more"):
            break

        start_cursor = resp.get("next_cursor")

    logger.info("存量更新完成")
    return stats

def discover_new_rules(agent: NotionAgent) -> Dict[str, int]:
    logger.info("开始增量发现：Stripe & Automation 规则")
    stats = {"created": 0, "updated": 0, "skipped": 0, "error": 0}
    
    keywords = ["stripe", "automation"]
    base = "https://cursor.directory"
    seen_titles = set()

    for kw in keywords:
        search_url = f"https://cursor.directory/search?q={kw}"
        logger.info(f"正在搜索 cursor.directory: {kw}")
        html = fetch_remote_text(search_url)
        if not html:
            continue

        # Regex to find rule links. 
        # Adapting to potential structure: <a href="/rules/foo-bar"> ... <h3>Foo Bar</h3> ... </a>
        # This is a best-effort regex based on common patterns.
        pattern = re.compile(r'href=\"(/rules/[^\"]+)\"', re.IGNORECASE)
        matches = pattern.findall(html)
        
        if not matches:
            logger.info(f"未找到关于 {kw} 的规则")
            continue

        for path in matches:
            # Deduplicate by URL path
            if path in seen_titles:
                continue
            seen_titles.add(path)

            # Derive title from path
            # /rules/stripe-api-best-practices -> Stripe Api Best Practices
            title = path.replace("/rules/", "").replace("-", " ").title()
            
            rule_url = base + path
            remote_text = fetch_remote_text(rule_url)
            if not remote_text:
                continue

            content = (
                f"中文功能简介：自动发现的 {kw} 规则 [{title}]，"
                f"用于增强 Agent 在该领域的自动化能力。\n\n"
                f"Original Content ({rule_url}):\n\n"
                f"{remote_text}"
            )

            logger.info(f"增量发现：尝试入库新规则: {title}")
            res = agent.save_to_notion(
                title=title,
                content=content,
                tag="Skill",
                url=rule_url,
                status="Active",
            )
            stats[res] = stats.get(res, 0) + 1
            
            # Be polite to the server
            time.sleep(1)

    logger.info("增量发现流程完成")
    return stats

def run_once() -> None:
    validate_env()
    agent = NotionAgent()
    client = Client(auth=NOTION_TOKEN)

    logger.info("开始本轮巡检：存量更新 + 增量发现")
    
    # Run tasks and aggregate stats
    s1 = sync_existing_sources(client, agent)
    s2 = discover_new_rules(agent)
    
    total_created = s1["created"] + s2["created"]
    total_updated = s1["updated"] + s2["updated"]
    total_skipped = s1["skipped"] + s2["skipped"]
    
    report_msg = (
        f"✅ 新增: {total_created} | 🔄 更新: {total_updated} | ⏭️ 跳过: {total_skipped}"
    )
    logger.info(report_msg)
    
    # Run Backup (Once per cycle, effectively daily in current loop)
    try:
        logger.info("开始执行每日数据冷备份...")
        backup_notion_data(client, NOTION_DATABASE_ID)
    except Exception as e:
        logger.error(f"Backup failed: {e}")
        send_telegram_message(f"⚠️ <b>备份失败</b>\n{str(e)}")
    
    # Send Telegram Report
    send_telegram_message(f"<b>巡检报告</b>\n{report_msg}")

def main() -> None:
    validate_env()
    logger.info("Agent Brain initialized (7x24h auto-inspection mode)")
    
    while True:
        start = time.time()
        try:
            run_once()
        except KeyboardInterrupt:
            logger.info("收到中断信号，退出巡检")
            break
        except Exception as e:
            error_msg = f"脚本巡检报错: {str(e)}"
            logger.error(error_msg)
            traceback.print_exc()
            send_telegram_message(f"🚨 <b>紧急预警</b>\n{error_msg}")

        elapsed = time.time() - start
        sleep_seconds = max(0, 24 * 60 * 60 - int(elapsed))
        logger.info(f"下次巡检将在 {sleep_seconds} 秒后执行")
        time.sleep(sleep_seconds)

if __name__ == "__main__":
    main()
