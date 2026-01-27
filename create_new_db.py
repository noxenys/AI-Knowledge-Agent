import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

# Get Parent Page ID from Environment Variable (Optional) or create new
parent_page_id = os.getenv("NOTION_PARENT_PAGE_ID")
token = os.getenv("NOTION_TOKEN")

if not token:
    print("Error: NOTION_TOKEN is missing in .env")
    exit(1)

notion = Client(auth=token)

try:
    if not parent_page_id:
        print("NOTION_PARENT_PAGE_ID not found in .env. Creating a container page first...")
        # Since we cannot create a top-level page without a parent via API easily unless it's a child of another page 
        # or we just assume the user wants to create a database at the top level (which requires parent type 'workspace' or 'page_id').
        # However, 'workspace' parent is not supported for creating pages via API for all integrations (usually requires page_id).
        # We'll try to search for an existing page to use as parent or ask user to provide one.
        # For automation, let's assume we need a parent page ID.
        print("Please set NOTION_PARENT_PAGE_ID in .env to a valid Page ID where the database should be created.")
        
        # Fallback: Search for any page to use as parent (Dangerous? Maybe, but automation needs a target)
        print("Searching for a potential parent page...")
        search = notion.search(filter={"property": "object", "value": "page"}, page_size=1)
        if search["results"]:
            parent_page_id = search["results"][0]["id"]
            print(f"Found a page to use as parent: {parent_page_id}")
        else:
            print("No pages found to use as parent. Cannot create database.")
            exit(1)

    print(f"Creating new database under Page ID: {parent_page_id}...")
    new_db = notion.databases.create(
        parent={"page_id": parent_page_id},
        title=[{"type": "text", "text": {"content": "Final AI Skills List"}}],
        properties={
            "Name": {"title": {}},
            "Type": {
                "select": {
                    "options": [
                        {"name": "Skill", "color": "blue"},
                        {"name": "MCP", "color": "purple"}
                    ]
                }
            },
            "Status": {"status": {}},
            "Source": {"url": {}},
            "Content": {"rich_text": {}}
        }
    )
    print("New Database Created Successfully!")
    print(f"New Database ID: {new_db['id']}")
    
    # Update .env
    env_path = ".env"
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            lines = f.readlines()
    else:
        lines = []

    # Check if NOTION_DATABASE_ID exists
    found = False
    new_lines = []
    for line in lines:
        if line.startswith("NOTION_DATABASE_ID="):
            new_lines.append(f"NOTION_DATABASE_ID={new_db['id']}\n")
            found = True
        else:
            new_lines.append(line)
    
    if not found:
        new_lines.append(f"\nNOTION_DATABASE_ID={new_db['id']}\n")

    with open(env_path, "w") as f:
        f.writelines(new_lines)
        
    print("Updated .env with new Database ID.")

except Exception as e:
    print(f"Failed: {e}")

