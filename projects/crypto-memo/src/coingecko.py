"""CoinGecko API wrapper for token fundamentals."""
import requests
from typing import Optional
from datetime import datetime

BASE_URL = "https://api.coingecko.com/api/v3"

def get_token_data(token_id: str) -> Optional[dict]:
    """
    Fetch comprehensive token data from CoinGecko.
    token_id: CoinGecko ID (e.g., 'solana', 'jupiter-exchange-solana')
    """
    try:
        resp = requests.get(
            f"{BASE_URL}/coins/{token_id}",
            params={
                "localization": "false",
                "tickers": "true",
                "market_data": "true",
                "community_data": "true",
                "developer_data": "false",
                "sparkline": "false"
            },
            timeout=10
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Error fetching {token_id}: {e}")
        return None

def get_market_chart(token_id: str, days: int = 30) -> Optional[dict]:
    """Fetch price history for chart analysis."""
    try:
        resp = requests.get(
            f"{BASE_URL}/coins/{token_id}/market_chart",
            params={"vs_currency": "usd", "days": days},
            timeout=10
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"Error fetching chart for {token_id}: {e}")
        return None

def search_token(query: str) -> list:
    """Search for token ID by name/symbol."""
    try:
        resp = requests.get(
            f"{BASE_URL}/search",
            params={"query": query},
            timeout=10
        )
        resp.raise_for_status()
        coins = resp.json().get("coins", [])
        return [{"id": c["id"], "symbol": c["symbol"], "name": c["name"]} for c in coins[:5]]
    except Exception as e:
        print(f"Search error: {e}")
        return []

def extract_fundamentals(data: dict) -> dict:
    """Extract key metrics from CoinGecko response."""
    if not data:
        return {}
    
    market = data.get("market_data", {})
    
    return {
        "name": data.get("name"),
        "symbol": data.get("symbol", "").upper(),
        "price": market.get("current_price", {}).get("usd"),
        "market_cap": market.get("market_cap", {}).get("usd"),
        "fdv": market.get("fully_diluted_valuation", {}).get("usd"),
        "volume_24h": market.get("total_volume", {}).get("usd"),
        "circulating_supply": market.get("circulating_supply"),
        "total_supply": market.get("total_supply"),
        "max_supply": market.get("max_supply"),
        "ath": market.get("ath", {}).get("usd"),
        "ath_date": market.get("ath_date", {}).get("usd"),
        "ath_change_pct": market.get("ath_change_percentage", {}).get("usd"),
        "atl": market.get("atl", {}).get("usd"),
        "price_change_24h": market.get("price_change_percentage_24h"),
        "price_change_7d": market.get("price_change_percentage_7d"),
        "price_change_30d": market.get("price_change_percentage_30d"),
        "mcap_rank": data.get("market_cap_rank"),
        "categories": data.get("categories", []),
        "description": data.get("description", {}).get("en", "")[:500],
        "links": {
            "website": data.get("links", {}).get("homepage", [None])[0],
            "twitter": data.get("links", {}).get("twitter_screen_name"),
            "telegram": data.get("links", {}).get("telegram_channel_identifier"),
        }
    }

if __name__ == "__main__":
    # Quick test
    results = search_token("jupiter")
    print("Search results:", results)
    if results:
        data = get_token_data(results[0]["id"])
        fundamentals = extract_fundamentals(data)
        for k, v in fundamentals.items():
            print(f"{k}: {v}")
