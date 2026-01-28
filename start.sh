#!/bin/bash
echo "🚀 Notion Agent Container Starting..."
echo "📅 Date: $(date)"

# Ensure environment variables are loaded (if not passed via Docker env)
if [ -f .env ]; then
    echo "📄 Loading .env file..."
    export $(grep -v '^#' .env | xargs)
fi

echo "🔍 Starting Initial Inspection Loop..."
exec python agent_brain.py
