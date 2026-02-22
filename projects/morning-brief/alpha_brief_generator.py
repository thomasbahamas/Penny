#!/usr/bin/env python3
"""
THOMAS ALPHA BRIEF GENERATOR
Runs at 5:30am PST daily
Only actionable signals. No noise.
"""

import json
from datetime import datetime

THRESHOLDS = {
    "dip_buy": -0.15,      # 15% dip = potential buy
    "pump_sell": 0.25,     # 25% pump = consider taking profit
    "portfolio_drift": 0.05 # 5% drift = rebalance alert
}

WATCHLIST = [
    # Crypto
    "SOL", "ZEC", "HYPE", "ORE", "MET", "SKR", "MONAD",
    "TGB", "JUP", "BONK", "HOSICO",
    # Stocks (for dips)
    "GOLD", "GOOGL", "TSLA", "RIVN"
]

AIRDROPS_TO_MONITOR = [
    "Hyperliquid",
    "Kamino V2",
    "Drift V2",
    "Jupiter",
]

def generate_brief():
    now = datetime.now()
    day_name = now.strftime("%A")
    
    brief = f"""🌅 THOMAS ALPHA BRIEF | {now.strftime('%B %d, %Y')} | {day_name}

⏰ TIME CHECK: 5:30am PST | Kids leave: 6:40am

📊 OVERNIGHT MARKET (What moved >10%?)
• [Auto-populated from Birdeye/Coingecko]
• [Highlight any watchlist moves]

💰 YOUR PORTFOLIO SIGNALS
• BONK: [price] [change] → [HOLD/SELL/BUY]
• SOL ecosystem: [status]
• Cash position: [ready to deploy?]
• Drift >5%? [REBALANCE ALERT/Nominal]

🎯 TODAY'S ONE DECISION
[ ] Buy the dip on [asset]?
[ ] Take profit on [asset]?
[ ] Farm [airdrop]?
[ ] Hold & wait

🪂 AIRDROP ALERTS
• [Any new drops worth farming?]
• [Time commitment estimate]

📅 FAMILY/STAFF TODAY
• Kids schedule: [from calendar]
• Wife schedule: [from calendar]
• Your focus window: 5:30-6:40am

🎬 CONTENT IDEA
[If overnight inspiration struck]

⏰ HARD STOP: 6:40am → Family mode

Reply with your ONE decision. I execute.
"""
    return brief

if __name__ == "__main__":
    print(generate_brief())
