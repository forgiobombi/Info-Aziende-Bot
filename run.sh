#!/bin/bash

# Info Aziende Bot - Startup Script

echo "🚀 Starting Info Aziende Bot..."
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "Please copy .env.example to .env and configure your tokens."
    echo ""
    echo "Run: cp .env.example .env"
    echo "Then edit .env with your Discord and OpenAPI tokens."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed!"
    echo "Please install Python 3.8 or higher."
    exit 1
fi

# Check if requirements are installed
if ! python3 -c "import discord" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    echo ""
fi

# Run the bot
echo "✅ Starting bot..."
python3 bot.py
