#!/usr/bin/env python3
"""Alpha Hunter - monitors X and crypto news for alpha"""
import requests
import json
import os
from datetime import datetime, timedelta
from urllib.parse import urlencode

# Config
KEYWORDS = {
    "high": ["x402", "alpenglow", "bam", "jito", "solana", "firedancer", "depin", "rwa"],
    "medium": ["hyperliquid", "jupiter", "drift", "kamino", "marginfi"],
    "alerts": ["exploit", "hack", "rug", "audit", "partnership", "raise", "funding"]
}

ACCOUNTS_TO_WATCH = [
    "solana",
    "toly",
    "aeyakovenko", 
    "superteamdao",
    "thomasbahamasfi",
    "Inversebrah",
    "blknoiz06"
]

# Nitter instances (rotating for reliability)
NITTER_INSTANCES = [
    "https://nitter.net",
    "https://nitter.it",
    "https://nitter.cz"
]

NEWS_CHANNELS = {
    "coindesk": "https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=amp",
    "theblock": "https://www.theblock.co/rss",
    "cointelegraph": "https://cointelegraph.com/rss",
    "decrypt": "https://decrypt.co/feed"
}

def fetch_x_feed(username, instance_idx=0):
    """Fetch recent tweets from X via Nitter"""
    try:
        instance = NITTER_INSTANCES[instance_idx % len(NITTER_INSTANCES)]
        url = f"{instance}/{username}/rss"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 200:
            # Parse RSS for items
            import xml.etree.ElementTree as ET
            root = ET.fromstring(resp.content)
            items = []
            
            for item in root.findall('.//item'):
                title = item.find('title')
                link = item.find('link')
                pub_date = item.find('pubDate')
                
                if title is not None:
                    items.append({
                        'username': username,
                        'text': title.text,
                        'link': link.text if link is not None else '',
                        'time': pub_date.text if pub_date is not None else ''
                    })
            
            return items[:5]  # Last 5 tweets
    except Exception as e:
        print(f"Error fetching @{username}: {e}")
    return []

def scan_for_alpha(text, source):
    """Scan text for alpha keywords"""
    text_lower = text.lower()
    findings = []
    
    for priority, words in KEYWORDS.items():
        for word in words:
            if word in text_lower:
                findings.append({
                    'word': word,
                    'priority': priority,
                    'source': source
                })
    
    return findings

def fetch_news_rss(source_name, url):
    """Fetch RSS feed from crypto news"""
    try:
        resp = requests.get(url, timeout=15, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        })
        
        if resp.status_code == 200:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(resp.content)
            items = []
            
            for item in root.findall('.//item')[:10]:  # Last 10
                title = item.find('title')
                link = item.find('link')
                desc = item.find('description')
                
                if title is not None:
                    items.append({
                        'title': title.text,
                        'link': link.text if link is not None else '',
                        'desc': desc.text if desc is not None else '',
                        'source': source_name
                    })
            
            return items
    except Exception as e:
        print(f"Error fetching {source_name}: {e}")
    return []

def generate_alpha_report():
    """Generate alpha hunting report"""
    print("=" * 60)
    print("🎯 ALPHA HUNTER REPORT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    print("=" * 60)
    
    all_findings = []
    
    # Scan X accounts
    print("\n🐦 SCANNING X ACCOUNTS...")
    for username in ACCOUNTS_TO_WATCH:
        tweets = fetch_x_feed(username)
        if tweets:
            print(f"  @{username}: {len(tweets)} tweets")
            for tweet in tweets:
                findings = scan_for_alpha(tweet['text'], f"@{username}")
                if findings:
                    all_findings.extend(findings)
                    print(f"    🚨 ALPHA: {tweet['text'][:80]}...")
                    for f in findings:
                        print(f"      → {f['priority'].upper()}: {f['word']}")
        else:
            print(f"  @{username}: No data (rate limited)")
    
    # Scan news
    print("\n📰 SCANNING NEWS...")
    for source, url in NEWS_CHANNELS.items():
        articles = fetch_news_rss(source, url)
        if articles:
            print(f"  {source}: {len(articles)} articles")
            for article in articles[:3]:
                text = f"{article['title']} {article.get('desc', '')}"
                findings = scan_for_alpha(text, source)
                if findings:
                    all_findings.extend(findings)
                    print(f"    🚨 ALPHA: {article['title'][:80]}...")
        else:
            print(f"  {source}: Failed")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 ALPHA SUMMARY")
    print("=" * 60)
    
    if all_findings:
        high_priority = [f for f in all_findings if f['priority'] == 'alerts']
        medium = [f for f in all_findings if f['priority'] == 'high']
        low = [f for f in all_findings if f['priority'] == 'medium']
        
        if high_priority:
            print(f"\n🚨 URGENT ALERTS ({len(high_priority)}):")
            for f in high_priority[:5]:
                print(f"  • {f['word']} ({f['source']})")
        
        if medium:
            print(f"\n🔥 HIGH ALPHA ({len(medium)}):")
            seen = set()
            for f in medium:
                if f['word'] not in seen:
                    print(f"  • {f['word']} ({f['source']})")
                    seen.add(f['word'])
        
        if low:
            print(f"\n📌 MENTIONS ({len(low)}):")
            seen = set()
            for f in low[:10]:
                if f['word'] not in seen:
                    print(f"  • {f['word']}")
                    seen.add(f['word'])
    else:
        print("\nNo major alpha detected.")
    
    # Save activity
    os.makedirs("/root/clawd/mission-control", exist_ok=True)
    with open("/root/clawd/mission-control/activity.jsonl", "a") as f:
        f.write(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "type": "alpha_hunter_scan",
            "findings": len(all_findings),
            "high": len([x for x in all_findings if x['priority'] == 'alerts'])
        }) + "\n")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    generate_alpha_report()
