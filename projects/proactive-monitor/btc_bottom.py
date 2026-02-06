#!/usr/bin/env python3
"""BTC bottom detector - alerts when conditions suggest a bottom"""
import requests
import json
from datetime import datetime

def get_btc_data():
    """Fetch BTC price and indicators from CoinGecko"""
    try:
        resp = requests.get(
            "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart",
            params={"vs_currency": "usd", "days": "30"},
            timeout=10
        )
        data = resp.json()
        prices = [p[1] for p in data.get("prices", [])]
        volumes = [v[1] for v in data.get("total_volumes", [])]
        
        current = prices[-1] if prices else 0
        high = max(prices) if prices else 0
        low = min(prices) if prices else 0
        
        # Simple RSI approximation (14-period)
        if len(prices) >= 14:
            gains = []
            losses = []
            for i in range(1, 15):
                change = prices[-i] - prices[-i-1]
                if change > 0:
                    gains.append(change)
                else:
                    losses.append(abs(change))
            avg_gain = sum(gains) / 14 if gains else 0
            avg_loss = sum(losses) / 14 if losses else 0
            rs = avg_gain / avg_loss if avg_loss else 0
            rsi = 100 - (100 / (1 + rs)) if rs else 50
        else:
            rsi = 50
        
        return {
            "price": current,
            "high_30d": high,
            "low_30d": low,
            "rsi": rsi,
            "from_ath_pct": ((current - high) / high * 100) if high else 0,
            "from_low_pct": ((current - low) / low * 100) if low else 0
        }
    except Exception as e:
        print(f"Error fetching BTC data: {e}")
        return None

def check_bottom_signals(data):
    """Check if bottom conditions are met"""
    signals = []
    
    if data["rsi"] < 20:
        signals.append(f"🚨 RSI EXTREMELY OVERSOLD: {data['rsi']:.1f}")
    elif data["rsi"] < 30:
        signals.append(f"⚠️ RSI Oversold: {data['rsi']:.1f}")
    
    if data["from_ath_pct"] < -30:
        signals.append(f"📉 Down {data['from_ath_pct']:.1f}% from ATH")
    
    if data["price"] <= data["low_30d"] * 1.05:
        signals.append(f"🎯 Near 30-day low")
    
    return signals

if __name__ == "__main__":
    data = get_btc_data()
    if data:
        signals = check_bottom_signals(data)
        if signals:
            print("🪙 BTC BOTTOM ALERT")
            print(f"Price: ${data['price']:,.2f}")
            print(f"RSI: {data['rsi']:.1f}")
            for s in signals:
                print(s)
        else:
            print(f"BTC: ${data['price']:,.2f} | RSI: {data['rsi']:.1f} | No bottom signal yet")
    else:
        print("Failed to fetch BTC data")
