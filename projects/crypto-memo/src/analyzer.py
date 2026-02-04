"""Main analyzer - combines data sources into trade memo."""
import json
from datetime import datetime
from typing import Optional
from coingecko import get_token_data, extract_fundamentals, search_token, get_market_chart
from birdeye import get_token_overview, get_token_security, extract_birdeye_metrics, KNOWN_TOKENS

def format_number(n, decimals=2):
    """Format large numbers with K/M/B suffixes."""
    if n is None:
        return "N/A"
    if n >= 1_000_000_000:
        return f"${n/1_000_000_000:.{decimals}f}B"
    if n >= 1_000_000:
        return f"${n/1_000_000:.{decimals}f}M"
    if n >= 1_000:
        return f"${n/1_000:.{decimals}f}K"
    return f"${n:.{decimals}f}"

def format_pct(p):
    """Format percentage."""
    if p is None:
        return "N/A"
    sign = "+" if p > 0 else ""
    return f"{sign}{p:.1f}%"

def calculate_supply_metrics(fundamentals: dict) -> dict:
    """Calculate supply-related metrics."""
    circ = fundamentals.get("circulating_supply")
    total = fundamentals.get("total_supply")
    max_sup = fundamentals.get("max_supply")
    
    metrics = {}
    if circ and total:
        metrics["pct_circulating"] = (circ / total) * 100
    if circ and max_sup:
        metrics["pct_of_max"] = (circ / max_sup) * 100
    if fundamentals.get("market_cap") and fundamentals.get("fdv"):
        metrics["mcap_fdv_ratio"] = fundamentals["market_cap"] / fundamentals["fdv"]
    
    return metrics

def calculate_chart_metrics(chart_data: dict) -> dict:
    """Basic technical analysis from price history."""
    if not chart_data or "prices" not in chart_data:
        return {}
    
    prices = [p[1] for p in chart_data["prices"]]
    if len(prices) < 2:
        return {}
    
    current = prices[-1]
    high_30d = max(prices)
    low_30d = min(prices)
    
    # Simple support/resistance (recent high/low)
    recent_prices = prices[-7:] if len(prices) >= 7 else prices
    
    return {
        "current_price": current,
        "high_30d": high_30d,
        "low_30d": low_30d,
        "range_position": ((current - low_30d) / (high_30d - low_30d) * 100) if high_30d != low_30d else 50,
        "from_30d_high": ((current - high_30d) / high_30d) * 100,
        "from_30d_low": ((current - low_30d) / low_30d) * 100,
    }

