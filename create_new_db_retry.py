import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("NOTION_TOKEN")
notion = Client(auth=token)

page_id = "2f564d60-7387-81bc-bbd8-f1aa5709e843"

try:
    print(f"Creating new database inside page {page_id}...")
    new_db = notion.databases.create(
        parent={"type": "page_id", "page_id": page_id},
        title=[{"type": "text", "text": {"content": "Final AI Skills List"}}],
        properties={
            "Name": {"title": {}},
            "Tags": {"multi_select": {
                "options": [
                    {"name": "Skill", "color": "blue"},
                    {"name": "MCP", "color": "purple"}
                ]
            }},
            "Source Link": {"url": {}},
            "Content": {"rich_text": {}}
        }
    )
    print("New Database Created!")
    print(f"New Database ID: {new_db['id']}")
    
    # Update .env
    with open(".env", "r") as f:
        lines = f.readlines()
    
    with open(".env", "w") as f:
        for line in lines:
            if "NOTION_DATABASE_ID" in line:
                f.write(f"NOTION_DATABASE_ID={new_db['id']}\n")
            else:
                f.write(line)
    print("Updated .env with new Database ID.")

except Exception as e:
    print(f"Failed: {e}")
