#!/usr/bin/env python3
"""Morning Memory Recap - Compare today vs yesterday, show improvements"""
import json
from datetime import datetime, timedelta
from pathlib import Path
import sys

sys.path.insert(0, '/root/clawd/projects/memory')
from conversation_logger import ConversationLogger

class MorningRecap:
    def __init__(self):
        self.logger = ConversationLogger()
        self.recap_dir = Path("/root/clawd/memory/recaps")
        self.recap_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_recap(self):
        """Generate morning recap comparing yesterday vs today"""
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        
        today_str = today.strftime("%Y-%m-%d")
        yesterday_str = yesterday.strftime("%Y-%m-%d")
        
        # Get summaries
        today_summary = self.logger.get_daily_summary(today_str) or {
            "date": today_str, 
            "total_interactions": 0, 
            "actions_completed": 0,
            "topics_discussed": [],
            "key_actions": []
        }
        
        yesterday_summary = self.logger.get_daily_summary(yesterday_str) or {
            "date": yesterday_str,
            "total_interactions": 0,
            "actions_completed": 0,
            "topics_discussed": [],
            "key_actions": []
        }
        
        # Calculate improvements
        interaction_delta = today_summary["total_interactions"] - yesterday_summary["total_interactions"]
        action_delta = today_summary["actions_completed"] - yesterday_summary["actions_completed"]
        
        # Build recap
        recap = []
        recap.append("=" * 60)
        recap.append(f"🧠 MORNING MEMORY RECAP")
        recap.append(f"{today.strftime('%A, %B %d, %Y')}")
        recap.append("=" * 60)
        recap.append("")
        
        # Yesterday's achievements
        recap.append(f"📅 Yesterday ({yesterday_str}):")
        recap.append(f"   • {yesterday_summary['total_interactions']} conversations")
        recap.append(f"   • {yesterday_summary['actions_completed']} actions completed")
        if yesterday_summary['key_actions']:
            recap.append("   • Key work:")
            for action in yesterday_summary['key_actions'][:3]:
                recap.append(f"     - {action}")
        recap.append("")
        
        # Today's stats so far
        recap.append(f"📊 Today ({today_str}) - So Far:")
        recap.append(f"   • {today_summary['total_interactions']} interactions")
        recap.append(f"   • {today_summary['actions_completed']} actions shipped")
        
        # Improvement indicators
        if action_delta > 0:
            recap.append(f"   📈 +{action_delta} more actions than yesterday!")
        elif action_delta < 0:
            recap.append(f"   📉 {action_delta} fewer actions (early in day)")
        else:
            recap.append("   ➡️ Same pace as yesterday")
        recap.append("")
        
        # Context recall
        recap.append("🎯 Active Projects (from memory):")
        all_topics = set(today_summary['topics_discussed'] + yesterday_summary['topics_discussed'])
        for topic in all_topics:
            recap.append(f"   • {topic}")
        recap.append("")
        
        # Recommendations based on yesterday
        recap.append("💡 Suggestions for Today:")
        
        # Check for incomplete work
        if 'skrmax' in str(yesterday_summary).lower() and 'submitted' not in str(yesterday_summary).lower():
            recap.append("   • SKRmaxing was discussed — check dApp Store status")
        
        if 'bonk' in str(yesterday_summary).lower():
            recap.append("   • BONK position mentioned — review portfolio allocation")
        
        if 'qdrant' in str(yesterday_summary).lower() or 'memory' in str(yesterday_summary).lower():
            recap.append("   • Memory system was built — test it out!")
        
        if 'alpha' in str(yesterday_summary).lower() or 'research' in str(yesterday_summary).lower():
            recap.append("   • Alpha research pipeline active — check overnight findings")
        
        recap.append("")
        recap.append("=" * 60)
        recap.append("🦞 Ready when you are!")
        
        # Save recap
        recap_text = "\n".join(recap)
        recap_file = self.recap_dir / f"recap-{today_str}.md"
        with open(recap_file, 'w') as f:
            f.write(recap_text)
        
        return recap_text, recap_file
    
    def compare_week_over_week(self):
        """Compare this week vs last week"""
        # Future enhancement
        pass

if __name__ == "__main__":
    recap = MorningRecap()
    text, file_path = recap.generate_recap()
    print(text)
    print(f"\n✅ Recap saved to: {file_path}")
