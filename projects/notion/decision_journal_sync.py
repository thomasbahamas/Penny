#!/usr/bin/env python3
"""
Thomas Decision Journal — Notion Sync Helper
Posts daily agency check-ins to Notion database
"""

import os
from datetime import datetime

# Notion setup (you'll need to add your integration token)
NOTION_TOKEN = os.getenv("NOTION_API_KEY")
DATABASE_ID = "decision-journal"  # You'll create this in Notion

DAILY_PROMPTS = {
    "morning": """🌅 MORNING PRIMING (5:00-5:10am)

1. My intuition says:
2. If I couldn't check X/Twitter, I would:
3. The one thing I know but don't want to admit:
""",
    
    "decision_filter": """⏸️ THE DECISION FILTER (60 seconds)

Decision: ___________

• Why am I REALLY doing this?
• What am I avoiding by doing this?
• Is this moving toward freedom or away?
• If I do nothing, what happens?

Verdict: [ ] YES  [ ] NO  [ ] WAIT
""",
    
    "evening": """🌙 EVENING REFLECTION

Today I decided:
My reasoning was:
What I ignored:
What I'll question tomorrow:

Agency Score (1-10): ___
"""
}

def generate_daily_entry():
    today = datetime.now().strftime("%Y-%m-%d (%A)")
    return f"""# Decision Journal — {today}

{DAILY_PROMPTS["morning"]}

---

{DAILY_PROMPTS["decision_filter"]}

---

{DAILY_PROMPTS["evening"]}
"""

if __name__ == "__main__":
    print(generate_daily_entry())
    print("\n" + "="*50)
    print("Copy this to your Notion page for today")
    print("Or set up NOTION_API_KEY to auto-sync")
