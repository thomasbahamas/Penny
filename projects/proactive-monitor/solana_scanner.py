#!/usr/bin/env python3
"""Solana ecosystem scanner - monitors news, Twitter, sources for alpha"""
import requests
import json
import os
from datetime import datetime, timedelta
from urllib.parse import urljoin

# Keywords to track
KEYWORDS = {
    "high": ["firedancer", "depin", "rwa", "tokenization", "stablecoin", "launch", "partnership"],
    "medium": ["x spaces", "twitter space", "ama", "ecosystem", "grant", "hackathon"],
    "projects": ["jupiter", "jito", "drift", "marginfi", "kamino", "solend", "orca", "raydium", "meteora"]
}

SOURCES = {
    "coindesk": "https://www.coindesk.com/tag/solana/",
    "theblock": "https://www.theblock.co/topic/solana",
    "cointelegraph": "https://cointelegraph.com/tags/solana",
}

def fetch_feed(url, name):
    """Fetch and parse a news feed"""
    try:
        resp = requests.get(url, timeout=15, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        if resp.status_code == 200:
            return {"source": name, "content": resp.text[:5000], "url": url}
    except Exception as e:
        print(f"Error fetching {name}: {e}")
    return None

def scan_for_keywords(text):
    """Scan text for keywords and return matches"""
    text_lower = text.lower()
    matches = {
        "high": [],
        "medium": [],
        "projects": []
    }
    
    for priority, keywords in KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                matches[priority].append(keyword)
    
    return matches

def get_sol_price():
    """Get current SOL price"""
    try:
        resp = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": "solana", "vs_currencies": "usd", "include_24hr_change": "true"},
            timeout=10
        )
        data = resp.json()
        return {
            "price": data["solana"]["usd"],
            "change_24h": data["solana"]["usd_24h_change"]
        }
    except:
        return None

def generate_report():
    """Generate daily Solana ecosystem report"""
    print("=" * 60)
    print("SOLANA ECOSYSTEM SCANNER")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    print("=" * 60)
    
    # SOL price
    sol = get_sol_price()
    if sol:
        change = sol['change_24h']
        emoji = "🟢" if change > 0 else "🔴"
        print(f"\n{emoji} SOL: ${sol['price']:.2f} ({change:+.2f}%)")
    
    # Scan sources
    print("\n📰 SCANNING SOURCES...")
    all_matches = {"high": set(), "medium": set(), "projects": set()}
    
    for name, url in SOURCES.items():
        print(f"  Checking {name}...", end=" ")
        feed = fetch_feed(url, name)
        if feed:
            matches = scan_for_keywords(feed["content"])
            for priority in all_matches:
                all_matches[priority].update(matches[priority])
            print(f"✓ Found {sum(len(v) for v in matches.values())} keywords")
        else:
            print("✗ Failed")
    
    # Report findings
    print("\n" + "=" * 60)
    print("🎯 KEY FINDINGS")
    print("=" * 60)
    
    if all_matches["high"]:
        print(f"\n🔥 HIGH PRIORITY ({len(all_matches['high'])}):")
        for k in sorted(all_matches["high"]):
            print(f"  - {k.upper()}")
    
    if all_matches["medium"]:
        print(f"\n📌 MEDIUM PRIORITY ({len(all_matches['medium'])}):")
        for k in sorted(all_matches["medium"]):
            print(f"  - {k}")
    
    if all_matches["projects"]:
        print(f"\n🏗️ PROJECTS MENTIONED ({len(all_matches['projects'])}):")
        for k in sorted(all_matches["projects"]):
            print(f"  - {k}")
    
    if not any(all_matches.values()):
        print("\nNo significant mentions found.")
    
    print("\n" + "=" * 60)

def check_supabase_pipeline():
    """Placeholder for Supabase monitoring - needs your URL"""
    print("\n📊 SUPABASE PIPELINE (requires config)")
    print("  Status: Not configured")
    print("  To enable: Set SUPABASE_URL and SUPABASE_KEY env vars")

if __name__ == "__main__":
    generate_report()
    check_supabase_pipeline()
    
    # Save activity log
    os.makedirs("/root/clawd/mission-control", exist_ok=True)
    with open("/root/clawd/mission-control/activity.jsonl", "a") as f:
        f.write(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "type": "solana_scan",
            "details": "Daily ecosystem scan completed"
        }) + "\n")
