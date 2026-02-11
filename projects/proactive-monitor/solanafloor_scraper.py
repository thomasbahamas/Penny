#!/usr/bin/env python3
"""SolanaFloor content scraper for daily briefing"""
import requests
from bs4 import BeautifulSoup

def fetch_solanafloor():
    try:
        url = "https://solanafloor.com/news"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        articles = []
        for item in soup.find_all(['article', 'a'], href=True):
            title = item.get_text().strip()
            link = item['href']
            if title and len(title) > 20 and 'news' in link:
                articles.append({
                    'title': title[:80] + ('...' if len(title) > 80 else ''),
                    'url': f"https://solanafloor.com{link}" if link.startswith('/') else link
                })
                if len(articles) >= 5:
                    break
        
        if articles:
            output = "📰 Latest from SolanaFloor:\n\n"
            for i, art in enumerate(articles, 1):
                output += f"{i}. {art['title']}\n"
            return output
        return "⚠️ Could not fetch SolanaFloor"
    except Exception as e:
        return f"⚠️ SolanaFloor fetch error: {str(e)[:50]}"

if __name__ == "__main__":
    print(fetch_solanafloor())
