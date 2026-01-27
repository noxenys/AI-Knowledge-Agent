import os
import sys
import time
import argparse
import requests
from typing import List, Optional
from dotenv import load_dotenv
from notion_client import Client
from notion_client.errors import APIResponseError
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# -----------------------------------------------------------------------------
# Configuration & Constants
# -----------------------------------------------------------------------------
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

print(f"DEBUG: Loaded DB ID: {NOTION_DATABASE_ID}")

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
MAX_BLOCK_LENGTH = 2000

# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------

def print_success(message: str):
    """Prints a green success message."""
    print(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")

def print_error(message: str):
    """Prints a red error message."""
    print(f"{Fore.RED}❌ {message}{Style.RESET_ALL}")

def print_info(message: str):
    """Prints a generic info message."""
    print(f"{Fore.CYAN}ℹ️  {message}{Style.RESET_ALL}")

def validate_env():
    """Ensures environment variables are set."""
    if not NOTION_TOKEN or NOTION_TOKEN.startswith("ntn_your_"):
        print_error("Missing or invalid NOTION_TOKEN in .env file.")
        sys.exit(1)
    if not NOTION_DATABASE_ID or NOTION_DATABASE_ID.startswith("your_database_"):
        print_error("Missing or invalid NOTION_DATABASE_ID in .env file.")
        sys.exit(1)

def split_text_to_chunks(text: str, max_length: int = MAX_BLOCK_LENGTH) -> List[str]:
    """Splits text into chunks that fit within Notion's block limit."""
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

def build_rich_text_segments(content: str) -> List[dict]:
    """Build a list of rich_text segments that respect Notion's 2000-char limit."""
    segments: List[dict] = []
    for chunk in split_text_to_chunks(content, MAX_BLOCK_LENGTH):
        segments.append(
            {
                "type": "text",
                "text": {"content": chunk},
            }
        )
    return segments

def get_page_by_name(client: Client, title: str) -> Optional[dict]:
    """Query the target database by the Name(title) equals filter."""
    try:
        # Use direct requests due to environment library issue
        url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
        headers = {
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        payload = {
            "filter": {"property": "Name", "title": {"equals": title}},
            "page_size": 1
        }
        
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if resp.status_code == 200:
            results = resp.json().get("results", [])
            return results[0] if results else None
        else:
            print_error(f"Query by Name failed: {resp.status_code} {resp.text}")
            return None
            
    except Exception as e:
        print_error(f"Query by Name failed: {e}")
        return None

def extract_plain_rich_text(prop: dict) -> str:
    """Extract plain_text from a rich_text property list."""
    if not prop or prop.get("type") != "rich_text":
        return ""
    rich_list = prop.get("rich_text", [])
    buf: List[str] = []
    for item in rich_list:
        txt = item.get("plain_text")
        if txt is None:
            # Fallback to nested text.content if plain_text not present
            text_obj = item.get("text", {})
            txt = (text_obj.get("content") or "")
        buf.append(txt)
    return "".join(buf)

# -----------------------------------------------------------------------------
# Core Logic Class
# -----------------------------------------------------------------------------

class NotionAgent:
    def __init__(self):
        validate_env()
        self.client = Client(auth=NOTION_TOKEN)

    def save_to_notion(self, title: str, content: str, tag: str, url: Optional[str] = None, status: str = "Active") -> str:
        """Upsert item into Notion with intelligent dedup and long-text handling. Returns status: 'created', 'updated', 'skipped', 'error'."""
        if not title:
            print_error("Title is required.")
            return "error"
        if not content:
            print_error("Content is required.")
            return "error"
        if tag not in ["Skill", "MCP"]:
            print_error(f"Invalid tag: {tag}. Must be 'Skill' or 'MCP'.")
            return "error"

        rich_segments = build_rich_text_segments(content)

        properties = {
            "Name": {"title": [{"text": {"content": title}}]},
            "Type": {"select": {"name": tag}},
            "Status": {"status": {"name": "Active" if not status else status}},
            "Content": {
                "rich_text": rich_segments
            },
        }

        if url:
            properties["Source"] = {"url": url}

        # Upsert flow: find existing by Name
        existing = get_page_by_name(self.client, title)
        if not existing:
            # Create new page
            attempt = 0
            while attempt < MAX_RETRIES:
                try:
                    self.client.pages.create(
                        parent={"database_id": NOTION_DATABASE_ID},
                        properties=properties,
                    )
                    print_success(f"[Saved]: {title}")
                    return "created"
                except APIResponseError as e:
                    attempt += 1
                    print_error(f"Notion API Error (Attempt {attempt}/{MAX_RETRIES}): {e}")
                    if attempt < MAX_RETRIES:
                        time.sleep(RETRY_DELAY)
                    else:
                        print_error(f"Failed to save '{title}' after {MAX_RETRIES} attempts.")
                        raise e
                except Exception as e:
                    print_error(f"Unexpected Error: {str(e)}")
                    return "error"
            return "error"
        else:
            # Compare existing Content and Status; update if either changed
            props = existing.get("properties", {})
            
            # Check Content
            content_prop = props.get("Content")
            prev_content = extract_plain_rich_text(content_prop)
            curr_content = "".join([seg["text"]["content"] for seg in rich_segments])

            # Check Status
            status_prop = props.get("Status", {})
            prev_status = status_prop.get("status", {}).get("name")
            target_status = "Active" if not status else status

            if prev_content == curr_content and prev_status == target_status:
                print_info(f"⏭️  [Skipped]: {title} (no changes)")
                return "skipped"

            page_id = existing["id"]
            try:
                self.client.pages.update(
                    page_id=page_id,
                    properties=properties,
                )
                print_success(f"[Updated]: {title}")
                return "updated"
            except Exception as e:
                print_error(f"Update failed: {e}")
                return "error"

# -----------------------------------------------------------------------------
# CLI Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Notion Automation Agent")
    parser.add_argument("--title", required=True, help="Title of the page")
    parser.add_argument("--content", required=True, help="Content (Markdown supported)")
    parser.add_argument("--tag", required=True, choices=["Skill", "MCP"], help="Tag: Skill or MCP")
    parser.add_argument("--url", help="Optional URL resource")

    args = parser.parse_args()

    agent = NotionAgent()
    agent.save_to_notion(
        title=args.title,
        content=args.content,
        tag=args.tag,
        url=args.url
    )
