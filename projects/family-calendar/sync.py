#!/usr/bin/env python3
"""
Family Calendar Sync for Thomas
Tracks daycare closures, school holidays, and family events
with 2-week advance notifications
"""

from datetime import datetime, timedelta

# Daycare/school closures (extracted from screenshot)
DAYCARE_CLOSURES = [
    {"date": "2026-02-16", "name": "President's Day - School Closed", "type": "holiday"},
    {"date": "2026-04-02", "name": "Easter Party", "type": "event"},
    {"date": "2026-04-03", "name": "Good Friday - Closed", "type": "holiday"},
    {"date": "2026-04-06", "name": "Easter Monday - Closed", "type": "holiday"},
    {"date": "2026-05-25", "name": "Memorial Day - School Closed", "type": "holiday"},
]

# Family trips/events
FAMILY_EVENTS = [
    {
        "start": "2026-05-04",
        "end": "2026-05-08",
        "name": "Anniversary Trip - Newport Beach",
        "type": "trip",
        "notes": "Work off, kids need coverage"
    },
]

# Additional typical school holidays (add as discovered)
PROJECTED_HOLIDAYS_2026 = [
    # Winter break (check with school)
    # Spring break (varies)
    # Summer break start
    # Labor Day
    # Thanksgiving
    # Christmas/New Year
]

def get_notification_date(event_date, days_before=14):
    """Calculate when to send reminder"""
    event = datetime.strptime(event_date, "%Y-%m-%d")
    notify = event - timedelta(days=days_before)
    return notify.strftime("%Y-%m-%d")

def generate_calendar_sync():
    """Generate calendar entries with notifications"""
    print("=" * 60)
    print("📅 FAMILY CALENDAR SYNC")
    print("=" * 60)
    
    for event in DAYCARE_CLOSURES:
        notify_date = get_notification_date(event["date"])
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Skip if already passed
        if event["date"] < today:
            status = "✅ Past"
        elif notify_date <= today:
            status = "🔔 NOTIFY NOW"
        else:
            status = f"⏰ Notify on {notify_date}"
        
        print(f"\n{event['name']}")
        print(f"  Date: {event['date']}")
        print(f"  Type: {event['type']}")
        print(f"  Status: {status}")
    
    print("\n" + "=" * 60)
    print("🌴 FAMILY TRIPS")
    print("=" * 60)
    
    for trip in FAMILY_EVENTS:
        notify_date = get_notification_date(trip["start"])
        print(f"\n{trip['name']}")
        print(f"  Dates: {trip['start']} to {trip['end']}")
        print(f"  Notify: {notify_date}")
        print(f"  Notes: {trip['notes']}")
    
    print("\n" + "=" * 60)
    print("✅ Calendar sync complete!")
    print("=" * 60)

def add_to_notion_calendar():
    """Sync to Notion (when API ready)"""
    # This would use notion_sync.py to add entries
    pass

def check_upcoming_notifications():
    """Check if any notifications due today"""
    today = datetime.now().strftime("%Y-%m-%d")
    notifications = []
    
    all_events = DAYCARE_CLOSURES + FAMILY_EVENTS
    
    for event in all_events:
        event_date = event.get("date") or event.get("start")
        notify_date = get_notification_date(event_date)
        
        if notify_date == today:
            notifications.append(event)
    
    if notifications:
        print(f"\n🔔 NOTIFICATIONS DUE TODAY ({today}):")
        for n in notifications:
            print(f"  - {n['name']} in 2 weeks")
        return notifications
    
    return []

if __name__ == "__main__":
    generate_calendar_sync()
    
    # Check for notifications due
    upcoming = check_upcoming_notifications()
    
    if not upcoming:
        print("\n✨ No notifications due today")
