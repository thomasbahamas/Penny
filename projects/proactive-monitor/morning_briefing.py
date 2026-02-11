#!/usr/bin/env python3
"""Morning briefing - 5:30 AM PST daily digest"""
import subprocess
import json
from datetime import datetime

BRIEFING = []

def add_section(title, content):
    BRIEFING.append(f"\n{'='*60}")
    BRIEFING.append(f"📌 {title}")
    BRIEFING.append('='*60)
    BRIEFING.append(content)

def run_scanner(script_path):
    try:
        result = subprocess.run(
            ['python3', script_path],
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.stdout
    except:
        return "Scanner unavailable"

# Header
BRIEFING.append("🌅 GOOD MORNING THOMAS")
BRIEFING.append(f"📅 {datetime.now().strftime('%A, %B %d, %Y - 5:30 AM PST')}")
BRIEFING.append("🤖 Your overnight briefing from Penny")

# Trading Signals
signals = run_scanner('/root/clawd/projects/trading-signals/signal_scanner.py')
add_section("🎯 TRADING SIGNALS", signals)

# Solana Ecosystem
solana = run_scanner('/root/clawd/projects/proactive-monitor/solana_scanner.py')
add_section("🌊 SOLANA ECOSYSTEM", solana)

# SolanaFloor Latest
solanafloor = run_scanner('/root/clawd/projects/proactive-monitor/solanafloor_scraper.py')
add_section("🏛️ SOLANAFLOOR INSIGHTS", solanafloor)

# SKRmaxi Status Check
skrmaxi = run_scanner('/root/clawd/projects/proactive-monitor/skrmaxi_monitor.py')
add_section("📱 SKRMAXI MONITOR", skrmaxi)

# BTC Bottom Check
btc = run_scanner('/root/clawd/projects/proactive-monitor/btc_bottom.py')
add_section("🪙 BITCOIN STATUS", btc)

# Overnight Activity (from mission control log)
try:
    with open('/root/clawd/mission-control/activity.jsonl', 'r') as f:
        lines = f.readlines()
        recent = [json.loads(l) for l in lines[-10:] if l.strip()]
        if recent:
            activity_text = "Recent activity:\n"
            for item in recent[-5:]:
                activity_text += f"  • {item['type']}: {item.get('details', 'Task completed')}\n"
            add_section("🤖 OVERNIGHT ACTIVITY", activity_text)
except:
    pass

# Today's Focus
BRIEFING.append("\n" + "="*60)
BRIEFING.append("🎯 TODAY'S FOCUS")
BRIEFING.append("="*60)
BRIEFING.append("""
1. Check tagged messages from EU/EC team
2. Review any urgent trading signals above
3. Tackle your #todo list (paste here when ready)
4. Daily standup prep

Reply with your todo list and I'll organize it!
""")

# Print final briefing
output = "\n".join(BRIEFING)
print(output)

# Save to file
with open('/tmp/morning_briefing.txt', 'w') as f:
    f.write(output)

# Send to Telegram
import os
import requests
import os

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "1123064049")  # Thomas's ID

if not TELEGRAM_BOT_TOKEN:
    print("⚠️  TELEGRAM_BOT_TOKEN not set - skipping Telegram send")
    TELEGRAM_BOT_TOKEN = "dummy_token_for_testing"

def send_telegram_message(text):
    """Send message to Telegram"""
    try:
        # Split long messages
        max_length = 4000
        chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]
        
        for chunk in chunks:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            data = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": chunk,
                "parse_mode": "HTML"
            }
            resp = requests.post(url, json=data, timeout=10)
            if not resp.json().get("ok"):
                print(f"Telegram error: {resp.json()}")
    except Exception as e:
        print(f"Failed to send Telegram: {e}")

# Send the briefing
send_telegram_message(output.replace('=', '━').replace('📌', '▸'))
print("\n📤 Briefing sent to Telegram!")
