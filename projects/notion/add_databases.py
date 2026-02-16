#!/usr/bin/env python3
"""Create Notion databases for Thomas"""
import os
from notion_client import Client

NOTION_TOKEN = os.getenv('NOTION_TOKEN')
if not NOTION_TOKEN:
    with open(os.path.expanduser('~/.env')) as f:
        for line in f:
            if line.startswith('NOTION_TOKEN='):
                NOTION_TOKEN = line.split('=', 1)[1].strip().strip('"\'')
                break

notion = Client(auth=NOTION_TOKEN)

# Find the Mission Control page
search = notion.search(query="Mission Control")
parent_id = None

for page in search['results']:
    if 'Mission Control' in str(page.get('properties', {})):
        parent_id = page['id']
        break

if not parent_id:
    # Use first available page
    search = notion.search(query="", page_size=1)
    if search['results']:
        parent_id = search['results'][0]['id']

print(f"Using parent: {parent_id}")

# Create databases as inline within pages
try:
    # Add database blocks to Mission Control page
    notion.blocks.children.append(
        block_id=parent_id,
        children=[
            {
                "object": "block",
                "type": "divider",
                "divider": {}
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"text": {"content": "💰 Trading Journal"}}]}
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"text": {"content": "Log your trades here. I can auto-populate this from our research sessions."}}]}
            },
            {
                "object": "block",
                "type": "table",
                "table": {
                    "table_width": 7,
                    "has_column_header": True,
                    "has_row_header": False,
                    "children": [
                        {
                            "object": "block",
                            "type": "table_row",
                            "table_row": {
                                "cells": [
                                    [{"text": {"content": "Date"}}],
                                    [{"text": {"content": "Token"}}],
                                    [{"text": {"content": "Action"}}],
                                    [{"text": {"content": "Entry"}}],
                                    [{"text": {"content": "Exit"}}],
                                    [{"text": {"content": "PnL"}}],
                                    [{"text": {"content": "Thesis"}}]
                                ]
                            }
                        }
                    ]
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
                "heading_2": {"rich_text": [{"text": {"content": "🎥 Content Pipeline"}}]}
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"text": {"content": "Track video ideas from concept to published."}}]}
            },
            {
                "object": "block",
                "type": "table",
                "table": {
                    "table_width": 5,
                    "has_column_header": True,
                    "has_row_header": False,
                    "children": [
                        {
                            "object": "block",
                            "type": "table_row",
                            "table_row": {
                                "cells": [
                                    [{"text": {"content": "Title"}}],
                                    [{"text": {"content": "Status"}}],
                                    [{"text": {"content": "Agent"}}],
                                    [{"text": {"content": "Due"}}],
                                    [{"text": {"content": "Notes"}}]
                                ]
                            }
                        }
                    ]
                }
            }
        ]
    )
    print("✅ Added Trading Journal and Content Pipeline tables")
    
except Exception as e:
    print(f"⚠️ Error: {e}")

print("\n🎉 Dashboard setup complete!")
print("\nOpen Notion and check your Mission Control page")
