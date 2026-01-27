import os
from notion_client import Client
from dotenv import load_dotenv
import json

load_dotenv()
notion = Client(auth=os.getenv("NOTION_TOKEN"))
db_id = os.getenv("NOTION_DATABASE_ID")

try:
    print(f"Querying ID: {db_id}")
    results = notion.databases.query(database_id=db_id, page_size=1)
    print("Query Result:")
    print(json.dumps(results, indent=2))
except Exception as e:
    print(f"Query Error: {e}")
