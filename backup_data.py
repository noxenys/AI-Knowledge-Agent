import os
import json
import datetime
import pprint
from notion_client import Client
from typing import List, Dict, Any
from agent_notion import extract_plain_rich_text, print_info, print_success, print_error
import time

import requests

def fetch_all_pages(client: Client, database_id: str) -> List[Dict[str, Any]]:
    """Fetch all pages from the Notion database using pagination via direct HTTP requests."""
    all_results = []
    start_cursor = None
    
    token = os.getenv("NOTION_TOKEN")
    if not token:
        print_error("NOTION_TOKEN missing for backup fetch.")
        return []

    print_info("开始全量备份：拉取 Notion 数据 (via requests)...")
    
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    while True:
        try:
            payload = {
                "page_size": 100,
                "sorts": [{"timestamp": "last_edited_time", "direction": "descending"}]
            }
            if start_cursor:
                payload["start_cursor"] = start_cursor
            
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if resp.status_code != 200:
                print_error(f"Backup fetch failed: {resp.status_code} - {resp.text}")
                break
                
            data = resp.json()
            results = data.get("results", [])
            print_info(f"已拉取 {len(results)} 条数据...")
            all_results.extend(results)
            
            if not data.get("has_more"):
                break
                
            start_cursor = data.get("next_cursor")
            time.sleep(0.5) # Rate limit friendly
            
        except Exception as e:
            print_error(f"Backup fetch exception: {e}")
            break
            
    print_info(f"拉取完成，共 {len(all_results)} 条数据")
    return all_results

def parse_page(page: Dict[str, Any]) -> Dict[str, Any]:
    """Extract structured data from a raw Notion page object."""
    props = page.get("properties", {})
    
    # 1. Name (Title)
    name_prop = props.get("Name") or {}
    title_items = name_prop.get("title", [])
    title = ""
    if title_items:
        title = title_items[0].get("plain_text") or title_items[0].get("text", {}).get("content", "")
        
    # 2. Type (Select)
    type_prop = props.get("Type") or {}
    tag_name = "Unknown"
    if type_prop.get("type") == "select":
        sel = type_prop.get("select")
        if sel:
            tag_name = sel.get("name")
            
    # 3. Status (Status)
    status_prop = props.get("Status") or {}
    status_name = "Unknown"
    if status_prop.get("type") == "status":
        status_name = status_prop.get("status", {}).get("name")
        
    # 4. Source (URL)
    source_prop = props.get("Source") or {}
    source_url = None
    if source_prop.get("type") == "url":
        source_url = source_prop.get("url")
        
    # 5. Content (Rich Text)
    content_prop = props.get("Content") or {}
    content_text = extract_plain_rich_text(content_prop)
    
    # 6. Last Edited Time
    last_edited = page.get("last_edited_time")
    
    return {
        "Name": title,
        "Type": tag_name,
        "Status": status_name,
        "Source": source_url,
        "Content": content_text,
        "Last Edited Time": last_edited,
        "Notion ID": page.get("id"),
        "URL": page.get("url")
    }

def generate_markdown(data: List[Dict[str, Any]]) -> str:
    """Generate a readable Markdown summary."""
    lines = ["# Notion Database Backup", f"\nBackup Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"]
    
    for item in data:
        lines.append(f"## {item['Name']}")
        lines.append(f"- **Type**: {item['Type']}")
        lines.append(f"- **Status**: {item['Status']}")
        lines.append(f"- **Source**: {item['Source']}")
        lines.append(f"- **Last Edited**: {item['Last Edited Time']}")
        lines.append(f"\n**Content**:\n")
        lines.append(f"```\n{item['Content']}\n```")
        lines.append("\n---\n")
        
    return "\n".join(lines)

