from agent_notion import NotionAgent
import time


def build_items():
    return [
        {
            "title": "Stripe Iframe Master",
            "tag": "Skill",
            "url": "https://docs.stripe.com/payments/payment-element/best-practices",
            "content": (
                "中文功能简介：专门处理 Stripe 支付元素在 iframe 下的复杂嵌套与跳转问题，指导表单布局与重定向策略，确保安全与合规。\n\n"
                "Original English Prompt:\n"
                "The Payment Element contains an iframe that securely sends payment information to Stripe over an HTTPS connection. "
                "Avoid placing the Payment Element within another iframe because some payment methods require a redirect to another page for payment confirmation. "
                "For more information on iframe considerations, see Collect payment details.\n"
                "Source: https://docs.stripe.com/payments/payment-element/best-practices"
            ),
        },
        {
            "title": "Cloudflare Bypass Expert",
            "tag": "Skill",
            "url": "https://github.com/unixfox/pupflare",
            "content": (
                "中文功能简介：针对自动化脚本过 Cloudflare 防护的工程化实践，采用 Chromium 代理、挑战等待、UserDataDir、Headful/Headless 切换等策略。\n\n"
                "Original English Prompt:\n"
                "A webpage proxy that request through Chromium (puppeteer) - can be used to bypass Cloudflare anti bot / anti ddos on any application (like curl). "
                "This script has been configured to wait for the cloudflare challenge to pass but, you can configure the \"match\" for anything else using the environment variable CHALLENGE_MATCH. "
                "To show the browser window, set the environment variable PUPPETEER_HEADFUL=1. "
                "To specify user data directory, set PUPPETEER_USERDATADIR=/path/to/dir.\n"
                "Source: https://github.com/unixfox/pupflare"
            ),
        },
        {
            "title": "merajmehrabi/puppeteer-mcp-server",
            "tag": "MCP",
            "url": "https://github.com/merajmehrabi/puppeteer-mcp-server",
            "content": (
                "中文功能简介：Puppeteer MCP 服务器，提供浏览器自动化工具集，支持 npx/本地/Node 直接运行并接入 Claude。\n\n"
                "Original English Prompt:\n"
                "This MCP server provides browser automation capabilities via Puppeteer with tool definitions, browser connection, and server initialization. "
                "Add the following to your Claude Desktop configuration file:\n"
                "{ \"mcpServers\": { \"puppeteer\": { \"command\": \"npx\", \"args\": [\"-y\", \"puppeteer-mcp-server\"], \"env\": {} } } }\n"
                "Source: https://github.com/merajmehrabi/puppeteer-mcp-server"
            ),
        },
        {
            "title": "sultannaufal/puppeteer-mcp-server",
            "tag": "MCP",
            "url": "https://github.com/sultannaufal/puppeteer-mcp-server",
            "content": (
                "中文功能简介：自托管 Puppeteer MCP，提供 HTTP/SSE 远程访问、API Key 认证与 Docker 部署，生产可用。\n\n"
                "Original English Prompt:\n"
                "Self-hosted Puppeteer MCP server with remote SSE access, API key authentication, and Docker deployment. "
                "Add the server with HTTP transport:\n"
                "claude mcp add puppeteer http://localhost:3000/http --scope user --transport http --header \"Authorization: Bearer your-api-key-here\"\n"
                "Source: https://github.com/sultannaufal/puppeteer-mcp-server"
            ),
        },
        {
            "title": "ratiofu/mcp-puppeteer",
            "tag": "MCP",
            "url": "https://github.com/ratiofu/mcp-puppeteer",
            "content": (
                "中文功能简介：轻量 Puppeteer MCP 服务器，智能浏览器管理、自动 npx 下载与启动，简化接入。\n\n"
                "Original English Prompt:\n"
                "A Model Context Protocol (MCP) server that provides browser automation capabilities through Puppeteer with intelligent browser management. "
                "The server automatically downloads and runs via npx when your MCP client needs it.\n"
                "Source: https://github.com/ratiofu/mcp-puppeteer"
            ),
        },
        {
            "title": "jaenster/puppeteer-mcp-claude",
            "tag": "MCP",
            "url": "https://github.com/jaenster/puppeteer-mcp-claude",
            "content": (
                "中文功能简介：面向 Claude 的 Puppeteer MCP，开箱 10+ 浏览器工具，跨平台安装简便。\n\n"
                "Original English Prompt:\n"
                "A Model Context Protocol server with 11 new puppeteer tools for browser automation. "
                "Add via npx: { \"command\": \"npx\", \"args\": [\"puppeteer-mcp-claude\", \"serve\"], \"env\": { \"NODE_ENV\": \"production\" } }\n"
                "Source: https://github.com/jaenster/puppeteer-mcp-claude"
            ),
        },
        {
            "title": "twolven/mcp-server-puppeteer-py",
            "tag": "MCP",
            "url": "https://github.com/twolven/mcp-server-puppeteer-py",
            "content": (
                "中文功能简介：Python 版 Playwright MCP 服务器，提供截图、执行 JS 等能力，错误处理更稳健。\n\n"
                "Original English Prompt:\n"
                "MCP server providing browser automation capabilities using Playwright (Python's equivalent to Puppeteer). "
                "This server enables LLMs to interact with web pages, take screenshots, and execute JavaScript in a real browser environment.\n"
                "Source: https://github.com/twolven/mcp-server-puppeteer-py"
            ),
        },
        {
            "title": "ZFC-Digital/puppeteer-real-browser",
            "tag": "Skill",
            "url": "https://github.com/ZFC-Digital/puppeteer-real-browser",
            "content": (
                "中文功能简介：模拟“真实浏览器”行为，降低被 Cloudflare 等服务识别为机器人风险，支持 Turnstile 自动点击。\n\n"
                "Original English Prompt:\n"
                "This package prevents Puppeteer from being detected as a bot in services like Cloudflare and allows you to pass captchas without any problems. "
                "It behaves like a real browser. Turnstile: Cloudflare Turnstile automatically clicks on Captchas if set to true.\n"
                "Source: https://github.com/ZFC-Digital/puppeteer-real-browser"
            ),
        },
        {
            "title": "Stripe Agent Toolkit (MCP)",
            "tag": "MCP",
            "url": "https://cursor.directory/mcp/stripe-agent-toolkit",
            "content": (
                "中文功能简介：通过 MCP 接入 Stripe API，实现支付、客户管理与账务工作流。\n\n"
                "Original English Prompt:\n"
                "Integrates with Stripe's API to enable payment processing, customer management, and financial operations for e-commerce and billing workflows.\n"
                "Source: https://cursor.directory/mcp/stripe-agent-toolkit"
            ),
        },
        {
            "title": "Stripe MCP Server",
            "tag": "MCP",
            "url": "https://cursor.directory/mcp/stripe",
            "content": (
                "中文功能简介：与 Stripe API 交互的官方 MCP 入口，用于支付相关操作。\n\n"
                "Original English Prompt:\n"
                "Interact with the Stripe API via MCP. Install and configure in Cursor Settings > Features > MCP.\n"
                "Source: https://cursor.directory/mcp/stripe"
            ),
        },
    ]


def main():
    agent = NotionAgent()
    items = build_items()
    print(f"准备入库：{len(items)} 条精准采集结果，Status=Active")

    for idx, item in enumerate(items, 1):
        print(f"[{idx}/{len(items)}] Saving: {item['title']}")
        agent.save_to_notion(
            title=item["title"],
            content=item["content"],
            tag=item["tag"],
            url=item["url"],
            status="Active",
        )
        time.sleep(0.5)

    print("入库完成")


if __name__ == "__main__":
    main()

