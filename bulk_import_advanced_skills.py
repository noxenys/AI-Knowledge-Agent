from agent_notion import NotionAgent


def build_items():
    return [
        {
            "title": "Modern Web Scraping",
            "tag": "Skill",
            "url": "https://cursor.directory/modern-web-scraping",
            "content": (
                "**用途简介**: 面向 Python 的现代网页爬虫规则，涵盖 requests、BeautifulSoup、"
                "Selenium 以及 firecrawl/agentQL 等高级工具，适合构建稳定的生产级采集脚本。\n\n"
                "# Modern Web Scraping (Cursor Rule)\n\n"
                "- Use requests for static pages and BeautifulSoup for HTML parsing.\n"
                "- Use Selenium or headless browsers for JavaScript-heavy sites.\n"
                "- Respect robots.txt and terms of service.\n"
                "- Implement rate limiting, random delays, and proper headers.\n"
                "- Validate scraped data formats and types before processing.\n"
                "- Use asyncio or concurrent.futures for concurrent scraping.\n"
                "- Handle CAPTCHAs and complex flows with agentQL, jina, or multion.\n"
            ),
        },
        {
            "title": "Web Scraping",
            "tag": "Skill",
            "url": "https://cursor.directory/rules/web-scraping",
            "content": (
                "**用途简介**: 通用 Web Scraping 规则，强调模块化、错误重试和数据验证，适合你各类采集任务的基准规则。\n\n"
                "# Web Scraping (Cursor Rule)\n\n"
                "- Modularize scraping logic into reusable functions.\n"
                "- Follow PEP 8 and keep code readable and maintainable.\n"
                "- Use proper User-Agent and headers, avoid aggressive crawling.\n"
                "- Implement robust error handling and retry with backoff.\n"
                "- Store data in CSV/JSON/SQLite with clear schemas.\n"
            ),
        },
        {
            "title": "Playwright Cursor Rules",
            "tag": "Skill",
            "url": "https://cursor.directory/playwright-cursor-rules",
            "content": (
                "**用途简介**: Playwright 端到端自动化测试与爬虫规则，适合你的麦当劳脚本和复杂登录流程。\n\n"
                "# Playwright Cursor Rules\n\n"
                "- Use fixtures (test, page, expect) for isolation.\n"
                "- Use page.getByRole / getByLabel / getByText over CSS/XPath.\n"
                "- Avoid hardcoded timeouts; rely on web-first assertions.\n"
                "- Use test.beforeEach / afterEach for setup and teardown.\n"
                "- Run tests in parallel without shared mutable state.\n"
            ),
        },
        {
            "title": "Playwright MCP (official)",
            "tag": "MCP",
            "url": "https://github.com/microsoft/playwright-mcp",
            "content": (
                "**用途简介**: 微软官方 Playwright MCP Server，用于浏览器自动化、可视化调试和反爬策略实验。\n\n"
                "# Playwright MCP Server (Microsoft)\n\n"
                "- Provides browser automation via MCP using Playwright.\n"
                "- Uses accessibility tree instead of screenshots.\n"
                "- Suitable for exploratory automation and self-healing tests.\n"
                "- Standard config: command `npx @playwright/mcp@latest`.\n"
            ),
        },
        {
            "title": "Playwright MCP Server (ExecuteAutomation)",
            "tag": "MCP",
            "url": "https://github.com/executeautomation/mcp-playwright",
            "content": (
                "**用途简介**: 支持截图、设备模拟（iPhone/Android）、JS 执行的 Playwright MCP，适合多终端反爬实验。\n\n"
                "# ExecuteAutomation Playwright MCP Server\n\n"
                "- Full browser automation: navigation, click, form filling.\n"
                "- Screenshot capture for full page or specific elements.\n"
                "- Device emulation with many real device presets.\n"
                "- Installed via `npx @executeautomation/playwright-mcp-server`.\n"
            ),
        },
        {
            "title": "Playwright Universal MCP (Python)",
            "tag": "MCP",
            "url": "https://github.com/xkiranj/playwright-universal-mcp",
            "content": (
                "**用途简介**: Python 实现的通用 Playwright MCP，支持容器环境，适合你未来用 Docker 部署自动化。\n\n"
                "# Playwright Universal MCP\n\n"
                "- Multi-browser support (Chromium, Firefox, WebKit, Edge, Chrome).\n"
                "- Designed for containerized environments.\n"
                "- Tools: navigate, click, type, get_text, screenshots, etc.\n"
                "- Run via `playwright-universal-mcp --browser msedge --headless`.\n"
            ),
        },
        {
            "title": "Stripe Cursor Rules",
            "tag": "Skill",
            "url": "https://cursor.directory/rules/stripe",
            "content": (
                "**用途简介**: Stripe 支付与订阅模型规则，适合未来接入 Stripe API 做订阅付费。\n\n"
                "# Stripe Integration Rules\n\n"
                "- Implement Stripe for payments and subscription management.\n"
                "- Use Stripe Customer Portal for managing subscriptions.\n"
                "- Handle webhooks for created/updated/canceled subscriptions.\n"
                "- Sync subscription status with your user database.\n"
                "- Apply strong error handling and security best practices.\n"
            ),
        },
        {
            "title": "Stripe MCP Server",
            "tag": "MCP",
            "url": "https://cursor.directory/mcp/stripe-agent-toolkit",
            "content": (
                "**用途简介**: 提供直接操作 Stripe 的 MCP Server，适合在 Cursor 内完成账单、订阅和退款操作。\n\n"
                "# Stripe Agent Toolkit MCP\n\n"
                "- Integrates with Stripe API via MCP tools.\n"
                "- Supports payment processing and customer management.\n"
                "- Good for automating billing workflows from Cursor.\n"
            ),
        },
        {
            "title": "Notion MCP Server",
            "tag": "MCP",
            "url": "https://cursor.directory/mcp/notion-6",
            "content": (
                "**用途简介**: 官方 Notion MCP Server，支持在 Cursor 内搜索、读取、创建和更新 Notion 内容。\n\n"
                "# Notion MCP Server\n\n"
                "- Tools for searching and reading Notion pages and databases.\n"
                "- Create and update pages directly from the editor.\n"
                "- Requires a Notion integration token and shared pages.\n"
            ),
        },
        {
            "title": "Notion MCP Server (ecovirtual)",
            "tag": "MCP",
            "url": "https://github.com/ramidecodes/mcp-server-notion",
            "content": (
                "**用途简介**: 基于官方 SDK 的 Notion MCP Server，文档中包含 Cursor 集成的详细实践指南。\n\n"
                "# mcp-server-notion\n\n"
                "- Wraps official Notion SDK as an MCP server.\n"
                "- Cursor integration via `npx @ecovirtual/mcp-server-notion@latest`.\n"
                "- Supports search, append blocks, query databases, etc.\n"
                "- Docs include troubleshooting for API key and access.\n"
            ),
        },
    ]


def main():
    agent = NotionAgent()
    items = build_items()

    for idx, item in enumerate(items, 1):
        print(f"[{idx}/{len(items)}] Saving: {item['title']}")
        agent.save_to_notion(
            title=item["title"],
            content=item["content"],
            tag=item["tag"],
            url=item["url"],
            status="Active",
        )


if __name__ == "__main__":
    main()

