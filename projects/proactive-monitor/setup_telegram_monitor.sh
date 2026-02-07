#!/bin/bash
# Setup Telegram Alpha Monitor

echo "Setting up Telegram Alpha Monitor..."

# Install dependencies
cd /root/clawd/projects/proactive-monitor
pip3 install telethon aiofiles

# Create .env template
cat > .env << 'EOF'
# Get these from https://my.telegram.org/apps
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash

# Your bot token (from @BotFather)
TELEGRAM_BOT_TOKEN=your_bot_token
EOF

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Get API ID and Hash from https://my.telegram.org/apps"
echo "2. Edit .env file with your credentials"
echo "3. Add @dcawatcher and other channels to monitor"
echo "4. Run: python3 telegram_alpha_monitor.py"
echo "5. Message your bot /start to get your chat ID"
echo "6. Add chat ID to config, restart"
