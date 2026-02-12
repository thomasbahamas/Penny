#!/usr/bin/env python3
"""SolanaFloor content scraper - lightweight version"""
import requests
import re
from datetime import datetime

def fetch_solanafloor():
    """Fetch latest articles from SolanaFloor"""
    try:
        url = "https://solanafloor.com/news"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        resp = requests.get(url, headers=headers, timeout=15)
        html = resp.text
        
        # Extract article titles and links
        articles = []
        
        # Look for article links with /news/ pattern
        pattern = r'href="(/news/[^"]+)"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern, html)
        
        seen = set()
        for link, title in matches[:8]:  # Get first 8 unique
            title = title.strip()
            if title and len(title) > 10 and title not in seen:
                seen.add(title)
                articles.append({
                    'title': title[:80] + ('...' if len(title) > 80 else ''),
                    'url': f"https://solanafloor.com{link}"
                })
        
        if articles:
            output = "🏛️ Latest from SolanaFloor:\n\n"
            for i, art in enumerate(articles[:5], 1):
                output += f"{i}. {art['title']}\n"
            return output
            
        return "⚠️ Could not fetch SolanaFloor articles"
        
    except Exception as e:
        return f"⚠️ SolanaFloor error: {str(e)[:50]}"

def fetch_solana_twitter_highlights():
    """Curated highlights from key Solana Twitter accounts"""
    # Since we can't scrape Twitter easily, provide framework
    return """
🐦 Key Solana Twitter Accounts to Monitor:
   • @solana - Official updates
   • @aeyakovenko - Toly's insights  
   • @SolanaFloor - Ecosystem news
   • @pumpdotfun - Meme coin trends
   • @JupiterExchange - DeFi updates

💡 Tip: Set up Twitter lists for these accounts
"""

def fetch_on_chain_metrics():
    """Fetch key Solana on-chain metrics"""
    try:
        # Try to get simple price data from CoinGecko
        url = "https://api.coingecko.com/api/v3/coins/solana?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        
        price = data['market_data']['current_price']['usd']
        change_24h = data['market_data']['price_change_percentage_24h']
        change_30d = data['market_data']['price_change_percentage_30d_in_currency']['usd']
        
        return f"""
📊 SOL On-Chain Snapshot:
   Price: ${price:.2f}
   24h Change: {change_24h:+.1f}%
   30d Change: {change_30d:+.1f}%
"""
    except:
        return "📊 SOL: Price data unavailable"

if __name__ == "__main__":
    print(fetch_solanafloor())
    print(fetch_solana_twitter_highlights())
    print(fetch_on_chain_metrics())
