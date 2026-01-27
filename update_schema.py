import os
import sys
from notion_client import Client
from dotenv import load_dotenv
from colorama import init, Fore, Style

init(autoreset=True)
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

def print_success(msg): print(f"{Fore.GREEN}✅ {msg}{Style.RESET_ALL}")
def print_error(msg): print(f"{Fore.RED}❌ {msg}{Style.RESET_ALL}")
def print_info(msg): print(f"{Fore.CYAN}ℹ️  {msg}{Style.RESET_ALL}")

def update_schema():
    if not NOTION_TOKEN or not NOTION_DATABASE_ID:
        print_error("Missing Environment Variables")
        return

    client = Client(auth=NOTION_TOKEN)

    try:
        print_info(f"Checking schema for Database ID: {NOTION_DATABASE_ID}")
        db = client.databases.retrieve(database_id=NOTION_DATABASE_ID)
        props = db.get("properties", {})
        
        # 1. Ensure 'Status' is native status
        status_prop = props.get("Status")
        if not status_prop:
            print_info("'Status' property missing. Creating as Native Status...")
            client.databases.update(
                database_id=NOTION_DATABASE_ID,
                properties={"Status": {"status": {}}}
            )
            print_success("Created 'Status' property.")
        elif status_prop.get("type") == "select":
            print_info("Detected Conflict: 'Status' is 'select'. Renaming and creating native Status...")
            client.databases.update(
                database_id=NOTION_DATABASE_ID,
                properties={"Status": {"name": "Status_Legacy"}}
            )
            client.databases.update(
                database_id=NOTION_DATABASE_ID,
                properties={"Status": {"status": {}}}
            )
            print_success("Fixed 'Status' property.")
        else:
            print_success(f"'Status' property exists as {status_prop.get('type')}.")

        # 2. Ensure 'Type' is select
        type_prop = props.get("Type")
        if not type_prop:
            print_info("'Type' property missing. Creating as Select...")
            client.databases.update(
                database_id=NOTION_DATABASE_ID,
                properties={
                    "Type": {
                        "select": {
                            "options": [
                                {"name": "Skill", "color": "blue"},
                                {"name": "MCP", "color": "purple"}
                            ]
                        }
                    }
                }
            )
            print_success("Created 'Type' property.")
        elif type_prop.get("type") != "select":
             print_error(f"'Type' property exists but is {type_prop.get('type')} (expected select). Manual check recommended.")
        else:
             print_success("'Type' property exists as select.")

        # 3. Ensure 'Source' is url
        # Note: Previous script might have used 'Source Link', checking conflict
        source_prop = props.get("Source")
        source_link_prop = props.get("Source Link")
        
        if not source_prop:
            if source_link_prop and source_link_prop.get("type") == "url":
                print_info("'Source Link' exists but 'Source' missing. Renaming 'Source Link' to 'Source'...")
                client.databases.update(
                    database_id=NOTION_DATABASE_ID,
                    properties={"Source Link": {"name": "Source"}}
                )
                print_success("Renamed 'Source Link' to 'Source'.")
            else:
                print_info("'Source' property missing. Creating as URL...")
                client.databases.update(
                    database_id=NOTION_DATABASE_ID,
                    properties={"Source": {"url": {}}}
                )
                print_success("Created 'Source' property.")
        else:
            print_success("'Source' property exists.")

        # 4. Ensure 'Content' is rich_text
        content_prop = props.get("Content")
        if not content_prop:
             print_info("'Content' property missing. Creating as Rich Text...")
             client.databases.update(
                database_id=NOTION_DATABASE_ID,
                properties={"Content": {"rich_text": {}}}
            )
             print_success("Created 'Content' property.")
        else:
             print_success("'Content' property exists.")
            
        print_success("Schema update/verification complete.")

    except Exception as e:
        print_error(f"Schema update failed: {e}")

if __name__ == "__main__":
    update_schema()
