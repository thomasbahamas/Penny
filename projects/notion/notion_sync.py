#!/usr/bin/env python3
"""Penny Notion Sync - Auto-sync data to Thomas's dashboard"""
import os
import sys
from datetime import datetime
from notion_client import Client

class NotionSync:
    def __init__(self):
        # Load token
        self.token = os.getenv('NOTION_TOKEN')
        if not self.token:
            try:
                with open(os.path.expanduser('~/.env')) as f:
                    for line in f:
                        if line.startswith('NOTION_TOKEN='):
                            self.token = line.split('=', 1)[1].strip().strip('"\'')
                            break
            except:
                pass
        
        if not self.token:
            raise ValueError("NOTION_TOKEN not found")
        
        self.notion = Client(auth=self.token)
        self.cache = {}
        
    def find_page(self, query):
        """Find a page by query (with caching)"""
        if query in self.cache:
            return self.cache[query]
        
        results = self.notion.search(query=query, page_size=5)
        for page in results['results']:
            if page['object'] == 'page':
                self.cache[query] = page['id']
                return page['id']
        return None
    
    def sync_daily_brief(self, brief_text: str, date_str: str = None):
        """Sync daily brief to Mission Control"""
        if date_str is None:
            date_str = datetime.now().strftime("%Y-%m-%d")
        
        mission_id = self.find_page("Mission Control")
        if not mission_id:
            print("⚠️ Mission Control page not found")
            return False
        
        try:
            # Add brief as a new block at the top
            self.notion.blocks.children.append(
                block_id=mission_id,
                children=[
                    {
                        "object": "block",
                        "type": "divider",
                        "divider": {}
                    },
                    {
                        "object": "block",
                        "type": "heading_2",
                        "heading_2": {
                            "rich_text": [{"text": {"content": f"📅 Daily Brief - {date_str}"}}]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"text": {"content": brief_text[:2000]}}]  # Notion limit
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {"text": {"content": "Updated: "}},
                                {"text": {"content": datetime.now().strftime("%H:%M")}}
                            ]
                        }
                    }
                ]
            )
            print(f"✅ Synced daily brief to Notion: {date_str}")
            return True
        except Exception as e:
            print(f"⚠️ Failed to sync brief: {e}")
            return False
    
    def log_trade(self, token: str, action: str, entry: float, 
                  position_size: float = None, exit: float = None, 
                  pnl: float = None, thesis: str = None):
        """Log a trade to Trading Journal table"""
        mission_id = self.find_page("Mission Control")
        if not mission_id:
            print("⚠️ Mission Control not found")
            return False
        
        # Find the Trading Journal table
        try:
            blocks = self.notion.blocks.children.list(block_id=mission_id)
            table_id = None
            
            for block in blocks['results']:
                if block['type'] == 'table':
                    table_id = block['id']
                    break
            
            if not table_id:
                print("⚠️ Trading Journal table not found")
                return False
            
            # Add row to table
            self.notion.blocks.children.append(
                block_id=table_id,
                children=[
                    {
                        "object": "block",
                        "type": "table_row",
                        "table_row": {
                            "cells": [
                                [{"text": {"content": datetime.now().strftime("%Y-%m-%d")}}],
                                [{"text": {"content": token}}],
                                [{"text": {"content": action}}],
                                [{"text": {"content": f"${entry}" if entry else "-"}}],
                                [{"text": {"content": f"${exit}" if exit else "-"}}],
                                [{"text": {"content": f"${pnl:+.2f}" if pnl else "-"}}],
                                [{"text": {"content": thesis[:100] if thesis else "-"}}]
                            ]
                        }
                    }
                ]
            )
            print(f"✅ Logged trade: {action} {token}")
            return True
            
        except Exception as e:
            print(f"⚠️ Failed to log trade: {e}")
            return False
    
    def update_agent_status(self, agent_name: str, status: str, task: str = None):
        """Update agent status in Agent Team page"""
        agent_page_id = self.find_page("Agent Team")
        if not agent_page_id:
            print("⚠️ Agent Team page not found")
            return False
        
        try:
            # Add status update
            self.notion.blocks.children.append(
                block_id=agent_page_id,
                children=[
                    {
                        "object": "block",
                        "type": "callout",
                        "callout": {
                            "rich_text": [
                                {"text": {"content": f"{agent_name}: "}},
                                {"text": {"content": f"{status}"}},
                                {"text": {"content": f" - {task}" if task else "")}}
                            ],
                            "icon": {"emoji": "🤖"}
                        }
                    }
                ]
            )
            print(f"✅ Updated {agent_name} status: {status}")
            return True
        except Exception as e:
            print(f"⚠️ Failed to update agent: {e}")
            return False
    
    def add_content_idea(self, title: str, status: str = "Idea", 
                        agent: str = None, due: str = None, notes: str = None):
        """Add content idea to pipeline"""
        mission_id = self.find_page("Mission Control")
        if not mission_id:
            return False
        
        try:
            # Find Content Pipeline table
            blocks = self.notion.blocks.children.list(block_id=mission_id)
            table_id = None
            
            for block in blocks['results']:
                if block['type'] == 'table':
                    # Check if this is the content table by looking at headers
                    table_info = self.notion.blocks.retrieve(block_id=block['id'])
                    table_id = block['id']
                    break
            
            if not table_id:
                print("⚠️ Content Pipeline table not found")
                return False
            
            # Add row
            self.notion.blocks.children.append(
                block_id=table_id,
                children=[
                    {
                        "object": "block",
                        "type": "table_row",
                        "table_row": {
                            "cells": [
                                [{"text": {"content": title}}],
                                [{"text": {"content": status}}],
                                [{"text": {"content": agent or "-"}}],
                                [{"text": {"content": due or "-"}}],
                                [{"text": {"content": notes or "-"}}]
                            ]
                        }
                    }
                ]
            )
            print(f"✅ Added content: {title}")
            return True
            
        except Exception as e:
            print(f"⚠️ Failed to add content: {e}")
            return False

# Global instance
_notion_sync = None

def get_sync():
    global _notion_sync
    if _notion_sync is None:
        _notion_sync = NotionSync()
    return _notion_sync

# Convenience functions
def sync_brief(text: str, date: str = None):
    return get_sync().sync_daily_brief(text, date)

def log_trade(token: str, action: str, entry: float, **kwargs):
    return get_sync().log_trade(token, action, entry, **kwargs)

def update_agent(agent: str, status: str, task: str = None):
    return get_sync().update_agent_status(agent, status, task)

def add_content(title: str, **kwargs):
    return get_sync().add_content_idea(title, **kwargs)

if __name__ == "__main__":
    # Test
    sync = NotionSync()
    print("✅ Notion sync initialized")
    
    # Test brief sync
    sync.sync_daily_brief("Test brief: BONK up 2%, SOL showing support at $80. FED meeting tomorrow.")
    
    # Test trade log
    sync.log_trade("SOL", "Buy", 80.50, position_size=1000, thesis="Support bounce")
    
    print("✅ Test complete")
