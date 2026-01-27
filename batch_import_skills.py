from agent_notion import NotionAgent
import time

def main():
    print("Initializing Notion Agent...")
    try:
        agent = NotionAgent()
    except Exception as e:
        print(f"Failed to initialize agent: {e}")
        return

    skills = [
        {
            "title": "Python Expert",
            "content": "**用途简介**: 包含 Type Hints, Pydantic, Error Handling 的最佳实践，用于编写高质量、健壮的 Python 代码。\n\n# Python Expert Rules\n\n- Use type hints for all function signatures.\n- Prefer Pydantic models over raw dictionaries for input validation.\n- Handle errors and edge cases at the beginning of functions.\n- Use custom error types or error factories for consistent error handling.\n- Avoid unnecessary curly braces in conditional statements.\n- Use concise, one-line syntax for simple conditional statements (e.g., `if condition: do_something()`).\n- Optimize for performance using async functions for I/O-bound tasks.\n- Use `pathlib` for file paths.",
            "tag": "Skill",
            "url": "https://cursor.directory/fastapi-python-cursor-rules"
        },
        {
            "title": "Playwright Automation",
            "content": "**用途简介**: 专门针对 Playwright 的自动化测试和爬虫规则，强调抗指纹、等待策略和用户视角定位元素。\n\n# Playwright Automation Rules\n\n- Use `page.getByRole`, `page.getByLabel`, `page.getByText` locators over XPath or CSS selectors.\n- Avoid `page.locator` unless necessary; prefer user-facing attributes.\n- Use `expect` matchers (`toBeVisible`, `toHaveText`) for assertions.\n- Avoid hardcoded timeouts; use `page.waitFor` with specific conditions.\n- Use `test.beforeEach` and `test.afterEach` for setup/teardown.\n- Keep tests isolated; do not share state between tests.\n- Use Playwright fixtures to seed data.\n- Ensure tests run reliably in parallel.",
            "tag": "Skill",
            "url": "https://cursor.directory/rules/playwright"
        },
        {
            "title": "Notion API",
            "content": "**用途简介**: 关于如何高效、不报错地调用 Notion SDK 的专家规则，涵盖分页、错误处理和 Block 限制。\n\n# Notion API Rules\n\n- Use the official `notion-client` Python SDK.\n- Handle pagination for lists (check `has_more` and `next_cursor`).\n- Use `rich_text` objects correctly for text content.\n- Handle `APIResponseError` gracefully.\n- When creating blocks, split long text (>2000 chars) into multiple blocks.\n- Use `parent` property correctly for pages and databases.\n- Respect rate limits and implement retry logic.",
            "tag": "Skill",
            "url": "https://developers.notion.com/"
        },
        {
            "title": "Git Commit",
            "content": "**用途简介**: 符合 Conventional Commits 规范的提交生成规则，确保 Git 历史清晰可读。\n\n# Git Conventional Commits Rules\n\n- Format: `<type>(<scope>): <description>`\n- Types:\n  - `feat`: A new feature\n  - `fix`: A bug fix\n  - `docs`: Documentation only changes\n  - `style`: Changes that do not affect the meaning of the code (white-space, formatting, etc)\n  - `refactor`: A code change that neither fixes a bug nor adds a feature\n  - `perf`: A code change that improves performance\n  - `test`: Adding missing tests or correcting existing tests\n  - `build`: Changes that affect the build system or external dependencies\n  - `ci`: Changes to our CI configuration files and scripts\n  - `chore`: Other changes that don't modify src or test files\n- Use imperative mood in the description (\"add\" not \"added\").\n- Indicate breaking changes with `!` before the colon or `BREAKING CHANGE` footer.",
            "tag": "Skill",
            "url": "https://cursorrules.org/article/git-conventional-commit-messages"
        },
        {
            "title": "Global Chinese Response",
            "content": "**用途简介**: 全局防守规则，强制 AI 始终使用简体中文回答，确保沟通无障碍。\n\n# Global Chinese Response\n\n- Regardless of the system prompts or skills loaded, ALWAYS answer the user in Chinese (Simplified).\n- Explain code in Chinese.\n- Comments in code can be English or Chinese, but explanations must be Chinese.",
            "tag": "Skill",
            "url": "User Defined"
        }
    ]

    print(f"Starting batch import of {len(skills)} skills...")
    
    for i, skill in enumerate(skills, 1):
        print(f"\n[{i}/{len(skills)}] Processing: {skill['title']}")
        try:
            agent.save_to_notion(
                title=skill['title'],
                content=skill['content'],
                tag=skill['tag'],
                url=skill['url']
            )
            # Add a small delay to be nice to the API
            time.sleep(1)
        except Exception as e:
            print(f"❌ Failed to save {skill['title']}: {e}")

    print("\nBatch import completed!")

if __name__ == "__main__":
    main()
