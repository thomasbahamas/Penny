#!/usr/bin/env python3
"""
Penny Command Interface - Quick commands for Thomas

Usage:
  python3 penny_cmd.py log-trade SOL Buy 80.50 --size 1000 --thesis "Support bounce"
  python3 penny_cmd.py agent-status SCALP "Researching SOL setup"
  python3 penny_cmd.py content "x402 Video" --status "Scripting" --agent NOVA
"""
import sys
import argparse

sys.path.insert(0, '/root/clawd/projects/notion')
from notion_sync import log_trade, update_agent, add_content

def main():
    parser = argparse.ArgumentParser(description='Penny Command Interface')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Log trade command
    trade_parser = subparsers.add_parser('log-trade', help='Log a trade to Notion')
    trade_parser.add_argument('token', help='Token symbol (e.g., SOL, BONK)')
    trade_parser.add_argument('action', choices=['Buy', 'Sell', 'Hold'], help='Trade action')
    trade_parser.add_argument('entry', type=float, help='Entry price')
    trade_parser.add_argument('--size', type=float, help='Position size in USD')
    trade_parser.add_argument('--exit', type=float, help='Exit price (if closed)')
    trade_parser.add_argument('--pnl', type=float, help='PnL (if closed)')
    trade_parser.add_argument('--thesis', help='Trade thesis/reasoning')
    
    # Agent status command
    agent_parser = subparsers.add_parser('agent-status', help='Update agent status')
    agent_parser.add_argument('agent', help='Agent name (NOVA, SCALP, FED, etc.)')
    agent_parser.add_argument('status', help='Current status')
    agent_parser.add_argument('--task', help='Current task (optional)')
    
    # Content command
    content_parser = subparsers.add_parser('content', help='Add content idea')
    content_parser.add_argument('title', help='Content title')
    content_parser.add_argument('--status', default='Idea', help='Status (Idea, Scripting, etc.)')
    content_parser.add_argument('--agent', help='Assigned agent')
    content_parser.add_argument('--due', help='Due date (YYYY-MM-DD)')
    content_parser.add_argument('--notes', help='Additional notes')
    
    args = parser.parse_args()
    
    if args.command == 'log-trade':
        success = log_trade(
            token=args.token,
            action=args.action,
            entry=args.entry,
            position_size=args.size,
            exit=args.exit,
            pnl=args.pnl,
            thesis=args.thesis
        )
        if success:
            print(f"✅ Logged: {args.action} {args.token} @ ${args.entry}")
        else:
            print("❌ Failed to log trade")
            
    elif args.command == 'agent-status':
        success = update_agent(args.agent, args.status, args.task)
        if success:
            print(f"✅ Updated {args.agent}: {args.status}")
        else:
            print("❌ Failed to update agent")
            
    elif args.command == 'content':
        success = add_content(
            title=args.title,
            status=args.status,
            agent=args.agent,
            due=args.due,
            notes=args.notes
        )
        if success:
            print(f"✅ Added content: {args.title}")
        else:
            print("❌ Failed to add content")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
