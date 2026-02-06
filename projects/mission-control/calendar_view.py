#!/usr/bin/env python3
"""Calendar view - shows all scheduled OpenClaw tasks"""
import json
import os
from datetime import datetime, timedelta
from croniter import croniter

CRON_FILE = "/var/spool/cron/crontabs/root"

def get_cron_jobs():
    """Parse crontab and return scheduled tasks"""
    jobs = []
    try:
        with open(CRON_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    parts = line.split()
                    if len(parts) >= 6:
                        schedule = " ".join(parts[:5])
                        command = " ".join(parts[5:])
                        jobs.append({
                            "schedule": schedule,
                            "command": command,
                            "next_run": get_next_run(schedule)
                        })
    except FileNotFoundError:
        pass
    return jobs

def get_next_run(schedule):
    """Calculate next run time from cron schedule"""
    try:
        itr = croniter(schedule, datetime.now())
        return itr.get_next(datetime).isoformat()
    except:
        return "unknown"

if __name__ == "__main__":
    jobs = get_cron_jobs()
    print("📅 SCHEDULED TASKS")
    print("=" * 50)
    for job in jobs:
        print(f"⏰ {job['schedule']}")
        print(f"   {job['command'][:60]}")
        print(f"   Next: {job['next_run'][:16]}")
        print()
