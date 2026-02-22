#!/usr/bin/env python3
"""
THOMAS EVENING WIN LOG — WITH OPTIMISM
Runs at 6:00pm PST daily
Focus on what went RIGHT, not just audit
"""

from datetime import datetime

def generate_win_log():
    today = datetime.now().strftime("%B %d, %Y")
    
    return f"""🌙 THOMAS EVENING WIN LOG | {today}

---

🎉 TODAY'S WINS (What went RIGHT?)

1. 
2. 
3. 

No win too small. Did you make a decision? Show up for family? Create something?

---

✨ WHAT I CREATED TODAY

• Content: 
• Value: 
• Connections: 

---

❤️ WHAT I'M PROUD OF

• 
• 

---

🎯 AGENCY MOMENT

When did I feel most ALIVE / EMPOWERED today?
What decision made me PROUD?

---

📊 AGENCY SCORE: ___/10

(1 = Drifting, 10 = Fully intentional)

---

🚀 OPTIMISM FOR TOMORROW

What am I EXCITED about for tomorrow?
What would make tomorrow a WIN?

---

💪 REMEMBER

You built systems today.
You showed up for family today.
You made decisions with intention today.

That's wealth-building. That's freedom.

🦞 PENNY | See you at 5:10am for optimism priming
"""

if __name__ == "__main__":
    print(generate_win_log())
