import os
import requests
from dotenv import load_dotenv
from agent_notion import extract_plain_rich_text

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

def fetch_active_skills():
    """Fetch all pages with Status='Active'."""
    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    payload = {
        "filter": {
            "property": "Status",
            "status": {
                "equals": "Active"
            }
        }
    }
    
    results = []
    has_more = True
    next_cursor = None
    
    while has_more:
        if next_cursor:
            payload["start_cursor"] = next_cursor
        
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
            if resp.status_code != 200:
                print(f"Error fetching data: {resp.text}")
                break
                
            data = resp.json()
            results.extend(data.get("results", []))
            has_more = data.get("has_more", False)
            next_cursor = data.get("next_cursor")
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
            break
        
    return results

def format_for_trae(pages):
    """Format pages into a single string for Trae."""
    output_lines = []
    
    output_lines.append("# Trae Global Skills & Rules Export")
    output_lines.append(f"# Generated from Notion Database: {len(pages)} items\n")
    
    for page in pages:
        props = page.get("properties", {})
        
        # Name
        name_prop = props.get("Name", {})
        title_list = name_prop.get("title", [])
        title = title_list[0].get("text", {}).get("content", "Untitled") if title_list else "Untitled"
        
        # Content
        content_prop = props.get("Content", {})
        content = extract_plain_rich_text(content_prop)
        
        output_lines.append(f"## {title}")
        output_lines.append(content)
        output_lines.append("\n" + "-"*40 + "\n")
        
    return "\n".join(output_lines)

def main():
    print("⏳ Fetching Active skills from Notion...")
    pages = fetch_active_skills()
    print(f"✅ Found {len(pages)} active skills.")
    
    formatted_text = format_for_trae(pages)
    
    print("\n" + "="*20 + " COPY BELOW THIS LINE " + "="*20 + "\n")
    print(formatted_text)
    print("\n" + "="*20 + " COPY ABOVE THIS LINE " + "="*20 + "\n")

if __name__ == "__main__":
    main()