def generate_seed_script(data: List[Dict[str, Any]]) -> str:
    """Generate a standalone Python script to re-seed the database."""
    # Convert data to the format expected by agent_notion.py's save_to_notion
    # agent_notion.save_to_notion(title, content, tag, url, status)
    
    seed_list = []
    for item in data:
        seed_list.append({
            "title": item["Name"],
            "content": item["Content"],
            "tag": item["Type"],
            "url": item["Source"],
            "status": item["Status"]
        })
    
    # Use pprint to ensure valid Python syntax (None instead of null, True instead of true)
    seed_data_str = pprint.pformat(seed_list, indent=4, width=120, sort_dicts=False)
    
    script_content = f'''
import os
import sys
import json
from typing import List, Dict, Any

# Ensure we can find the agent modules if running from project root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from agent_notion import NotionAgent, NOTION_TOKEN, NOTION_DATABASE_ID
except ImportError:
    print("❌ 错误: 找不到 agent_notion.py 模块。请确保此脚本在项目根目录下运行。")
    sys.exit(1)

# DATA SEED GENERATED AT: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# TOTAL ITEMS: {len(seed_list)}

SEED_DATA: List[Dict[str, Any]] = {seed_data_str}

def run_seed():
    print(f"🌱 开始播种数据，共 {{len(SEED_DATA)}} 条...")
    if not NOTION_TOKEN or not NOTION_DATABASE_ID:
        print("❌ 错误: 环境变量 NOTION_TOKEN 或 NOTION_DATABASE_ID 未设置")
        return
        
    # NotionAgent initializes from env vars automatically
    agent = NotionAgent()
    
    success_count = 0
    skip_count = 0
    
    for item in SEED_DATA:
        try:
            print(f"Processing: {{item['title']}}")
            # Using save_to_notion which handles upsert (check existence by title)
            result = agent.save_to_notion(
                title=item['title'],
                content=item['content'],
                tag=item['tag'],
                url=item['url'],
                status=item['status']
            )
            
            if result == "created":
                print(f"✅ Created: {{item['title']}}")
                success_count += 1
            elif result == "updated":
                print(f"🔄 Updated: {{item['title']}}")
                success_count += 1
            else:
                print(f"⏭️ Skipped: {{item['title']}}")
                skip_count += 1
                
        except Exception as e:
            print(f"❌ Error processing {{item['title']}}: {{e}}")
            
    print(f"\\n🎉 播种完成! 成功/更新: {{success_count}}, 跳过: {{skip_count}}")

if __name__ == "__main__":
    run_seed()
'''
    return script_content.strip()

def backup_notion_data(client: Client, database_id: str, backup_dir: str = "backups") -> None:
    """Main backup function."""
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    
    # Fetch and Parse
    raw_pages = fetch_all_pages(client, database_id)
    parsed_data = [parse_page(p) for p in raw_pages]
    
    # Save JSON
    json_filename = f"skills_{timestamp}.json"
    json_path = os.path.join(backup_dir, json_filename)
    try:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(parsed_data, f, ensure_ascii=False, indent=2)
        print_success(f"JSON 备份已保存: {json_path}")
    except Exception as e:
        print_error(f"Failed to save JSON backup: {e}")
        
    # Save Markdown
    md_filename = f"skills_{timestamp}.md"
    md_path = os.path.join(backup_dir, md_filename)
    try:
        md_content = generate_markdown(parsed_data)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        print_success(f"Markdown 备份已保存: {md_path}")
    except Exception as e:
        print_error(f"Failed to save Markdown backup: {e}")

    # Save Seed Script
    seed_filename = "data_seed_latest.py"
    # Also save a timestamped version in backups/
    seed_backup_filename = f"data_seed_{timestamp}.py"
    
    # Save to backups folder
    seed_backup_path = os.path.join(backup_dir, seed_backup_filename)
    
    # Save to root folder (latest)
    seed_latest_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), seed_filename)
    
    try:
        seed_content = generate_seed_script(parsed_data)
        
        # Save timestamped backup
        with open(seed_backup_path, "w", encoding="utf-8") as f:
            f.write(seed_content)
        print_success(f"Seed Script 备份已保存: {seed_backup_path}")
        
        # Save latest to root
        with open(seed_latest_path, "w", encoding="utf-8") as f:
            f.write(seed_content)
        print_success(f"最新 Seed Script 已更新: {seed_latest_path}")
        
    except Exception as e:
        print_error(f"Failed to save Seed Script: {e}")

if __name__ == "__main__":
    # Test run
    from dotenv import load_dotenv
    load_dotenv()
    token = os.getenv("NOTION_TOKEN")
    db_id = os.getenv("NOTION_DATABASE_ID")
    if token and db_id:
        client = Client(auth=token)
        backup_notion_data(client, db_id)
    else:
        print("Env vars missing")
