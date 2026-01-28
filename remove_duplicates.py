import os
import requests
from collections import defaultdict
from dateutil import parser
from dotenv import load_dotenv
from agent_notion import NOTION_TOKEN, NOTION_DATABASE_ID, print_success, print_error, print_info, validate_env

def get_property_text(page, prop_name):
    """Helper to extract plain text from various property types."""
    props = page.get("properties", {})
    prop = props.get(prop_name)
    if not prop:
        return ""
    
    p_type = prop.get("type")
    if p_type == "title":
        items = prop.get("title", [])
        return items[0].get("plain_text", "") if items else ""
    elif p_type == "rich_text":
        items = prop.get("rich_text", [])
        return items[0].get("plain_text", "") if items else ""
    elif p_type == "url":
        return prop.get("url") or ""
    
    return ""

def main():
    validate_env()
    load_dotenv()
    
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    print_info(f"正在连接数据库 {NOTION_DATABASE_ID}...")
    print_info("开始扫描数据库进行去重检查...")

    all_pages = []
    start_cursor = None
    query_url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    
    # 1. Fetch All Pages
    while True:
        try:
            payload = {"page_size": 100}
            if start_cursor:
                payload["start_cursor"] = start_cursor

            resp = requests.post(query_url, headers=headers, json=payload, timeout=30)
            if resp.status_code != 200:
                print_error(f"查询失败: {resp.status_code} {resp.text}")
                break
                
            data = resp.json()
            results = data.get("results", [])
            all_pages.extend(results)
            
            print_info(f"已加载 {len(all_pages)} 条数据...")

            if not data.get("has_more"):
                break
            start_cursor = data.get("next_cursor")
            
        except Exception as e:
            print_error(f"Fetch error: {e}")
            break
            
    # 2. Group by Name
    groups = defaultdict(list)
    for page in all_pages:
        title = get_property_text(page, "Name")
        if title:
            groups[title].append(page)
            
    # 3. Analyze Duplicates
    duplicates_found = 0
    removed_count = 0
    
    print_info("开始分析重复项...")
    
    for title, pages in groups.items():
        if len(pages) > 1:
            duplicates_found += 1
            print_info(f"发现重复: [{title}] - 共 {len(pages)} 条")
            
            # Scoring Strategy
            # We want to keep the one with Content, and if both have content, the oldest created one.
            scored_pages = []
            for p in pages:
                content = get_property_text(p, "Content")
                created_time = parser.parse(p.get("created_time"))
                score = 0
                if content and len(content) > 10:
                    score += 100
                
                # Tie-breaker: older is better (higher score)
                # Use timestamp as negative penalty (newer = smaller score)
                score -= created_time.timestamp() / 10000000000
                
                scored_pages.append((score, p))
            
            # Sort by score descending
            scored_pages.sort(key=lambda x: x[0], reverse=True)
            
            winner = scored_pages[0][1]
            losers = [x[1] for x in scored_pages[1:]]
            
            print_success(f"  保留: ID={winner['id']} (Created: {winner['created_time']})")
            
            # 4. Delete (Archive) Losers
            for loser in losers:
                loser_id = loser['id']
                print_info(f"  🗑️ 删除: ID={loser_id} (Created: {loser['created_time']})")
                
                try:
                    del_url = f"https://api.notion.com/v1/pages/{loser_id}"
                    del_payload = {"archived": True}
                    del_resp = requests.patch(del_url, headers=headers, json=del_payload, timeout=10)
                    
                    if del_resp.status_code == 200:
                        removed_count += 1
                    else:
                        print_error(f"  删除失败: {del_resp.status_code}")
                except Exception as e:
                    print_error(f"  删除异常: {e}")

    if duplicates_found == 0:
        print_info("🎉 没有发现任何重复条目！")
    else:
        print_success(f"✅ 去重完成。发现 {duplicates_found} 组重复，删除了 {removed_count} 个多余条目。")

if __name__ == "__main__":
    main()
