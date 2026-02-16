#!/usr/bin/env python3
"""Notion Dashboard Setup for Thomas"""
import os
import sys
from datetime import datetime

try:
    from notion_client import Client
except ImportError:
    print("Installing notion-client...")
    os.system("pip3 install notion-client --user --break-system-packages 2>&1 | tail -3")
    from notion_client import Client

# Load token from env
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
if not NOTION_TOKEN:
    # Try loading from file
    try:
        with open(os.path.expanduser('~/.env')) as f:
            for line in f:
                if line.startswith('NOTION_TOKEN='):
                    NOTION_TOKEN = line.split('=', 1)[1].strip().strip('"\'')
                    break
    except:
        pass

if not NOTION_TOKEN:
    print("❌ NOTION_TOKEN not found")
    sys.exit(1)

print(f"✅ Token loaded: {NOTION_TOKEN[:20]}...")

# Initialize Notion client
notion = Client(auth=NOTION_TOKEN)

# Test connection
try:
    user = notion.users.me()
    print(f"✅ Connected as: {user.get('name', 'Unknown')}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    sys.exit(1)

# Search for existing pages to use as parent
try:
    search_results = notion.search(query="", page_size=10)
    print(f"\n📄 Found {len(search_results['results'])} pages in workspace")
    
    for page in search_results['results'][:3]:
        title = "Untitled"
        if 'properties' in page and 'title' in page['properties']:
            title_obj = page['properties']['title']
            if 'title' in title_obj and title_obj['title']:
                title = title_obj['title'][0].get('plain_text', 'Untitled')
        print(f"  - {title}")
        
except Exception as e:
    print(f"⚠️ Search failed: {e}")

print("\n✅ Notion connection successful!")
print("\nNext steps:")
print("1. Create dashboard pages")
print("2. Set up databases for tracking")
print("3. Configure auto-sync")
