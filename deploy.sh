#!/bin/bash

# Cloud Deployment Trigger Script
# Usage: ./deploy.sh [commit_message]

echo "🚀 Preparing to deploy to Cloud (via GitHub Actions/Webhooks)..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Error: Not a git repository."
    exit 1
fi

# Add all changes
echo "📦 Staging changes..."
git add .

# Commit
MSG=${1:-"Update: Auto-deployment trigger via deploy.sh"}
echo "📝 Committing with message: '$MSG'"
git commit -m "$MSG"

# Push
echo "☁️  Pushing to GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo "✅ Success! Code pushed to GitHub."
    echo "👀 Watch your cloud dashboard (Zeabur/HuggingFace) for build progress."
    echo "📱 You will receive a Telegram notification when the agent restarts."
else
    echo "❌ Error: Git push failed."
fi
