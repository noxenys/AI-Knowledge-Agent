import os
from notion_client import Client
from dotenv import load_dotenv
from agent_notion import NOTION_TOKEN, NOTION_DATABASE_ID, print_success, print_error, print_info, validate_env


def main():
    validate_env()
    load_dotenv()
    client = Client(auth=NOTION_TOKEN)

    print_info("开始扫描数据库中 Status 为 'Not started' 的页面...")

    start_cursor = None
    updated_count = 0

    while True:
        params = {
            "filter": {"property": "object", "value": "page"},
            "page_size": 100,
        }
        if start_cursor:
            params["start_cursor"] = start_cursor

        response = client.search(**params)
        results = response.get("results", [])

        for page in results:
            parent = page.get("parent", {})
            if parent.get("type") != "database_id":
                continue
            if parent.get("database_id") != NOTION_DATABASE_ID:
                continue

            properties = page.get("properties", {})
            status_prop = properties.get("Status")
            if not status_prop or status_prop.get("type") != "status":
                continue

            status_value = status_prop.get("status")
            if not status_value or status_value.get("name") != "Not started":
                continue

            page_id = page["id"]

            try:
                client.pages.update(
                    page_id=page_id,
                    properties={
                        "Status": {
                            "status": {"name": "Active"}
                        }
                    },
                )

                title_prop = properties.get("Name")
                title_text = ""
                if title_prop and title_prop.get("type") == "title":
                    title_items = title_prop.get("title", [])
                    if title_items:
                        title_text = title_items[0].get("plain_text", "")

                label = title_text or page_id
                print_success(f"已更新页面 Status 为 'Active': {label}")
                updated_count += 1
            except Exception as e:
                print_error(f"更新页面失败: {e}")

        if not response.get("has_more"):
            break

        start_cursor = response.get("next_cursor")

    if updated_count == 0:
        print_info("没有找到任何 Status 为 'Not started' 的页面。")
    else:
        print_success(f"处理完成，共更新 {updated_count} 个页面。")


if __name__ == "__main__":
    main()

