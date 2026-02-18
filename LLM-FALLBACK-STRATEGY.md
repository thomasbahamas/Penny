# Multi-Provider LLM Fallback Strategy

## Current Setup
- **Primary:** Kimi K2.5 (OpenRouter) - $0
- **Status:** Credits depleted, needs fallback

## Your Subscriptions (All Added)

| Provider | Model | Cost | Use Case |
|----------|-------|------|----------|
| **OpenAI** | GPT-4o | $2.50/M | Vision, reliability |
| **OpenAI** | GPT-4o-mini | $0.15/M | Cheap fallback |
| **Claude** | Sonnet 4.6 | $3/M | Computer use, reasoning |
| **Claude** | Opus 4.5 | $15/M | Deep analysis |
| **Grok** | Grok-2 | $2/M | X data, real-time |
| **Gemini** | 2.0 Flash | $0.10/M | Ultra cheap, 1M context |

## Fallback Chain (Auto-Switch)

```
1. Kimi K2.5 (OpenRouter) → FREE/$1M
   ↓ (if credits depleted)
2. Gemini 2.0 Flash → $0.10/M (cheapest)
   ↓ (if rate limited)
3. GPT-4o-mini → $0.15/M (reliable)
   ↓ (if needs reasoning)
4. Claude Sonnet 4.6 → $3/M (best reasoning)
   ↓ (if needs X data)
5. Grok-2 → $2/M (real-time X)
   ↓ (if all else fails)
6. GPT-4o → $2.50/M (most reliable)
```

## Cost-Optimized Strategy

**Daily Brief / Routine:**
- Gemini Flash ($0.10/M) - 90% of tasks
- GPT-4o-mini ($0.15/M) - if Gemini fails

**Complex Tasks / Coding:**
- Claude Sonnet 4.6 ($3/M)
- GPT-4o ($2.50/M) - final fallback

**Real-time / X Data:**
- Grok-2 ($2/M) - only when needed

## Monthly Budget Estimate

| Scenario | Cost |
|----------|------|
| Light usage (Gemini mostly) | $5-10 |
| Medium (mix) | $20-50 |
| Heavy (Claude/4o) | $100-200 |

## Implementation

Add to OpenClaw config:
- All providers with API keys
- Cost-based priority ordering
- Auto-fallback on errors

Next: Set up API keys for each service
