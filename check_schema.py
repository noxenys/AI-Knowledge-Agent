import os
from notion_client import Client
from dotenv import load_dotenv
import json

load_dotenv()
notion = Client(auth=os.getenv("NOTION_TOKEN"))
db_id = os.getenv("NOTION_DATABASE_ID")

try:
    print(f"Retrieving ID: {db_id}")
    # Try retrieving as database first
    try:
        db = notion.databases.retrieve(database_id=db_id)
        print("Object is a DATABASE.")
        props = db.get("properties", {})
        print(f"Properties: {list(props.keys())}")
        for name, prop in props.items():
            print(f"  {name}: {prop['type']}")
    except Exception as e:
        print(f"Not a database or error: {e}")
        # Try as page
        page = notion.pages.retrieve(page_id=db_id)
        print("Object is a PAGE.")
        print(json.dumps(page, indent=2))

except Exception as e:
    print(f"Final Error: {e}")