def generate_memo(token_query: str, solana_address: str = None) -> str:
    """
    Generate a trade memo for a token.
    
    Args:
        token_query: CoinGecko search term (e.g., 'jupiter', 'bonk')
        solana_address: Optional Solana mint address for on-chain data
    """
    memo_lines = []
    memo_lines.append("=" * 60)
    memo_lines.append(f"CRYPTO TRADE MEMO | {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    memo_lines.append("=" * 60)
    
    # Search and fetch CoinGecko data
    search_results = search_token(token_query)
    if not search_results:
        return f"Token '{token_query}' not found on CoinGecko."
    
    token_id = search_results[0]["id"]
    raw_data = get_token_data(token_id)
    fundamentals = extract_fundamentals(raw_data)
    
    if not fundamentals.get("name"):
        return f"Could not fetch data for {token_query}"
    
    # Header
    memo_lines.append(f"\n## {fundamentals['name']} ({fundamentals['symbol']})")
    memo_lines.append(f"Rank: #{fundamentals.get('mcap_rank', 'N/A')}")
    if fundamentals.get("categories"):
        memo_lines.append(f"Categories: {', '.join(fundamentals['categories'][:3])}")
    
    # Price & Market Data
    memo_lines.append(f"\n### 💰 PRICE & MARKET DATA")
    memo_lines.append(f"Price: ${fundamentals.get('price', 0):.6f}")
    memo_lines.append(f"Market Cap: {format_number(fundamentals.get('market_cap'))}")
    memo_lines.append(f"FDV: {format_number(fundamentals.get('fdv'))}")
    memo_lines.append(f"24h Volume: {format_number(fundamentals.get('volume_24h'))}")
    
    # Price changes
    memo_lines.append(f"\n24h: {format_pct(fundamentals.get('price_change_24h'))} | 7d: {format_pct(fundamentals.get('price_change_7d'))} | 30d: {format_pct(fundamentals.get('price_change_30d'))}")
    
    # ATH/ATL
    memo_lines.append(f"\nATH: ${fundamentals.get('ath', 0):.6f} ({format_pct(fundamentals.get('ath_change_pct'))} from ATH)")
    
    # Supply Metrics
    memo_lines.append(f"\n### 📊 SUPPLY DYNAMICS")
    memo_lines.append(f"Circulating: {fundamentals.get('circulating_supply', 0):,.0f}")
    memo_lines.append(f"Total Supply: {fundamentals.get('total_supply', 0):,.0f}")
    if fundamentals.get('max_supply'):
        memo_lines.append(f"Max Supply: {fundamentals.get('max_supply', 0):,.0f}")
    
    supply_metrics = calculate_supply_metrics(fundamentals)
    if supply_metrics.get("pct_circulating"):
        memo_lines.append(f"% Circulating: {supply_metrics['pct_circulating']:.1f}%")
    if supply_metrics.get("mcap_fdv_ratio"):
        memo_lines.append(f"MCap/FDV Ratio: {supply_metrics['mcap_fdv_ratio']:.2f}")
    
    # Chart Analysis
    chart_data = get_market_chart(token_id, days=30)
    chart_metrics = calculate_chart_metrics(chart_data)
    if chart_metrics:
        memo_lines.append(f"\n### 📈 CHART ANALYSIS (30D)")
        memo_lines.append(f"30D High: ${chart_metrics.get('high_30d', 0):.6f}")
        memo_lines.append(f"30D Low: ${chart_metrics.get('low_30d', 0):.6f}")
        memo_lines.append(f"Range Position: {chart_metrics.get('range_position', 0):.0f}% (0=low, 100=high)")
        memo_lines.append(f"From 30D High: {format_pct(chart_metrics.get('from_30d_high'))}")
        memo_lines.append(f"From 30D Low: {format_pct(chart_metrics.get('from_30d_low'))}")
    
    # Birdeye on-chain data (if Solana address provided)
    if solana_address:
        overview = get_token_overview(solana_address)
        security = get_token_security(solana_address)
        birdeye_metrics = extract_birdeye_metrics(overview, security)
        
        if birdeye_metrics:
            memo_lines.append(f"\n### 🔗 ON-CHAIN DATA (SOLANA)")
            memo_lines.append(f"Liquidity: {format_number(birdeye_metrics.get('liquidity'))}")
            memo_lines.append(f"24h Trades: {birdeye_metrics.get('trade_count_24h', 'N/A'):,}")
            memo_lines.append(f"Unique Wallets 24h: {birdeye_metrics.get('unique_wallets_24h', 'N/A'):,}")
            memo_lines.append(f"Holders: {birdeye_metrics.get('holder_count', 'N/A'):,}")
            if birdeye_metrics.get('top10_holder_pct'):
                memo_lines.append(f"Top 10 Holder %: {birdeye_metrics['top10_holder_pct']:.1f}%")
            if birdeye_metrics.get('mint_authority'):
                memo_lines.append(f"⚠️ Mint Authority: Active")
            if birdeye_metrics.get('freeze_authority'):
                memo_lines.append(f"⚠️ Freeze Authority: Active")
    
    # Links
    links = fundamentals.get("links", {})
    memo_lines.append(f"\n### 🔗 LINKS")
    if links.get("website"):
        memo_lines.append(f"Website: {links['website']}")
    if links.get("twitter"):
        memo_lines.append(f"Twitter: @{links['twitter']}")
    
    # Trade Notes Section (to be filled manually or by Claude)
    memo_lines.append(f"\n### 📝 TRADE NOTES")
    memo_lines.append("Entry: ")
    memo_lines.append("Target 1: ")
    memo_lines.append("Target 2: ")
    memo_lines.append("Stop Loss: ")
    memo_lines.append("Thesis: ")
    memo_lines.append("Catalysts: ")
    memo_lines.append("Risks: ")
    
    memo_lines.append("\n" + "=" * 60)
    memo_lines.append("Generated by Crypto Memo Tool | Not financial advice")
    memo_lines.append("=" * 60)
    
    return "\n".join(memo_lines)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <token_name> [solana_address]")
        print("Example: python analyzer.py jupiter JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN")
        sys.exit(1)
    
    token = sys.argv[1]
    address = sys.argv[2] if len(sys.argv) > 2 else KNOWN_TOKENS.get(token.upper())
    
    memo = generate_memo(token, address)
    print(memo)
