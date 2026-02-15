#!/usr/bin/env python3
"""Penny Conversation Logger - Auto-store every interaction"""
import json
import sys
from datetime import datetime
from pathlib import Path

# Add memory module to path
sys.path.insert(0, '/root/clawd/projects/memory')

try:
    from penny_memory import PennyMemory
    MEMORY_AVAILABLE = True
except ImportError:
    MEMORY_AVAILABLE = False
    print("⚠️ Memory module not available yet")

class ConversationLogger:
    def __init__(self):
        self.memory = PennyMemory() if MEMORY_AVAILABLE else None
        self.log_dir = Path("/root/clawd/memory/conversations")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
    def log_interaction(self, user_message: str, assistant_response: str, 
                       context: dict = None):
        """Log a conversation interaction"""
        timestamp = datetime.now().isoformat()
        
        # Structure the memory
        memory_text = f"User: {user_message}\nPenny: {assistant_response[:200]}"
        metadata = {
            "type": "conversation",
            "timestamp": timestamp,
            "user_message": user_message[:500],
            "has_action": any(word in assistant_response.lower() 
                             for word in ["built", "created", "committed", "deployed"]),
            **(context or {})
        }
        
        # Store in Qdrant
        if self.memory and self.memory.client:
            self.memory.remember(memory_text, metadata)
        
        # Also save to daily log file (backup)
        date_str = datetime.now().strftime("%Y-%m-%d")
        log_file = self.log_dir / f"{date_str}.jsonl"
        
        entry = {
            "timestamp": timestamp,
            "user": user_message,
            "assistant_preview": assistant_response[:300],
            "metadata": metadata
        }
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
        
        return True
    
    def get_daily_summary(self, date_str: str = None):
        """Get summary of conversations for a day"""
        if date_str is None:
            date_str = datetime.now().strftime("%Y-%m-%d")
        
        log_file = self.log_dir / f"{date_str}.jsonl"
        
        if not log_file.exists():
            return None
        
        interactions = []
        with open(log_file) as f:
            for line in f:
                if line.strip():
                    interactions.append(json.loads(line))
        
        # Build summary
        actions_taken = [i for i in interactions if i['metadata'].get('has_action')]
        topics = set()
        for i in interactions:
            user_msg = i['user'].lower()
            if any(word in user_msg for word in ['skrmax', 'bonk', 'crypto', 'trade']):
                topics.add('trading/portfolio')
            if any(word in user_msg for word in ['video', 'content', 'script', 'solanafloor']):
                topics.add('content')
            if any(word in user_msg for word in ['memory', 'qdrant', 'setup', 'build']):
                topics.add('system/infra')
        
        return {
            "date": date_str,
            "total_interactions": len(interactions),
            "actions_completed": len(actions_taken),
            "topics_discussed": list(topics),
            "key_actions": [i['user'][:60] for i in actions_taken[:5]]
        }

# Global logger instance
_logger = None

def get_logger():
    global _logger
    if _logger is None:
        _logger = ConversationLogger()
    return _logger

if __name__ == "__main__":
    # Test
    logger = ConversationLogger()
    logger.log_interaction(
        "Test message about BONK position",
        "Built position tracker for you. It's now monitoring your portfolio."
    )
    print("✅ Conversation logged")
    
    summary = logger.get_daily_summary()
    print(f"\nToday's summary: {summary}")
