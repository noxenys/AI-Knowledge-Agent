# 部署指南

本项目已配置 GitHub Actions 自动构建 Docker 镜像，支持直接拉取运行，无需本地构建。

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

本项目默认使用 GitHub Container Registry (GHCR) 上的预构建镜像。

### 启动服务

直接运行以下命令，Docker 会自动拉取最新镜像并启动：

```bash
docker-compose up -d
```

### 更新镜像

如果代码仓库有更新，执行以下命令获取最新版本：

```bash
docker-compose pull
docker-compose up -d
```

### 常用命令

查看日志：
```bash
docker-compose logs -f
```

停止服务：
```bash
docker-compose down
```

## 3. 手动 Docker 构建 (仅开发调试)

如果你想修改代码并在本地测试，可以取消 `docker-compose.yml` 中 `image: ...` 的注释，并启用 `build: .`。

或者手动构建：

```bash
docker build -t notion-agent .
docker run -d --name notion-agent --env-file .env notion-agent
```

## 功能说明

- **7x24 自动巡检**: 容器启动后会自动进入循环模式，每 24 小时执行一次。
- **通知推送**: 每次巡检结束或发生错误时，会通过 Telegram 发送通知。
- **时区**: 容器已配置为 `Asia/Shanghai`。
