#!/usr/bin/env python3
"""Activity logger - records every action for Mission Control"""
import json
import os
from datetime import datetime

ACTIVITY_LOG = "/root/clawd/mission-control/activity.jsonl"

def log_activity(action_type, details, status="completed"):
    """Log an activity to the feed"""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "type": action_type,
        "details": details,
        "status": status,
        "session": os.environ.get("SESSION_ID", "main")
    }
    
    os.makedirs(os.path.dirname(ACTIVITY_LOG), exist_ok=True)
    with open(ACTIVITY_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    
    return entry

if __name__ == "__main__":
    # Test
    log_activity("test", "Activity logger initialized")
    print("✅ Activity logger ready")
