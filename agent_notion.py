import os
import sys
import time
import hashlib
import argparse
import requests
from typing import List, Optional, Dict, Any
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

# Support system env vars (Docker) or .env file
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
MAX_BLOCK_LENGTH = 1800  # Safe limit below 2000

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
    if not NOTION_TOKEN:
        print_error("Missing NOTION_TOKEN in environment.")
        sys.exit(1)
    if not NOTION_DATABASE_ID:
        print_error("Missing NOTION_DATABASE_ID in environment.")
        sys.exit(1)

def md5_of_text(text: str) -> str:
    """Calculate MD5 hash of text."""
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def chunk_text(text: str, max_length: int = MAX_BLOCK_LENGTH) -> List[str]:
    """Splits text into chunks that fit within Notion's block limit."""
    if not text:
        return []
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

def build_rich_text_segments(content: str) -> List[dict]:
    """Build a list of rich_text segments that respect Notion's limit."""
    segments: List[dict] = []
    chunks = chunk_text(content, MAX_BLOCK_LENGTH)
    for chunk in chunks:
        segments.append(
            {
                "type": "text",
                "text": {"content": chunk},
            }
        )
    return segments

def extract_plain_rich_text(prop: dict) -> str:
    """Extract plain_text from a rich_text property list."""
    if not prop or prop.get("type") != "rich_text":
        return ""
    rich_list = prop.get("rich_text", [])
    buf: List[str] = []
    for item in rich_list:
        txt = item.get("plain_text")
        if txt is None:
            # Fallback to nested text.content
            text_obj = item.get("text", {})
            txt = (text_obj.get("content") or "")
        buf.append(txt)
    return "".join(buf)

def get_page_by_name(client: Client, title: str) -> Optional[dict]:
    """Query the target database by the Name(title) equals filter."""
    try:
        # Direct request to bypass potential library version issues with query
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

# -----------------------------------------------------------------------------
# Core Logic Class
# -----------------------------------------------------------------------------

class NotionAgent:
    def __init__(self):
        validate_env()
        self.client = Client(auth=NOTION_TOKEN)

    def save_to_notion(self, title: str, content: str, tag: str, url: Optional[str] = None, status: str = "Active") -> str:
        """
        Upsert item into Notion with intelligent dedup (MD5) and long-text handling.
        Returns status: 'created', 'updated', 'skipped', 'error'.
        """
        if not title:
            print_error("Title is required.")
            return "error"
        if not content:
            print_error("Content is required.")
            return "error"
        
        # Normalize Tag
        valid_tags = ["Skill", "MCP"]
        if tag not in valid_tags:
            tag = "Skill" # Default fallback

        # Prepare Content Segments (Chunking)
        rich_segments = build_rich_text_segments(content)
        new_md5 = md5_of_text(content)

        # Prepare Properties
        properties = {
            "Name": {"title": [{"text": {"content": title}}]},
            "Type": {"select": {"name": tag}},
            "Status": {"status": {"name": status}},
            "Content": {
                "rich_text": rich_segments
            },
        }

        if url:
            properties["Source"] = {"url": url}

        # 1. Check Existence
        existing_page = get_page_by_name(self.client, title)

        if not existing_page:
            # --- CREATE ---
            attempt = 0
            while attempt < MAX_RETRIES:
                try:
                    self.client.pages.create(
                        parent={"database_id": NOTION_DATABASE_ID},
                        properties=properties,
                    )
                    print_success(f"[Created]: {title}")
                    return "created"
                except APIResponseError as e:
                    attempt += 1
                    print_error(f"Notion API Error (Attempt {attempt}/{MAX_RETRIES}): {e}")
                    if attempt < MAX_RETRIES:
                        time.sleep(RETRY_DELAY)
                    else:
                        print_error(f"Failed to create '{title}' after retries.")
                        return "error"
                except Exception as e:
                    print_error(f"Unexpected Error during create: {str(e)}")
                    return "error"
            return "error"
        else:
            # --- UPDATE / SKIP ---
            page_id = existing_page["id"]
            props = existing_page.get("properties", {})
            
            # Extract existing content to compare
            content_prop = props.get("Content")
            existing_text = extract_plain_rich_text(content_prop)
            existing_md5 = md5_of_text(existing_text)

            # Check Status
            status_prop = props.get("Status", {})
            existing_status = status_prop.get("status", {}).get("name")
            
            # Check Source URL
            source_prop = props.get("Source", {})
            existing_url = source_prop.get("url")

            # Comparison Logic
            content_changed = (new_md5 != existing_md5)
            status_changed = (existing_status != status)
            url_changed = (existing_url != url) if url else False

            if not content_changed and not status_changed and not url_changed:
                print_info(f"⏭️  [Skipped]: {title}")
                return "skipped"

            # Perform Update
            try:
                self.client.pages.update(
                    page_id=page_id,
                    properties=properties,
                )
                print_success(f"🔄 [Updated]: {title}")
                return "updated"
            except Exception as e:
                print_error(f"Update failed for '{title}': {e}")
                return "error"

# -----------------------------------------------------------------------------
# CLI Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Notion Automation Agent Core")
    parser.add_argument("--title", required=True, help="Title of the page")
    parser.add_argument("--content", required=True, help="Content (Markdown supported)")
    parser.add_argument("--tag", required=True, choices=["Skill", "MCP"], help="Tag: Skill or MCP")
    parser.add_argument("--url", help="Optional URL resource")
    parser.add_argument("--status", default="Active", help="Status (Active, Broken, Review)")

    args = parser.parse_args()

    agent = NotionAgent()
    agent.save_to_notion(
        title=args.title,
        content=args.content,
        tag=args.tag,
        url=args.url,
        status=args.status
    )
