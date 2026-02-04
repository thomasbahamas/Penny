# Lessons

## 2026-01-31 — CoinGecko search ambiguity
**What went wrong**: Searched "jupiter", got JLP instead of JUP
**Rule**: Verify token symbol matches before proceeding

## 2026-01-31 — API rate limits
**What went wrong**: Hit CoinGecko 429 during rapid testing
**Rule**: Add delays between calls, cache when possible

## 2026-02-01 — Premature complexity
**What went wrong**: Built elaborate CLAUDE.md framework before knowing if it was needed
**Rule**: Start simple. Add structure only when you feel friction.
