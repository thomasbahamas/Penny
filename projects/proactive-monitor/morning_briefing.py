#!/usr/bin/env python3
"""Morning briefing - 7:00 AM PST daily digest"""
import subprocess
import json
import os
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

# Weather fetch
weather = subprocess.run(
    ['curl', '-s', 'wttr.in/Los+Angeles?format=3'],
    capture_output=True, text=True
).stdout.strip() or "Weather unavailable"

# Header
BRIEFING.append("🌅 GOOD MORNING THOMAS")
BRIEFING.append(f"📅 {datetime.now().strftime('%A, %B %d, %Y - 7:00 AM PST')}")
BRIEFING.append(f"🌤️  {weather}")
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

# Overnight Work Summary (from overnight agent runs)
try:
    # Check for overnight agent activity logs
    overnight_log = '/tmp/overnight_work.log'
    if os.path.exists(overnight_log):
        with open(overnight_log, 'r') as f:
            content = f.read()
            if content.strip():
                add_section("🌙 WHAT I BUILT WHILE YOU SLEPT", content[:1000])
    else:
        add_section("🌙 OVERNIGHT STATUS", "No overnight work recorded yet. First run tonight at 11pm!")
except:
    pass

# Overnight Activity (from mission control log)
try:
    with open('/root/clawd/mission-control/activity.jsonl', 'r') as f:
        lines = f.readlines()
        recent = [json.loads(l) for l in lines[-10:] if l.strip()]
        if recent:
            activity_text = "System activity:\n"
            for item in recent[-5:]:
                activity_text += f"  • {item['type']}: {item.get('details', 'Task completed')}\n"
            add_section("⚙️ SYSTEM ACTIVITY", activity_text)
except:
    pass

# Today's Focus - Pull from todo.md
try:
    with open('/root/clawd/tasks/todo.md', 'r') as f:
        todo_content = f.read()
        # Extract incomplete tasks
        focus_items = []
        in_progress = False
        for line in todo_content.split('\n'):
            if '## In Progress' in line:
                in_progress = True
            elif '## Backlog' in line or '## Completed' in line:
                in_progress = False
            elif in_progress and line.strip().startswith('- [ ]'):
                task = line.replace('- [ ]', '').strip()
                focus_items.append(task)
        
        if focus_items:
            focus_text = "\n".join([f"{i+1}. {t}" for i, t in enumerate(focus_items[:5])])
        else:
            focus_text = "1. Review overnight work above\n2. Set today's priorities\n3. Check SKRmaxi dashboard"
except:
    focus_text = "1. Review overnight work above\n2. Set today's priorities\n3. Check SKRmaxi dashboard"

BRIEFING.append("\n" + "="*60)
BRIEFING.append("🎯 TODAY'S FOCUS")
BRIEFING.append("="*60)
BRIEFING.append(f"""
{focus_text}

💡 Reply with what you want me to prioritize and I'll get to work!
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
