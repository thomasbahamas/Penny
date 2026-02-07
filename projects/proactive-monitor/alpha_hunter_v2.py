#!/usr/bin/env python3
"""Alpha Hunter v2 - Telegram crypto news + RSS feeds"""
import requests
import json
import os
from datetime import datetime

# Crypto news Telegram channels to monitor
# Join these and add bot as admin to read them
TELEGRAM_NEWS_CHANNELS = [
    "@coindesk",           # CoinDesk
    "@Cointelegraph",      # Cointelegraph
    "@theblockcrypto",     # The Block
    "@decryptco",          # Decrypt
    "@CryptoPanicNews",    # Aggregator
]

# RSS feeds (reliable)
RSS_FEEDS = {
    "coindesk": "https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=amp",
    "cointelegraph": "https://cointelegraph.com/rss",
    "decrypt": "https://decrypt.co/feed",
    "bankless": "https://www.bankless.com/rss.xml"
}

# Keywords to hunt
ALPHA_KEYWORDS = {
    "solana_ecosystem": ["solana", "jupiter", "jito", "drift", "kamino", "marginfi", "ore", "bonk", "wif"],
    "tech": ["x402", "alpenglow", "firedancer", "depin", "rwa", "tokenization"],
    "alerts": ["exploit", "hack", "rug", "audit", "partnership", "raise", "funding", "airdrop"],
    "markets": ["etf", "sec", "binance", "coinbase", "listing"]
}

def fetch_rss(name, url):
    """Fetch RSS feed"""
    try:
        resp = requests.get(url, timeout=15, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        })
        
        if resp.status_code == 200:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(resp.content)
            items = []
            
            for item in root.findall('.//item')[:15]:
                title = item.find('title')
                link = item.find('link')
                
                if title is not None:
                    items.append({
                        'title': title.text,
                        'link': link.text if link else '',
                        'source': name
                    })
            return items
    except Exception as e:
        print(f"  {name}: Error - {e}")
    return []

def scan_alpha(text, source):
    """Scan for alpha keywords"""
    text_lower = text.lower()
    hits = []
    
    for category, words in ALPHA_KEYWORDS.items():
        for word in words:
            if word in text_lower:
                hits.append({'word': word, 'category': category, 'source': source})
    
    return hits

def generate_report():
    """Generate alpha report"""
    print("=" * 70)
    print("🎯 ALPHA HUNTER v2")
    print(f"Scanning: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    print("=" * 70)
    
    all_hits = []
    
    # Scan RSS
    print("\n📰 CRYPTO NEWS FEEDS...")
    for name, url in RSS_FEEDS.items():
        articles = fetch_rss(name, url)
        print(f"  {name}: {len(articles)} articles")
        
        for art in articles:
            hits = scan_alpha(art['title'], name)
            if hits:
                all_hits.extend(hits)
                print(f"    🚨 {art['title'][:70]}...")
                for h in hits[:2]:
                    print(f"       → {h['word']}")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 ALPHA DETECTED")
    print("=" * 70)
    
    if all_hits:
        by_category = {}
        for h in all_hits:
            cat = h['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(h)
        
        for cat, hits in by_category.items():
            print(f"\n{cat.upper().replace('_', ' ')} ({len(hits)}):")
            seen = set()
            for h in hits:
                if h['word'] not in seen:
                    print(f"  • {h['word']} - {h['source']}")
                    seen.add(h['word'])
    else:
        print("\nNo alpha detected this scan.")
    
    print("\n" + "=" * 70)
    print("💡 TIP: Join crypto news Telegram channels")
    print("   @coindesk @Cointelegraph @theblockcrypto @decryptco")
    print("   Then I'll scan those too for real-time alpha.")
    print("=" * 70)
    
    # Log
    os.makedirs("/root/clawd/mission-control", exist_ok=True)
    with open("/root/clawd/mission-control/activity.jsonl", "a") as f:
        f.write(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "type": "alpha_hunter_v2",
            "hits": len(all_hits)
        }) + "\n")

if __name__ == "__main__":
    generate_report()
