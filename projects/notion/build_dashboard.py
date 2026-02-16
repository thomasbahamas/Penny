#!/usr/bin/env python3
"""Build Thomas's Notion Dashboard"""
import os
from notion_client import Client
from datetime import datetime

# Load token
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
if not NOTION_TOKEN:
    with open(os.path.expanduser('~/.env')) as f:
        for line in f:
            if line.startswith('NOTION_TOKEN='):
                NOTION_TOKEN = line.split('=', 1)[1].strip().strip('"\'')
                break

notion = Client(auth=NOTION_TOKEN)

# Find or create parent page
search = notion.search(query="", page_size=5)
parent_page = None

for page in search['results']:
    if page['object'] == 'page':
        parent_page = page['id']
        break

if not parent_page:
    print("❌ No parent page found. Create a page in Notion first and share it with the integration.")
    exit(1)

print(f"✅ Using parent page: {parent_page}")

# Create Mission Control page
mission_control = notion.pages.create(
    parent={"page_id": parent_page},
    properties={
        "title": {"title": [{"text": {"content": "🪙 Mission Control"}}]}
    },
    children=[
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {"rich_text": [{"text": {"content": "Daily Overview"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"text": {"content": "Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M")}}]
            }
        },
        {
            "object": "block",
            "type": "divider",
            "divider": {}
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"text": {"content": "📊 Active Projects"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"text": {"content": "SKRmaxing v2 - x402 integration"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"text": {"content": "SolanaFloor content pipeline"}}]}
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"text": {"content": "🚨 Blocked Items"}}]}
        },
        {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {"rich_text": [{"text": {"content": "None currently"}}]}
        },
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {"rich_text": [{"text": {"content": "💡 Quick Notes"}}]}
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"text": {"content": "Type notes here..."}}]}
        }
    ]
)

print(f"✅ Created Mission Control: {mission_control['url']}")

# Create Agent Team page
agent_team = notion.pages.create(
    parent={"page_id": parent_page},
    properties={
        "title": {"title": [{"text": {"content": "🤖 Agent Team"}}]}
    },
    children=[
        {
            "object": "block",
            "type": "heading_1",
            "heading_1": {"rich_text": [{"text": {"content": "Active Agents"}}]}
        },
        {
            "object": "block",
            "type": "table",
            "table": {
                "table_width": 4,
                "has_column_header": True,
                "has_row_header": False,
                "children": [
                    {
                        "object": "block",
                        "type": "table_row",
                        "table_row": {
                            "cells": [
                                [{"text": {"content": "Agent"}}],
                                [{"text": {"content": "Role"}}],
                                [{"text": {"content": "Status"}}],
                                [{"text": {"content": "Current Task"}}]
                            ]
                        }
                    },
                    {
                        "object": "block",
                        "type": "table_row",
                        "table_row": {
                            "cells": [
                                [{"text": {"content": "🦞 PENNY"}}],
                                [{"text": {"content": "Orchestrator"}}],
                                [{"text": {"content": "Active"}}],
                                [{"text": {"content": "Coordinating"}}]
                            ]
                        }
                    },
                    {
                        "object": "block",
                        "type": "table_row",
                        "table_row": {
                            "cells": [
                                [{"text": {"content": "🎬 NOVA"}}],
                                [{"text": {"content": "Video Production"}}],
                                [{"text": {"content": "Standby"}}],
                                [{"text": {"content": "-"}}]
                            ]
                        }
                    },
                    {
                        "object": "block",
                        "type": "table_row",
                        "table_row": {
                            "cells": [
                                [{"text": {"content": "⚡ SCALP"}}],
                                [{"text": {"content": "Crypto Trader"}}],
                                [{"text": {"content": "Standby"}}],
                                [{"text": {"content": "-"}}]
                            ]
                        }
                    },
                    {
                        "object": "block",
                        "type": "table_row",
                        "table_row": {
                            "cells": [
                                [{"text": {"content": "🌍 FED"}}],
                                [{"text": {"content": "Macro Investor"}}],
                                [{"text": {"content": "Standby"}}],
                                [{"text": {"content": "-"}}]
                            ]
                        }
                    }
                ]
            }
        }
    ]
)

print(f"✅ Created Agent Team: {agent_team['url']}")

# Create Trading Journal database
trading_db = notion.databases.create(
    parent={"page_id": parent_page},
    title=[{"text": {"content": "💰 Trading Journal"}}],
    properties={
        "Token": {"title": {}},
        "Date": {"date": {}},
        "Action": {"select": {"options": [
            {"name": "Buy", "color": "green"},
            {"name": "Sell", "color": "red"},
            {"name": "Hold", "color": "yellow"}
        ]}},
        "Entry Price": {"number": {"format": "dollar"}},
        "Exit Price": {"number": {"format": "dollar"}},
        "Position Size": {"number": {"format": "dollar"}},
        "PnL": {"number": {"format": "dollar"}},
        "Thesis": {"rich_text": {}},
        "Status": {"select": {"options": [
            {"name": "Open", "color": "blue"},
            {"name": "Closed", "color": "gray"}
        ]}}
    }
)

print(f"✅ Created Trading Journal: {trading_db['url']}")

# Create Content Pipeline database
content_db = notion.databases.create(
    parent={"page_id": parent_page},
    title=[{"text": {"content": "🎥 Content Pipeline"}}],
    properties={
        "Title": {"title": {}},
        "Status": {"select": {"options": [
            {"name": "Idea", "color": "gray"},
            {"name": "Research", "color": "blue"},
            {"name": "Scripting", "color": "yellow"},
            {"name": "Recording", "color": "orange"},
            {"name": "Editing", "color": "purple"},
            {"name": "Published", "color": "green"}
        ]}},
        "Priority": {"select": {"options": [
            {"name": "High", "color": "red"},
            {"name": "Medium", "color": "yellow"},
            {"name": "Low", "color": "gray"}
        ]}},
        "Agent": {"select": {"options": [
            {"name": "NOVA", "color": "pink"},
            {"name": "SCRIBE", "color": "blue"},
            {"name": "ATLAS", "color": "green"}
        ]}},
        "Due Date": {"date": {}},
        "Notes": {"rich_text": {}}
    }
)

print(f"✅ Created Content Pipeline: {content_db['url']}")

print("\n" + "="*60)
print("🎉 NOTION DASHBOARD COMPLETE!")
print("="*60)
print("\nCreated:")
print("  1. 🪙 Mission Control")
print("  2. 🤖 Agent Team")
print("  3. 💰 Trading Journal (database)")
print("  4. 🎥 Content Pipeline (database)")
print("\nOpen Notion on your phone to see everything!")
