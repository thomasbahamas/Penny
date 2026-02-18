# Solana News Tracker

Automated news aggregation for Solana ecosystem content creation.

## What It Does

- Fetches latest news from Solana RSS feeds
- Auto-tags articles by category (RWA, DeFi, NFT, Infrastructure, etc.)
- Generates daily digest for content planning
- Sends Discord alerts for high-priority news (RWA, major partnerships)

## Setup

```bash
cd /root/clawd/projects/solana-news-tracker

# Optional: Set Discord webhook for alerts
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."

# Run manually
python3 tracker.py
```

## Daily Digest Output

The tool generates a daily digest organized by category:
- RWA (Real World Assets)
- DeFi
- NFT
- Infrastructure
- Mobile
- Gaming
- AI

## Automation

To run daily at 7 AM UTC:

```bash
# Add to crontab
crontab -e

# Add line:
0 7 * * * cd /root/clawd/projects/solana-news-tracker && python3 tracker.py >> /tmp/news-tracker.log 2>&1
```

## Customization

### Add More Feeds

Edit `RSS_FEEDS` in `tracker.py`:

```python
RSS_FEEDS = {
    'solana_official': 'https://solana.com/news/feed.xml',
    'your_source': 'https://...',
}
```

### Adjust Keywords

Edit `CATEGORIES` to change auto-tagging rules.

## Output Files

Daily digests saved as:
- `digest-YYYY-MM-DD.md`

Location: `/root/clawd/projects/solana-news-tracker/`

---

*Built for Thomas | SolanaFloor Content Pipeline*
