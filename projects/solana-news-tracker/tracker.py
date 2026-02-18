#!/usr/bin/env python3
"""Solana News Tracker - Aggregates ecosystem news for content creators"""

import json
import requests
import feedparser
from datetime import datetime, timedelta
from typing import List, Dict
import os

# RSS Feeds to monitor
RSS_FEEDS = {
    'solana_official': 'https://solana.com/news/feed.xml',
    'solana_fdn': 'https://solana.foundation/news/feed',
    # Add more as discovered:
    # 'ecosystem_blog': 'https://...',
}

# Discord webhook for alerts (set via env var)
DISCORD_WEBHOOK = os.environ.get('DISCORD_WEBHOOK_URL', '')

# Categories for auto-tagging
CATEGORIES = {
    'rwa': ['rwa', 'tokenized', 'treasury', 'real world', 'institutional', 'blackrock', 'ondo', 'wisdomtree'],
    'defi': ['defi', 'dex', 'amm', 'liquidity', 'yield', 'lending', 'borrowing'],
    'nft': ['nft', 'collectible', 'metaplex', 'compressed', 'cnft'],
    'infrastructure': ['firedancer', 'validator', 'rpc', 'client', 'network'],
    'mobile': ['seeker', 'mobile', 'sms', 'dapp store', 'solana mobile'],
    'gaming': ['game', 'gaming', 'play-to-earn', 'gamefi'],
    'ai': ['ai', 'artificial intelligence', 'ml', 'model'],
}

class SolanaNewsTracker:
    def __init__(self):
        self.articles = []
        
    def fetch_rss_feed(self, name: str, url: str) -> List[Dict]:
        """Fetch and parse an RSS feed"""
        try:
            feed = feedparser.parse(url)
            articles = []
            
            for entry in feed.entries[:10]:  # Last 10 articles
                article = {
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'published': entry.get('published', ''),
                    'summary': entry.get('summary', '')[:200] + '...',
                    'source': name,
                    'tags': self.auto_tag(entry.get('title', '') + ' ' + entry.get('summary', '')),
                }
                articles.append(article)
            
            return articles
        except Exception as e:
            print(f"Error fetching {name}: {e}")
            return []
    
    def auto_tag(self, text: str) -> List[str]:
        """Auto-tag article based on keywords"""
        text_lower = text.lower()
        tags = []
        
        for category, keywords in CATEGORIES.items():
            if any(kw in text_lower for kw in keywords):
                tags.append(category)
        
        return tags
    
    def filter_recent(self, articles: List[Dict], hours: int = 24) -> List[Dict]:
        """Filter articles from last N hours"""
        # Simple filter - in production, parse actual timestamps
        # For now, return last 5 from each source
        return articles[:5]
    
    def generate_digest(self) -> str:
        """Generate daily digest of Solana news"""
        all_articles = []
        
        for name, url in RSS_FEEDS.items():
            articles = self.fetch_rss_feed(name, url)
            all_articles.extend(articles)
        
        # Sort by published date (newest first)
        # Note: In production, parse actual timestamps
        
        digest = []
        digest.append("=" * 60)
        digest.append("🌞 SOLANA ECOSYSTEM DAILY DIGEST")
        digest.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
        digest.append("=" * 60)
        digest.append("")
        
        # Group by category
        by_category = {}
        for article in all_articles:
            tags = article.get('tags', ['general'])
            for tag in tags:
                if tag not in by_category:
                    by_category[tag] = []
                by_category[tag].append(article)
        
        # Output by category
        for category, articles in by_category.items():
            digest.append(f"\n## {category.upper().replace('_', ' ')}")
            digest.append("-" * 40)
            
            for article in articles[:3]:  # Top 3 per category
                digest.append(f"\n📰 {article['title']}")
                digest.append(f"   Source: {article['source']}")
                digest.append(f"   Link: {article['link']}")
                if article.get('summary'):
                    digest.append(f"   {article['summary']}")
        
        digest.append("\n" + "=" * 60)
        digest.append("For Thomas | SolanaFloor Content Pipeline")
        digest.append("=" * 60)
        
        return "\n".join(digest)
    
    def send_discord_alert(self, article: Dict):
        """Send Discord alert for high-priority news"""
        if not DISCORD_WEBHOOK:
            print("No Discord webhook configured")
            return
        
        # Check if high priority (RWA, major partnerships, etc.)
        high_priority_tags = ['rwa', 'infrastructure', 'major_partnership']
        if not any(tag in article.get('tags', []) for tag in high_priority_tags):
            return
        
        message = {
            "content": f"🚨 **Solana News Alert**\n\n**{article['title']}**\n{article['link']}\n\nTags: {', '.join(article.get('tags', []))}"
        }
        
        try:
            requests.post(DISCORD_WEBHOOK, json=message, timeout=10)
        except Exception as e:
            print(f"Failed to send Discord alert: {e}")
    
    def save_digest(self, digest: str, filename: str = None):
        """Save digest to file"""
        if not filename:
            date_str = datetime.now().strftime('%Y-%m-%d')
            filename = f"/root/clawd/projects/solana-news-tracker/digest-{date_str}.md"
        
        with open(filename, 'w') as f:
            f.write(digest)
        
        print(f"Digest saved to: {filename}")

def main():
    """Run the news tracker"""
    tracker = SolanaNewsTracker()
    
    print("🌙 Fetching Solana ecosystem news...")
    digest = tracker.generate_digest()
    
    print(digest)
    tracker.save_digest(digest)
    
    # In the future: Add to cron for daily runs
    # 0 7 * * * cd /root/clawd/projects/solana-news-tracker && python3 tracker.py

if __name__ == "__main__":
    main()
