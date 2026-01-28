# ☁️ 云端部署指南 (Cloud Deployment Guide)

本指南针对 **Zeabur** 和 **Hugging Face Spaces** 等容器化平台，旨在实现“零本地运维，Git 驱动部署”。

## 1. 🚀 推荐平台：Zeabur
Zeabur 是最适合本项目的部署平台，它能自动识别 `Dockerfile` 并构建，且支持国内访问速度快。

### 部署步骤
1.  **Fork/Push 代码**: 确保你的 GitHub 仓库中有本项目的最新代码。
2.  **注册/登录 Zeabur**: 访问 [Zeabur Dashboard](https://dash.zeabur.com/)，使用 GitHub 账号登录。
3.  **新建项目**: 点击 "Create Project" -> "New Service" -> "GitHub"。
4.  **选择仓库**: 选择 `AI-Knowledge-Agent` 仓库。
5.  **等待构建**: Zeabur 会自动读取根目录的 `Dockerfile` 进行构建。

### 环境变量配置 (Environment Variables)
在 Zeabur 项目的 "Settings" -> "Variables" 中添加以下变量：

| 变量名 | 说明 | 获取方式 |
| :--- | :--- | :--- |
| `NOTION_TOKEN` | Notion 集成令牌 | [Notion Integrations](https://www.notion.so/my-integrations) |
| `NOTION_DATABASE_ID` | 知识库 ID | Notion 数据库 URL 中 `?v=` 之前的那串字符 |
| `TELEGRAM_BOT_TOKEN` | 机器人 Token | 向 [@BotFather](https://t.me/BotFather) 发送 `/newbot` 获取 |
| `TELEGRAM_CHAT_ID` | 你的 Chat ID | 向 [@userinfobot](https://t.me/userinfobot) 发送任意消息获取 |
| `TZ` | 时区 | 填写 `Asia/Shanghai` |

---

## 2. 🤗 备选方案：Hugging Face Spaces
适合白嫖计算资源，但需注意休眠机制。

### 部署步骤
1.  **新建 Space**: 在 HF 创建新 Space，SDK 选择 **Docker**，Template 选择 **Blank**。
2.  **配置 Secrets**: 在 Space 的 "Settings" -> "Repository secrets" 中添加上述 4 个环境变量（`NOTION_TOKEN`, `DATABASE_ID` 等）。
3.  **同步代码**:
    *   **方式 A (推荐)**: 使用 GitHub Actions 自动同步（见下文 `deploy.sh`）。
    *   **方式 B**: 直接将代码 Push 到 HF 提供的 Git 仓库地址。

---

## 3. 🔄 自动化部署脚本 (`deploy.sh`)
本项目提供了一键部署脚本，实质是触发 Git Push，进而触发云端的自动构建。

**使用方法**:
在终端运行：
```bash
./deploy.sh
```
该脚本会自动添加所有变更、提交代码并推送到 GitHub。Zeabur/HF 检测到 Push 后会自动重新部署。

---

## 4. 📱 远程监控与调试
无需 SSH 登录容器，通过 Telegram 即可掌握运行状态。

*   **启动通知**: 容器启动时会发送 "Agent Brain initialized"。
*   **巡检报告**: 每天自动发送 "✅ 新增: X | 🔄 更新: Y"。
*   **错误报警**: 
    *   脚本崩溃会发送 `🚨 紧急预警`。
    *   **新增**: 代码中集成了 `logging` 模块，所有 `ERROR` 级别的日志会实时推送到 Telegram。
