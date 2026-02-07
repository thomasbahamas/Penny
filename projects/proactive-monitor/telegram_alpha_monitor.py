#!/usr/bin/env python3
"""Telegram Channel Alpha Monitor - watches crypto news channels"""
import asyncio
import json
import os
from datetime import datetime
from telethon import TelegramClient, events
from telethon.tl.types import Channel

# Config
SESSION_NAME = "alpha_monitor"
API_ID = os.environ.get("TELEGRAM_API_ID", "YOUR_API_ID")
API_HASH = os.environ.get("TELEGRAM_API_HASH", "YOUR_API_HASH")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN")

# Channels to monitor (add more as needed)
MONITORED_CHANNELS = [
    "dcawatcher",  # @dcawatcher
    # Add more:
    # "coindesk",
    # "Cointelegraph", 
    # "theblockcrypto",
    # "decryptco",
]

# Keywords to hunt
ALPHA_KEYWORDS = {
    "urgent": ["exploit", "hack", "rug", "drain", "emergency", "critical"],
    "solana": ["solana", "jupiter", "jito", "drift", "kamino", "marginfi", 
               "ore", "bonk", "wif", "firedancer", "x402", "alpenglow", "bam"],
    "alerts": ["partnership", "raise", "funding", "airdrop", "listing", 
               "binance", "coinbase", "sec", "etf"],
    "tech": ["depin", "rwa", "tokenization", "ai", "infra"]
}

USER_CHAT_ID = None  # Will be set on first interaction

def scan_message(text, channel_name):
    """Scan message for alpha"""
    if not text:
        return []
    
    text_lower = text.lower()
    hits = []
    
    for category, words in ALPHA_KEYWORDS.items():
        for word in words:
            if word in text_lower:
                hits.append({
                    'word': word,
                    'category': category,
                    'channel': channel_name
                })
    
    return hits

async def send_alert(client, hits, message_text, channel_name, message_link):
    """Send alert to user"""
    global USER_CHAT_ID
    
    if not USER_CHAT_ID:
        print("User chat ID not set - set it in config")
        return
    
    # Build alert
    categories = set(h['category'] for h in hits)
    
    if 'urgent' in categories:
        emoji = "🚨 URGENT"
    elif 'solana' in categories:
        emoji = "🌊 SOLANA ALPHA"
    elif 'alerts' in categories:
        emoji = "🔔 ALERT"
    else:
        emoji = "📊 ALPHA"
    
    # Truncate message
    preview = message_text[:200] + "..." if len(message_text) > 200 else message_text
    
    # Alert text
    alert = f"""
{emoji} from @{channel_name}

{preview}

🔍 Detected: {', '.join(set(h['word'] for h in hits))}
🔗 {message_link}
"""
    
    try:
        await client.send_message(USER_CHAT_ID, alert)
        print(f"Alert sent: {hits[0]['word']} from @{channel_name}")
    except Exception as e:
        print(f"Failed to send alert: {e}")

async def main():
    """Main monitor loop"""
    
    # Check config
    if API_ID == "YOUR_API_ID":
        print("ERROR: Set TELEGRAM_API_ID and TELEGRAM_API_HASH env vars")
        print("Get them from https://my.telegram.org/apps")
        return
    
    if not USER_CHAT_ID:
        print("WARNING: Set USER_CHAT_ID to receive alerts")
        print("Your chat ID will be printed when you message the bot")
    
    # Initialize client
    client = TelegramClient(SESSION_NAME, int(API_ID), API_HASH)
    
    @client.on(events.NewMessage(chats=MONITORED_CHANNELS))
    async def handler(event):
        """Handle new messages"""
        try:
            # Get message details
            message = event.message
            text = message.text or message.caption or ""
            
            if not text:
                return
            
            # Get channel info
            chat = await event.get_chat()
            channel_name = chat.username if hasattr(chat, 'username') and chat.username else "unknown"
            
            # Scan for alpha
            hits = scan_message(text, channel_name)
            
            if hits:
                # Build message link
                message_link = f"https://t.me/{channel_name}/{message.id}"
                
                # Log
                print(f"[{datetime.now().strftime('%H:%M')}] Alpha in @{channel_name}: {[h['word'] for h in hits]}")
                
                # Send alert
                await send_alert(client, hits, text, channel_name, message_link)
                
                # Save to activity log
                await log_activity(hits, channel_name)
        except Exception as e:
            print(f"Error processing message: {e}")
    
    @client.on(events.NewMessage(pattern='/start'))
    async def start_handler(event):
        """Handle /start to capture user chat ID"""
        global USER_CHAT_ID
        USER_CHAT_ID = event.chat_id
        await event.reply(f"Alpha monitor activated!\nYour chat ID: {USER_CHAT_ID}\n\nAdd this to config and restart.")
        print(f"User chat ID captured: {USER_CHAT_ID}")
    
    # Start
    print("=" * 60)
    print("ALPHA MONITOR STARTED")
    print(f"Monitoring: {', '.join(MONITORED_CHANNELS)}")
    print("=" * 60)
    
    await client.start(bot_token=BOT_TOKEN if BOT_TOKEN != "YOUR_BOT_TOKEN" else None)
    await client.run_until_disconnected()

async def log_activity(hits, channel):
    """Log to activity file"""
    import aiofiles
    
    os.makedirs("/root/clawd/mission-control", exist_ok=True)
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "type": "telegram_alpha",
        "words": [h['word'] for h in hits],
        "channel": channel
    }
    
    try:
        async with aiofiles.open("/root/clawd/mission-control/activity.jsonl", "a") as f:
            await f.write(json.dumps(entry) + "\n")
    except:
        pass

if __name__ == "__main__":
    asyncio.run(main())
