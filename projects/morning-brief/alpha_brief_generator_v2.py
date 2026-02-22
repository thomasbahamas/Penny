#!/usr/bin/env python3
"""
THOMAS ALPHA BRIEF GENERATOR v2.0 — WITH OPTIMISM + CONTENT IDEAS
Runs at 5:30am PST daily
Actionable signals + momentum + opportunity sizing + video topics
"""

import json
from datetime import datetime

THRESHOLDS = {
    "dip_buy": -0.15,      # 15% dip = potential buy
    "pump_sell": 0.25,     # 25% pump = consider taking profit
    "portfolio_drift": 0.05 # 5% drift = rebalance alert
}

WATCHLIST = {
    # Crypto
    "SOL": {"type": "crypto", "conviction": 9},
    "ZEC": {"type": "crypto", "conviction": 6},
    "HYPE": {"type": "crypto", "conviction": 8},
    "ORE": {"type": "crypto", "conviction": 5},
    "MET": {"type": "crypto", "conviction": 7},
    "SKR": {"type": "crypto", "conviction": 8},
    "MONAD": {"type": "crypto", "conviction": 6},
    "TGB": {"type": "crypto", "conviction": 5},
    "JUP": {"type": "crypto", "conviction": 7},
    "BONK": {"type": "crypto", "conviction": 4, "re_entry": True},
    "HOSICO": {"type": "crypto", "conviction": 5},
    # Stocks
    "GOLD": {"type": "stock", "conviction": 6},
    "GOOGL": {"type": "stock", "conviction": 7},
    "TSLA": {"type": "stock", "conviction": 5},
    "RIVN": {"type": "stock", "conviction": 4}
}

def generate_optimism_priming():
    return """🌅 OPTIMISM PRIMING | 5:10am

Before the data hits, lock in your mindset:

🚀 What am I EXCITED about today?
🎯 What would make today a WIN?
❤️ Who do I get to help/be with today?

This is your day. Own it.

---

"""

def generate_market_snapshot():
    return """📊 OVERNIGHT MARKET SIGNALS

[Auto-populated: What moved >10% overnight?]

MOMENTUM PLAYS (What's heating up):
• [Asset up 15%+ with volume] → Opportunity sizing
• [New narrative emerging] → Your edge?

DIP ALERTS (Buy opportunities):
• [Watchlist asset down >15%] → Conviction check

FLAT/CHOP:
• Everything else → Hold, wait for Alpha

"""

def generate_opportunity_sizing():
    return """🎯 OPPORTUNITY SIZING

If this plays out, what's the win?

[BUY DIP scenario]:
• Entry: $X
• Target: $Y (Z% upside)
• Position: $A (B% of portfolio)
• If right, gain: $C
• If wrong, loss: $D (max risk)

🎲 Risk/Reward: X:Y
✅ Conviction level: _/10
🏆 Your edge: [Why you're positioned to win]

"""

def generate_portfolio_signals():
    return """💰 YOUR PORTFOLIO

Current Allocation:
• SOL: X% (target: Y%) → [HOLD/ADD/TRIM]
• Cash: $3,000 → Deploy? [YES/NO/WAIT]

Drift Alert:
• Any position >10%? → REBALANCE
• Any position <2%? → Consider adding

Today's ONE Decision:
[ ] Buy the dip on ___?
[ ] Take profit on ___?
[ ] Deploy cash to ___?
[ ] Wait for better setup

"""

def generate_airdrops():
    return """🪂 AIRDROP OPPORTUNITIES

Farming this week:
• [Hyperliquid] → Time: X hrs/week, Potential: $Y
• [Monad testnet] → Time: X hrs, Potential: $Y

Verdict: [WORTH IT / SKIP / RESEARCH]

"""

def generate_video_topics():
    return """🎬 VIDEO TOPIC IDEAS (Brainstorm 2)

**Topic 1: [Narrative/Price Action Story]**
• Asset: [Biggest mover overnight]
• Hook: [Why is this moving?]
• Angle: [Your contrarian or confirming take]
• Urgency: [24-48hr freshness window?]

**Topic 2: [Protocol/Project Development]**
• Project: [New feature/launch/partnership]
• Hook: [What changed?]
• Angle: [Why this matters for Solana ecosystem]
• Evergreen?: [Will this matter in 2 weeks?]

💡 Brainstorm triggers:
• Any asset moved >20%? → "Why [X] is the new [Y]"
• New ATH or major low? → "The [Asset] bottom is in/out"
• Protocol announcement? → "[Project] just changed everything"
• Narrative shift? → "The [narrative] rotation is here"

Script outline ready? → Reply and I'll draft it.

"""

def generate_daily_brief():
    today = datetime.now()
    day_name = today.strftime("%A")
    
    brief = generate_optimism_priming()
    brief += f"""🌟 THOMAS ALPHA BRIEF | {today.strftime('%B %d, %Y')} | {day_name}

⏰ TIME CHECK: 5:30am PST | Kids leave: 6:40am

"""
    brief += generate_market_snapshot()
    brief += generate_opportunity_sizing()
    brief += generate_portfolio_signals()
    brief += generate_airdrops()
    brief += generate_video_topics()
    
    brief += """
📅 FAMILY/STAFF TODAY
• Kids schedule: [from calendar]
• Wife schedule: [from calendar]
• Your focus window: 5:30-6:40am

⏰ HARD STOP: 6:40am → Family mode

Reply with your ONE decision. I execute.

💡 Remember: Depth over breadth. One great call beats ten okay ones.

🦞 PENNY | Building wealth, not just working
"""
    return brief

if __name__ == "__main__":
    print(generate_daily_brief())
