"""Birdeye API wrapper for Solana token data."""
import requests
import os
from typing import Optional

BASE_URL = "https://public-api.birdeye.so"
API_KEY = os.environ.get("BIRDEYE_API_KEY", "")

def _headers():
    return {
        "X-API-KEY": API_KEY,
        "x-chain": "solana"
    }

def get_token_overview(address: str) -> Optional[dict]:
    """
    Fetch token overview by contract address.
    address: Solana token mint address
    """
    if not API_KEY:
        print("Warning: BIRDEYE_API_KEY not set. Get one at birdeye.so")
        return None
    
    try:
        resp = requests.get(
            f"{BASE_URL}/defi/token_overview",
            params={"address": address},
            headers=_headers(),
            timeout=10
        )
        resp.raise_for_status()
        return resp.json().get("data")
    except Exception as e:
        print(f"Birdeye error: {e}")
        return None

def get_token_security(address: str) -> Optional[dict]:
    """Fetch token security info (ownership, minting, etc.)."""
    if not API_KEY:
        return None
    
    try:
        resp = requests.get(
            f"{BASE_URL}/defi/token_security",
            params={"address": address},
            headers=_headers(),
            timeout=10
        )
        resp.raise_for_status()
        return resp.json().get("data")
    except Exception as e:
        print(f"Birdeye security error: {e}")
        return None

def get_price_history(address: str, interval: str = "1D", limit: int = 30) -> Optional[list]:
    """
    Fetch OHLCV data for chart analysis.
    interval: 1m, 5m, 15m, 1H, 4H, 1D, 1W
    """
    if not API_KEY:
        return None
    
    try:
        resp = requests.get(
            f"{BASE_URL}/defi/ohlcv",
            params={
                "address": address,
                "type": interval,
                "limit": limit
            },
            headers=_headers(),
            timeout=10
        )
        resp.raise_for_status()
        return resp.json().get("data", {}).get("items", [])
    except Exception as e:
        print(f"Birdeye OHLCV error: {e}")
        return None

def get_top_traders(address: str) -> Optional[list]:
    """Get top traders for a token."""
    if not API_KEY:
        return None
    
    try:
        resp = requests.get(
            f"{BASE_URL}/defi/v2/tokens/top_traders",
            params={"address": address, "limit": 10},
            headers=_headers(),
            timeout=10
        )
        resp.raise_for_status()
        return resp.json().get("data", {}).get("items", [])
    except Exception as e:
        print(f"Birdeye traders error: {e}")
        return None

def extract_birdeye_metrics(overview: dict, security: dict = None) -> dict:
    """Extract key on-chain metrics from Birdeye data."""
    if not overview:
        return {}
    
    metrics = {
        "name": overview.get("name"),
        "symbol": overview.get("symbol"),
        "address": overview.get("address"),
        "decimals": overview.get("decimals"),
        "price": overview.get("price"),
        "liquidity": overview.get("liquidity"),
        "volume_24h": overview.get("v24hUSD"),
        "volume_change_24h": overview.get("v24hChangePercent"),
        "trade_count_24h": overview.get("trade24h"),
        "unique_wallets_24h": overview.get("uniqueWallet24h"),
        "holder_count": overview.get("holder"),
        "price_change_24h": overview.get("priceChange24hPercent"),
        "mc": overview.get("mc"),  # market cap
        "supply": overview.get("supply"),
    }
    
    if security:
        metrics.update({
            "is_token_2022": security.get("isToken2022"),
            "owner_address": security.get("ownerAddress"),
            "creator_address": security.get("creatorAddress"),
            "mint_authority": security.get("mintAuthority"),
            "freeze_authority": security.get("freezeAuthority"),
            "top10_holder_pct": security.get("top10HolderPercent"),
        })
    
    return metrics

# Common Solana token addresses for reference
KNOWN_TOKENS = {
    "SOL": "So11111111111111111111111111111111111111112",
    "JUP": "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN",
    "BONK": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
    "WIF": "EKpQGSJtjMFqKZ9KQanSqYXRcF8fBopzLHYxdM65zcjm",
    "PYTH": "HZ1JovNiVvGrGNiiYvEozEVgZ58xaU3RKwX8eACQBCt3",
    "JTO": "jtojtomepa8beP8AuQc6eXt5FriJwfFMwQx2v2f9mCL",
    "RAY": "4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R",
    "ORCA": "orcaEKTdK7LKz57vaAYr9QeNsVEPfiu6QeMU1kektZE",
}

if __name__ == "__main__":
    # Test with JUP
    address = KNOWN_TOKENS["JUP"]
    print(f"Testing with JUP: {address}")
    overview = get_token_overview(address)
    if overview:
        metrics = extract_birdeye_metrics(overview)
        for k, v in metrics.items():
            print(f"{k}: {v}")
    else:
        print("No data - check API key")
