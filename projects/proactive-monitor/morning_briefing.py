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

# Save to file for Telegram bot to pick up
with open('/tmp/morning_briefing.txt', 'w') as f:
    f.write(output)
