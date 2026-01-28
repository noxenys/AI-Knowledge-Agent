import os
import sys
from agent_notion import NotionAgent

# -----------------------------------------------------------------------------
# Content Definitions
# -----------------------------------------------------------------------------

CONTENT_AGENT_BROWSER = """
# 中文功能深度解析
本技能详细拆解 Vercel Labs 推出的 `agent-browser` 工具。核心理念是**简化工具链**，不使用 17 个独立工具（点击、输入、滚动等），而是通过一个统一的 CLI 和 **Snapshot + Refs** 系统。
- **Snapshot (@e1)**: 获取页面的可交互元素树，自动分配引用 ID（如 `@e1`, `@e2`）。
- **Unified Interaction**: 所有操作（点击、填充）都基于这些引用 ID，极大降低了 LLM 的上下文消耗和幻觉风险。
- **Self-Correction**: 结合 "Ralph Wiggum Loop" 思想，简化决策空间，让 Agent 更专注于任务流而非底层 DOM 操作。

---

# Agent-Browser Specialist

## Core Philosophy
Vercel's `agent-browser` reduces complexity by using a single CLI tool instead of multiple granular tools. The key innovation is the **Snapshot System** which assigns stable reference IDs (refs) to interactive elements.

## Key Commands
- **Navigate**: `agent-browser open <url>`
- **Analyze**: `agent-browser snapshot -i` (Returns interactive elements with refs like `@e1`, `@e2`)
- **Interact**: 
  - `agent-browser click @e1`
  - `agent-browser fill @e2 "user@example.com"`
  - `agent-browser get text @e1`

## Workflow Example
1. **Open Page**: Start the session.
   ```bash
   agent-browser open https://example.com
   ```
2. **Get Refs**: Request a snapshot.
   ```bash
   agent-browser snapshot -i
   # Output:
   # - button "Submit" [ref=e1]
   # - input "Email" [ref=e2]
   ```
3. **Action**: Use the ref to interact.
   ```bash
   agent-browser fill @e2 "hello@vercel.com"
   agent-browser click @e1
   ```

## Best Practices
- **Prefer `-i` flag**: Use `snapshot -i` to get only interactive elements, saving token context.
- **Verification**: Use `agent-browser get text @e1` to verify state changes after actions.
- **Global Link**: Install globally via `pnpm link --global` for system-wide agent access.
"""

CONTENT_STRIPE_STEALTH = """
# 中文功能深度解析
本技能聚焦于 Stripe 支付环境的高级测试与安全攻防（Red Teaming）。
- **Iframe 穿透**: 解析攻击者如何利用 Overlay 技术覆盖 Stripe 官方 Iframe，劫持输入数据。
- **Card Testing**: 详解 Stripe 的反欺诈机制（Rate Limit, CAPTCHA, ML Models）以及测试环境下的正确模拟姿势。
- **Stealth Strategy**: 在自动化测试中，如何避免被判定为恶意 Bot（合理使用 Test Mode Keys, 模拟真实用户行为）。

---

# Stripe Stealth Master

## Iframe Security & Penetration
Stripe uses `<iframe>` elements to isolate PCI-DSS sensitive data.
- **The Attack Vector**: "Overlay Attacks". Attackers inject pixel-perfect fake forms *over* the legitimate Stripe Iframe.
- **Mechanism**: The malicious script captures keystrokes before they reach the secure Iframe.
- **Defense**: Implement Content Security Policy (CSP) and monitor for unexpected DOM mutations around payment forms.

## Testing Card Numbers (Test Mode Only)
Do NOT use real cards in test mode. Use Stripe's reserved test numbers:
- **Visa**: `4242 4242 4242 4242`
- **Mastercard**: `5555 5555 5555 4444`
- **Amex**: `3782 822463 10005`
- **Non-Card Payment**: Use `pm_card_visa` objects instead of raw numbers in API calls.

## Anti-Detection & Rate Limiting
Stripe employs sophisticated ML models to detect "Card Testing" attacks (fraudsters validating stolen cards).
- **Triggers**: High velocity of declines, sequential card numbers, single IP bursts.
- **Bypass for Testing**:
  - Ensure you are strictly using **Test Mode API Keys** (`sk_test_...`).
  - Do not mix Live and Test keys.
  - Implement exponential backoff in your automation scripts if you hit rate limits (`429 Too Many Requests`).
"""

CONTENT_PYTHON_AUTOMATION = """
# 中文功能深度解析
本技能总结 Python `asyncio` 在生产环境下的最佳实践，特别是针对高并发网络 I/O 任务。
- **Event Loop**: 理解事件循环机制，严禁在 Async 函数中调用 Blocking IO（如 `time.sleep` 或同步 `requests`）。
- **Concurrency**: 使用 `asyncio.gather` 和 `asyncio.create_task` 实现真正的并发执行。
- **Error Handling**: 异步任务中的异常必须被捕获或 await，否则会被“吞掉”或导致未预期的行为。

---

# Python Automation Pro

## Core Rules for Production Asyncio
1. **Never Block the Loop**: 
   - ❌ `time.sleep(1)` -> Stops the entire world.
   - ✅ `await asyncio.sleep(1)` -> Yields control to other tasks.
   - ❌ `requests.get()` -> Blocking.
   - ✅ `httpx.get()` or `aiohttp` -> Non-blocking.

## Task Management
- **Fire and Forget? No.**: Always keep a reference to your tasks to prevent garbage collection mid-execution.
  ```python
  # Bad
  asyncio.create_task(my_coro())
  
  # Good
  task = asyncio.create_task(my_coro())
  background_tasks.add(task)
  task.add_done_callback(background_tasks.discard)
  ```

## Concurrent Execution
Use `gather` for batch processing:
```python
async def main():
    urls = ["http://a.com", "http://b.com"]
    # Run fetch concurrently
    results = await asyncio.gather(*(fetch(url) for url in urls))
```

## Exception Handling
If a task fails in `gather`, it can cancel others depending on `return_exceptions`.
- `return_exceptions=True`: Returns the Exception object instead of raising it, allowing other tasks to finish.
"""

# -----------------------------------------------------------------------------
# Main Execution
# -----------------------------------------------------------------------------

def main():
    agent = NotionAgent()
    
    tasks = [
        {
            "title": "Agent-Browser Specialist",
            "content": CONTENT_AGENT_BROWSER,
            "url": "https://github.com/vercel-labs/agent-browser",
            "tag": "Skill"
        },
        {
            "title": "Stripe Stealth Master",
            "content": CONTENT_STRIPE_STEALTH,
            "url": "https://docs.stripe.com/testing",
            "tag": "Skill"
        },
        {
            "title": "Python Automation Pro",
            "content": CONTENT_PYTHON_AUTOMATION,
            "url": "https://docs.python.org/3/library/asyncio.html",
            "tag": "Skill"
        }
    ]
    
    print("🚀 Starting Precision Import...")
    for task in tasks:
        print(f"\nProcessing: {task['title']}")
        try:
            agent.save_to_notion(
                title=task["title"],
                content=task["content"],
                tag=task["tag"],
                url=task["url"],
                status="Active"
            )
        except Exception as e:
            print(f"❌ Error processing {task['title']}: {e}")
    print("\n✨ All tasks processed.")

if __name__ == "__main__":
    main()
