import os
import sys
import json
from typing import List, Dict, Any

# Ensure we can find the agent modules if running from project root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from agent_notion import NotionAgent, NOTION_TOKEN, NOTION_DATABASE_ID
except ImportError:
    print("❌ 错误: 找不到 agent_notion.py 模块。请确保此脚本在项目根目录下运行。")
    sys.exit(1)

# DATA SEED GENERATED AT: 2026-01-27 22:05:21
# TOTAL ITEMS: 19

SEED_DATA: List[Dict[str, Any]] = [   {   'title': 'Notion MCP Server (ecovirtual)',
        'content': '**用途简介**: 基于官方 SDK 的 Notion MCP Server，文档中包含 Cursor 集成的详细实践指南。\n'
                   '\n'
                   '# mcp-server-notion\n'
                   '\n'
                   '- Wraps official Notion SDK as an MCP server.\n'
                   '- Cursor integration via `npx @ecovirtual/mcp-server-notion@latest`.\n'
                   '- Supports search, append blocks, query databases, etc.\n'
                   '- Docs include troubleshooting for API key and access.\n',
        'tag': 'MCP',
        'url': 'https://github.com/ramidecodes/mcp-server-notion',
        'status': 'Active'},
    {   'title': 'Notion MCP Server',
        'content': '**用途简介**: 官方 Notion MCP Server，支持在 Cursor 内搜索、读取、创建和更新 Notion 内容。\n'
                   '\n'
                   '# Notion MCP Server\n'
                   '\n'
                   '- Tools for searching and reading Notion pages and databases.\n'
                   '- Create and update pages directly from the editor.\n'
                   '- Requires a Notion integration token and shared pages.\n',
        'tag': 'MCP',
        'url': 'https://cursor.directory/mcp/notion-6',
        'status': 'Active'},
    {   'title': 'Stripe MCP Server',
        'content': '**用途简介**: 提供直接操作 Stripe 的 MCP Server，适合在 Cursor 内完成账单、订阅和退款操作。\n'
                   '\n'
                   '# Stripe Agent Toolkit MCP\n'
                   '\n'
                   '- Integrates with Stripe API via MCP tools.\n'
                   '- Supports payment processing and customer management.\n'
                   '- Good for automating billing workflows from Cursor.\n',
        'tag': 'MCP',
        'url': 'https://cursor.directory/mcp/stripe-agent-toolkit',
        'status': 'Active'},
    {   'title': 'Stripe Cursor Rules',
        'content': '**用途简介**: Stripe 支付与订阅模型规则，适合未来接入 Stripe API 做订阅付费。\n'
                   '\n'
                   '# Stripe Integration Rules\n'
                   '\n'
                   '- Implement Stripe for payments and subscription management.\n'
                   '- Use Stripe Customer Portal for managing subscriptions.\n'
                   '- Handle webhooks for created/updated/canceled subscriptions.\n'
                   '- Sync subscription status with your user database.\n'
                   '- Apply strong error handling and security best practices.\n',
        'tag': 'Skill',
        'url': 'https://cursor.directory/rules/stripe',
        'status': 'Active'},
    {   'title': 'Playwright Universal MCP (Python)',
        'content': '**用途简介**: Python 实现的通用 Playwright MCP，支持容器环境，适合你未来用 Docker 部署自动化。\n'
                   '\n'
                   '# Playwright Universal MCP\n'
                   '\n'
                   '- Multi-browser support (Chromium, Firefox, WebKit, Edge, Chrome).\n'
                   '- Designed for containerized environments.\n'
                   '- Tools: navigate, click, type, get_text, screenshots, etc.\n'
                   '- Run via `playwright-universal-mcp --browser msedge --headless`.\n',
        'tag': 'MCP',
        'url': 'https://github.com/xkiranj/playwright-universal-mcp',
        'status': 'Active'},
    {   'title': 'Playwright MCP Server (ExecuteAutomation)',
        'content': '**用途简介**: 支持截图、设备模拟（iPhone/Android）、JS 执行的 Playwright MCP，适合多终端反爬实验。\n'
                   '\n'
                   '# ExecuteAutomation Playwright MCP Server\n'
                   '\n'
                   '- Full browser automation: navigation, click, form filling.\n'
                   '- Screenshot capture for full page or specific elements.\n'
                   '- Device emulation with many real device presets.\n'
                   '- Installed via `npx @executeautomation/playwright-mcp-server`.\n',
        'tag': 'MCP',
        'url': 'https://github.com/executeautomation/mcp-playwright',
        'status': 'Active'},
    {   'title': 'Playwright MCP (official)',
        'content': '**用途简介**: 微软官方 Playwright MCP Server，用于浏览器自动化、可视化调试和反爬策略实验。\n'
                   '\n'
                   '# Playwright MCP Server (Microsoft)\n'
                   '\n'
                   '- Provides browser automation via MCP using Playwright.\n'
                   '- Uses accessibility tree instead of screenshots.\n'
                   '- Suitable for exploratory automation and self-healing tests.\n'
                   '- Standard config: command `npx @playwright/mcp@latest`.\n',
        'tag': 'MCP',
        'url': 'https://github.com/microsoft/playwright-mcp',
        'status': 'Active'},
    {   'title': 'Playwright Cursor Rules',
        'content': '**用途简介**: Playwright 端到端自动化测试与爬虫规则，适合你的麦当劳脚本和复杂登录流程。\n'
                   '\n'
                   '# Playwright Cursor Rules\n'
                   '\n'
                   '- Use fixtures (test, page, expect) for isolation.\n'
                   '- Use page.getByRole / getByLabel / getByText over CSS/XPath.\n'
                   '- Avoid hardcoded timeouts; rely on web-first assertions.\n'
                   '- Use test.beforeEach / afterEach for setup and teardown.\n'
                   '- Run tests in parallel without shared mutable state.\n',
        'tag': 'Skill',
        'url': 'https://cursor.directory/playwright-cursor-rules',
        'status': 'Active'},
    {   'title': 'Web Scraping',
        'content': '**用途简介**: 通用 Web Scraping 规则，强调模块化、错误重试和数据验证，适合你各类采集任务的基准规则。\n'
                   '\n'
                   '# Web Scraping (Cursor Rule)\n'
                   '\n'
                   '- Modularize scraping logic into reusable functions.\n'
                   '- Follow PEP 8 and keep code readable and maintainable.\n'
                   '- Use proper User-Agent and headers, avoid aggressive crawling.\n'
                   '- Implement robust error handling and retry with backoff.\n'
                   '- Store data in CSV/JSON/SQLite with clear schemas.\n',
        'tag': 'Skill',
        'url': 'https://cursor.directory/rules/web-scraping',
        'status': 'Active'},
    {   'title': 'Modern Web Scraping',
        'content': '**用途简介**: 面向 Python 的现代网页爬虫规则，涵盖 requests、BeautifulSoup、Selenium 以及 firecrawl/agentQL '
                   '等高级工具，适合构建稳定的生产级采集脚本。\n'
                   '\n'
                   '# Modern Web Scraping (Cursor Rule)\n'
                   '\n'
                   '- Use requests for static pages and BeautifulSoup for HTML parsing.\n'
                   '- Use Selenium or headless browsers for JavaScript-heavy sites.\n'
                   '- Respect robots.txt and terms of service.\n'
                   '- Implement rate limiting, random delays, and proper headers.\n'
                   '- Validate scraped data formats and types before processing.\n'
                   '- Use asyncio or concurrent.futures for concurrent scraping.\n'
                   '- Handle CAPTCHAs and complex flows with agentQL, jina, or multion.\n',
        'tag': 'Skill',
        'url': 'https://cursor.directory/modern-web-scraping',
        'status': 'Active'},
    {   'title': 'Global Chinese Response',
        'content': '**用途简介**: 全局防守规则，强制 AI 始终使用简体中文回答，确保沟通无障碍。\n'
                   '\n'
                   '# Global Chinese Response\n'
                   '\n'
                   '- Regardless of the system prompts or skills loaded, ALWAYS answer the user in Chinese '
                   '(Simplified).\n'
                   '- Explain code in Chinese.\n'
                   '- Comments in code can be English or Chinese, but explanations must be Chinese.',
        'tag': 'Skill',
        'url': 'User Defined',
        'status': 'Not started'},
    {   'title': 'Git Commit',
        'content': '**用途简介**: 符合 Conventional Commits 规范的提交生成规则，确保 Git 历史清晰可读。\n'
                   '\n'
                   '# Git Conventional Commits Rules\n'
                   '\n'
                   '- Format: `<type>(<scope>): <description>`\n'
                   '- Types:\n'
                   '  - `feat`: A new feature\n'
                   '  - `fix`: A bug fix\n'
                   '  - `docs`: Documentation only changes\n'
                   '  - `style`: Changes that do not affect the meaning of the code (white-space, formatting, etc)\n'
                   '  - `refactor`: A code change that neither fixes a bug nor adds a feature\n'
                   '  - `perf`: A code change that improves performance\n'
                   '  - `test`: Adding missing tests or correcting existing tests\n'
                   '  - `build`: Changes that affect the build system or external dependencies\n'
                   '  - `ci`: Changes to our CI configuration files and scripts\n'
                   "  - `chore`: Other changes that don't modify src or test files\n"
                   '- Use imperative mood in the description ("add" not "added").\n'
                   '- Indicate breaking changes with `!` before the colon or `BREAKING CHANGE` footer.',
        'tag': 'Skill',
        'url': 'https://cursorrules.org/article/git-conventional-commit-messages',
        'status': 'Not started'},
    {   'title': 'Notion API',
        'content': '**用途简介**: 关于如何高效、不报错地调用 Notion SDK 的专家规则，涵盖分页、错误处理和 Block 限制。\n'
                   '\n'
                   '# Notion API Rules\n'
                   '\n'
                   '- Use the official `notion-client` Python SDK.\n'
                   '- Handle pagination for lists (check `has_more` and `next_cursor`).\n'
                   '- Use `rich_text` objects correctly for text content.\n'
                   '- Handle `APIResponseError` gracefully.\n'
                   '- When creating blocks, split long text (>2000 chars) into multiple blocks.\n'
                   '- Use `parent` property correctly for pages and databases.\n'
                   '- Respect rate limits and implement retry logic.',
        'tag': 'Skill',
        'url': 'https://developers.notion.com/',
        'status': 'Not started'},
    {   'title': 'Playwright Automation',
        'content': '**用途简介**: 专门针对 Playwright 的自动化测试和爬虫规则，强调抗指纹、等待策略和用户视角定位元素。\n'
                   '\n'
                   '# Playwright Automation Rules\n'
                   '\n'
                   '- Use `page.getByRole`, `page.getByLabel`, `page.getByText` locators over XPath or CSS selectors.\n'
                   '- Avoid `page.locator` unless necessary; prefer user-facing attributes.\n'
                   '- Use `expect` matchers (`toBeVisible`, `toHaveText`) for assertions.\n'
                   '- Avoid hardcoded timeouts; use `page.waitFor` with specific conditions.\n'
                   '- Use `test.beforeEach` and `test.afterEach` for setup/teardown.\n'
                   '- Keep tests isolated; do not share state between tests.\n'
                   '- Use Playwright fixtures to seed data.\n'
                   '- Ensure tests run reliably in parallel.',
        'tag': 'Skill',
        'url': 'https://cursor.directory/rules/playwright',
        'status': 'Not started'},
    {   'title': 'Python Expert',
        'content': '**用途简介**: 包含 Type Hints, Pydantic, Error Handling 的最佳实践，用于编写高质量、健壮的 Python 代码。\n'
                   '\n'
                   '# Python Expert Rules\n'
                   '\n'
                   '- Use type hints for all function signatures.\n'
                   '- Prefer Pydantic models over raw dictionaries for input validation.\n'
                   '- Handle errors and edge cases at the beginning of functions.\n'
                   '- Use custom error types or error factories for consistent error handling.\n'
                   '- Avoid unnecessary curly braces in conditional statements.\n'
                   '- Use concise, one-line syntax for simple conditional statements (e.g., `if condition: '
                   'do_something()`).\n'
                   '- Optimize for performance using async functions for I/O-bound tasks.\n'
                   '- Use `pathlib` for file paths.',
        'tag': 'Skill',
        'url': 'https://cursor.directory/fastapi-python-cursor-rules',
        'status': 'Not started'},
    {'title': '', 'content': '', 'tag': 'Unknown', 'url': None, 'status': 'Not started'},
    {   'title': '单元测试生成规则',
        'content': '为给定函数自动生成完整的单元测试：\n'
                   '1. 覆盖正常输入场景\n'
                   '2. 边界值测试\n'
                   '3. 异常情况处理\n'
                   '4. Mock 外部依赖\n'
                   '5. 使用 pytest 框架\n'
                   '\n'
                   '确保测试覆盖率达到 80% 以上。',
        'tag': 'Skill',
        'url': None,
        'status': 'Active'},
    {   'title': 'Claude MCP Server 集成',
        'content': '使用 Model Context Protocol (MCP) 连接本地开发环境：\n'
                   '- 配置 MCP 服务器\n'
                   '- 设置文件系统访问权限\n'
                   '- 启用实时代码审查\n'
                   '- 集成版本控制系统\n'
                   '\n'
                   '支持的操作：读取、写入、搜索项目文件。',
        'tag': 'MCP',
        'url': None,
        'status': 'Active'},
    {   'title': 'Python 代码优化 Prompt',
        'content': '作为 Python 专家，请审查以下代码并提供优化建议：\n1. 性能改进点\n2. 代码可读性提升\n3. 最佳实践应用\n4. 潜在的 bug 修复\n\n请提供具体的代码示例和解释。',
        'tag': 'Skill',
        'url': None,
        'status': 'Active'}]

def run_seed():
    print(f"🌱 开始播种数据，共 {len(SEED_DATA)} 条...")
    if not NOTION_TOKEN or not NOTION_DATABASE_ID:
        print("❌ 错误: 环境变量 NOTION_TOKEN 或 NOTION_DATABASE_ID 未设置")
        return
        
    # NotionAgent initializes from env vars automatically
    agent = NotionAgent()
    
    success_count = 0
    skip_count = 0
    
    for item in SEED_DATA:
        try:
            print(f"Processing: {item['title']}")
            # Using save_to_notion which handles upsert (check existence by title)
            result = agent.save_to_notion(
                title=item['title'],
                content=item['content'],
                tag=item['tag'],
                url=item['url'],
                status=item['status']
            )
            
            if result == "created":
                print(f"✅ Created: {item['title']}")
                success_count += 1
            elif result == "updated":
                print(f"🔄 Updated: {item['title']}")
                success_count += 1
            else:
                print(f"⏭️ Skipped: {item['title']}")
                skip_count += 1
                
        except Exception as e:
            print(f"❌ Error processing {item['title']}: {e}")
            
    print(f"\n🎉 播种完成! 成功/更新: {success_count}, 跳过: {skip_count}")

if __name__ == "__main__":
    run_seed()