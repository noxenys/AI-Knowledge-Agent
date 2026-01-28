# AI-Knowledge-Agent

全自动 Notion 知识库维护工具。监控链接健康状态，自动填充网页内容，定期全量备份。

## 主要功能

### 1. 自动内容抓取
监控 Notion 中仅包含 URL 的页面，自动爬取网页正文并转换为 Markdown 填充至 Content 字段。支持长文本自动分块。

### 2. 链接健康检查与自愈 (Self-Healing)
定期巡检数据库中的 Source URL：
- **存活检测**：自动识别 404/5xx 错误。
- **智能修复**：发现失效链接时，自动通过 DuckDuckGo 搜索项目名称（针对 GitHub 仓库改名或迁移场景），尝试匹配新的有效地址。
- **状态管理**：修复成功自动更新链接；无法修复则标记 Status 为 `Broken`。

### 3. 数据备份与灾备
- **每日备份**：自动导出全量数据为 JSON 和 Markdown 格式至 `backups/` 目录。
- **自动清理**：系统自动保留最近 30 份备份文件（含 JSON/Markdown/Script），过期文件自动删除，防止磁盘空间耗尽。
- **一键重建**：每次备份同时生成 `data_seed_latest.py` 脚本，可直接运行该脚本将数据重新写入新的 Notion 数据库，实现快速恢复。

### 4. 外部资源集成
内置爬虫模块 (`discover_new_rules`)，支持从 cursor.directory 等源检索特定技术栈（如 Stripe, Automation）的最新规则并存入知识库。

---

## 快速开始

### 1. 环境配置

复制配置文件：
```bash
cp .env.example .env
```

配置 `.env`:
*   `NOTION_TOKEN`: Notion Integration Token
*   `NOTION_DATABASE_ID`: 目标 Database ID
*   `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID`: (可选) 用于接收巡检报告和错误报警

### 2. 运行

**Docker Compose (推荐)**:
已包含完整运行环境，支持自动重启。
```bash
docker-compose up -d
```

**本地运行**:
```bash
pip install -r requirements.txt
python agent_brain.py
```

---

## 项目结构

### 核心服务

| 文件 | 说明 |
|-----|------|
| `agent_brain.py` | **主控程序**。负责任务调度、巡检循环、自愈逻辑决策及通知发送。 |
| `agent_notion.py` | **Notion 交互层**。封装 Notion API，实现 MD5 内容去重、长文本分块和重试机制。 |
| `backup_data.py` | **备份服务**。负责全量数据导出及 Seed 恢复脚本生成。 |

### 辅助工具

| 文件 | 说明 |
|-----|------|
| `sync_to_trae.py` | 将所有 Active 状态的 Skills 导出为单一文本文件，便于分发或 LLM 上下文使用。 |
| `remove_duplicates.py` | 数据库清理工具。基于 Title 分组，保留内容最丰富且创建时间最早的记录。 |
| `update_schema.py` | 数据库 Schema 校验与修复工具。确保 Status、Type 等字段类型符合系统要求。 |

### 批量导入脚本

| 文件 | 说明 |
|-----|------|
| `batch_import_skills.py` | 导入基础技能集（如 Python, Git 规范）。 |
| `bulk_import_advanced_skills.py` | 导入高级技能集（涵盖 Web Scraping, MCP Servers）。 |
| `core_assets_import.py` | 导入核心资产提示词（Prompts）。 |
| `precision_import.py` | 导入带详细说明的精选技能。 |

---

## 逻辑架构

系统采用**纯同步**架构设计以确保稳定性，核心流程如下：

1.  **Iterate**: `agent_brain` 遍历 Notion 数据库页面。
2.  **Fetch**: 请求 Source URL 获取最新内容（支持重试）。
3.  **Healing**: 若遇到 404，触发 `search_for_alternative_url` 进行模糊搜索匹配。
4.  **Dedup**: 计算远程内容 MD5，与 Notion 本地内容 MD5 对比。
5.  **Upsert**: 仅在内容变更（MD5 不一致）或 URL 修复时调用 `agent_notion` 写入数据。

## License

MIT
