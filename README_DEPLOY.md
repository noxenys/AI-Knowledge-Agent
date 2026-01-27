# 部署指南

本项目支持 Docker 和 Docker Compose 一键部署。

## 1. 配置环境变量

复制 `.env.example` 为 `.env`，并填入以下信息：

```bash
cp .env.example .env
```

在 `.env` 文件中填入：
- `NOTION_TOKEN`: Notion 集成 Token
- `NOTION_DATABASE_ID`: Notion 数据库 ID
- `TELEGRAM_BOT_TOKEN`: Telegram Bot Token (从 @BotFather 获取)
- `TELEGRAM_CHAT_ID`: 接收通知的 Chat ID

## 2. Docker Compose 部署 (推荐)

启动服务（后台运行，重启策略为 always）：

```bash
docker-compose up -d
```

查看日志：

```bash
docker-compose logs -f
```

停止服务：

```bash
docker-compose down
```

## 3. 手动 Docker 构建

构建镜像：

```bash
docker build -t notion-agent .
```

运行容器：

```bash
docker run -d --name notion-agent --env-file .env notion-agent
```

## 功能说明

- **7x24 自动巡检**: 容器启动后会自动进入循环模式，每 24 小时执行一次。
- **通知推送**: 每次巡检结束或发生错误时，会通过 Telegram 发送通知。
- **时区**: 容器已配置为 `Asia/Shanghai`。
