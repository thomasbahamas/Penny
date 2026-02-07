#!/usr/bin/env python3
"""Trading signal scanner - technical analysis for buy/sell signals"""
import requests
import json
import os
from datetime import datetime, timedelta

# Token mapping (CoinGecko IDs and addresses)
TOKENS = {
    "BTC": {"cg_id": "bitcoin", "type": "crypto"},
    "SOL": {"cg_id": "solana", "type": "solana", "address": "So11111111111111111111111111111111111111112"},
    "BONK": {"cg_id": "bonk", "type": "solana", "address": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"},
    "SKR": {"cg_id": "seeker", "type": "solana", "address": "oreoU2P8bN6jkk3jbaiVxYnG1dCXcYxwhwyK9jSybcp"},  # Note: ore is ORE token, need SKR address
    "ORE": {"cg_id": "ore", "type": "solana", "address": "oreoU2P8bN6jkk3jbaiVxYnG1dCXcYxwhwyK9jSybcp"},
    "HYPE": {"cg_id": "hyperliquid", "type": "crypto"},  # Hyperliquid on Arbitrum
}

def get_price_data(cg_id, days=30):
    """Get price and volume data from CoinGecko"""
    try:
        resp = requests.get(
            f"https://api.coingecko.com/api/v3/coins/{cg_id}/market_chart",
            params={"vs_currency": "usd", "days": days},
            timeout=10
        )
        data = resp.json()
        prices = [p[1] for p in data.get("prices", [])]
        volumes = [v[1] for v in data.get("total_volumes", [])]
        return prices, volumes
    except Exception as e:
        print(f"Error fetching {cg_id}: {e}")
        return [], []

def calculate_rsi(prices, period=14):
    """Calculate RSI from price data"""
    if len(prices) < period + 1:
        return 50
    
    gains = []
    losses = []
    
    for i in range(1, period + 1):
        change = prices[-i] - prices[-i-1]
        if change > 0:
            gains.append(change)
        else:
            losses.append(abs(change))
    
    avg_gain = sum(gains) / period if gains else 0
    avg_loss = sum(losses) / period if losses else 0
    
    if avg_loss == 0:
        return 100
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_ma(prices, period):
    """Calculate moving average"""
    if len(prices) < period:
        return prices[-1] if prices else 0
    return sum(prices[-period:]) / period

def analyze_token(symbol, token_info):
    """Analyze a token and generate signals"""
    cg_id = token_info["cg_id"]
    prices, volumes = get_price_data(cg_id, days=30)
    
    if not prices:
        return None
    
    current_price = prices[-1]
    high_30d = max(prices)
    low_30d = min(prices)
    
    # Technical indicators
    rsi = calculate_rsi(prices)
    ma7 = calculate_ma(prices, 7)
    ma20 = calculate_ma(prices, 20)
    ma50 = calculate_ma(prices, 50) if len(prices) >= 50 else ma20
    
    # Volume analysis
    avg_volume = sum(volumes[-7:]) / 7 if len(volumes) >= 7 else 0
    recent_volume = volumes[-1] if volumes else 0
    volume_spike = (recent_volume / avg_volume) > 1.5 if avg_volume > 0 else False
    
    # Signal logic
    signals = []
    signal_strength = 0
    
    # RSI signals
    if rsi < 30:
        signals.append("🟢 RSI OVERSOLD (<30) - Potential buy zone")
        signal_strength += 2
    elif rsi < 40:
        signals.append("🟡 RSI Low - Watch for bounce")
        signal_strength += 1
    elif rsi > 70:
        signals.append("🔴 RSI OVERBOUGHT (>70) - Potential sell/avoid")
        signal_strength -= 2
    
    # Moving average signals
    if current_price > ma7 > ma20:
        signals.append("🟢 Uptrend (price > MA7 > MA20)")
        signal_strength += 1
    elif current_price < ma7 < ma20:
        signals.append("🔴 Downtrend (price < MA7 < MA20)")
        signal_strength -= 1
    
    # Golden cross / Death cross
    if ma7 > ma20 and calculate_ma(prices[:-1], 7) <= calculate_ma(prices[:-1], 20):
        signals.append("✨ Golden Cross (MA7 crossed above MA20)")
        signal_strength += 2
    elif ma7 < ma20 and calculate_ma(prices[:-1], 7) >= calculate_ma(prices[:-1], 20):
        signals.append("⚠️ Death Cross (MA7 crossed below MA20)")
        signal_strength -= 2
    
    # Support/Resistance proximity
    from_low_pct = ((current_price - low_30d) / low_30d) * 100
    from_high_pct = ((current_price - high_30d) / high_30d) * 100
    
    if from_low_pct < 10:
        signals.append(f"🎯 Near 30-day support ({from_low_pct:.1f}% from low)")
        signal_strength += 1
    elif from_high_pct > -10:
        signals.append(f"⚠️ Near 30-day resistance ({abs(from_high_pct):.1f}% from high)")
    
    # Volume spike
    if volume_spike:
        signals.append("📈 Volume spike (>1.5x avg) - Momentum building")
    
    # Final signal
    if signal_strength >= 3:
        final_signal = "🟢 STRONG BUY"
    elif signal_strength >= 1:
        final_signal = "🟡 BUY / ACCUMULATE"
    elif signal_strength <= -2:
        final_signal = "🔴 SELL / AVOID"
    elif signal_strength <= -1:
        final_signal = "🟡 WEAK / HOLD"
    else:
        final_signal = "⚪ NEUTRAL / WAIT"
    
    return {
        "symbol": symbol,
        "price": current_price,
        "rsi": rsi,
        "ma7": ma7,
        "ma20": ma20,
        "high_30d": high_30d,
        "low_30d": low_30d,
        "from_low_pct": from_low_pct,
        "from_high_pct": from_high_pct,
        "signals": signals,
        "final_signal": final_signal,
        "strength": signal_strength
    }

def generate_report():
    """Generate trading signals report"""
    print("=" * 70)
    print("🎯 TRADING SIGNALS SCANNER")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    print("=" * 70)
    
    results = []
    for symbol, info in TOKENS.items():
        print(f"\n📊 Analyzing {symbol}...", end=" ")
        result = analyze_token(symbol, info)
        if result:
            print("✓")
            results.append(result)
        else:
            print("✗ Failed")
    
    # Sort by signal strength
    results.sort(key=lambda x: x["strength"], reverse=True)
    
    print("\n" + "=" * 70)
    print("📋 SIGNALS SUMMARY")
    print("=" * 70)
    
    # Strong buy signals
    strong_buys = [r for r in results if r["strength"] >= 2]
    if strong_buys:
        print("\n🔥 STRONG OPPORTUNITIES:")
        for r in strong_buys:
            print(f"\n  {r['symbol']}: {r['final_signal']}")
            print(f"  Price: ${r['price']:.4f} | RSI: {r['rsi']:.1f}")
            print(f"  From 30d low: {r['from_low_pct']:.1f}% | From high: {r['from_high_pct']:.1f}%")
            for s in r["signals"]:
                print(f"    • {s}")
    
    # All results
    print("\n📊 ALL TOKENS:")
    for r in results:
        signal_emoji = "🟢" if r["strength"] >= 1 else "🔴" if r["strength"] <= -1 else "⚪"
        print(f"  {signal_emoji} {r['symbol']:6} | {r['final_signal']} | ${r['price']:.4f} | RSI:{r['rsi']:.0f}")
    
    # Save to activity log
    os.makedirs("/root/clawd/mission-control", exist_ok=True)
    with open("/root/clawd/mission-control/activity.jsonl", "a") as f:
        for r in results:
            f.write(json.dumps({
                "timestamp": datetime.now().isoformat(),
                "type": "trading_signal",
                "symbol": r["symbol"],
                "signal": r["final_signal"],
                "strength": r["strength"],
                "price": r["price"]
            }) + "\n")
    
    print("\n" + "=" * 70)
    print("💡 REMEMBER: Not financial advice. DYOR. These are technical signals only.")
    print("=" * 70)

if __name__ == "__main__":
    generate_report()
