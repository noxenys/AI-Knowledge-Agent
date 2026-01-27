import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()
notion = Client(auth=os.getenv("NOTION_TOKEN"))
db_id = os.getenv("NOTION_DATABASE_ID")

payload = {
    "properties": {
        "Status": {
            "status": {
                "groups": [
                    {
                        "name": "To-do",
                        "options": [
                             {"name": "Review", "color": "red"},
                             {"name": "Broken", "color": "gray"}
                        ]
                    },
                    {
                        "name": "In progress",
                        "options": [
                            {"name": "Active", "color": "blue"}
                        ]
                    },
                    {
                        "name": "Complete",
                        "options": [
                            {"name": "Done", "color": "green"}
                        ]
                    }
                ]
            }
        }
    }
}

try:
    print("Updating schema to add 'Broken' status...")
    notion.databases.update(database_id=db_id, **payload)
    print("Update command sent.")
except Exception as e:
    print(f"Error: {e}")
