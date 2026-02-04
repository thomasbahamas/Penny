# Crypto Trade Memo Generator 🏝️

Quick trade analysis tool for crypto tokens. Pulls fundamentals from CoinGecko and on-chain data from Birdeye.

## Setup

```bash
cd /root/clawd/projects/crypto-memo
pip install -r requirements.txt

# For Solana on-chain data (optional but recommended)
cp .env.example .env
# Edit .env and add your Birdeye API key
```

## Usage

```bash
cd src

# Basic analysis (CoinGecko only)
python analyzer.py jupiter

# With Solana on-chain data
python analyzer.py jupiter JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN

# Common tokens have built-in addresses
python analyzer.py bonk  # Will auto-resolve BONK address
```

## Known Token Addresses

Built-in Solana addresses for quick lookups:
- SOL, JUP, BONK, WIF, PYTH, JTO, RAY, ORCA

## What You Get

- **Price & Market Data**: Current price, market cap, FDV, volume
- **Supply Dynamics**: Circulating %, MCap/FDV ratio, unlock exposure
- **Chart Analysis**: 30-day range, position within range, distance from highs/lows
- **On-Chain Data** (with Birdeye): Liquidity, holders, whale concentration, security flags

## Next Steps

- [ ] Add TradingView chart screenshots
- [ ] Token unlock schedule integration
- [ ] Social sentiment (LunarCrush)
- [ ] Auto-generate trade thesis with Claude
- [ ] Export to PDF/Notion

## API Keys

- **CoinGecko**: Free tier works, no key needed
- **Birdeye**: Free tier at [birdeye.so](https://birdeye.so) - needed for on-chain data
