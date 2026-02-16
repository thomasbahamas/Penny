# Thomas Life OS - PWA Specification

## Vision
A unified dashboard that orchestrates your family life, agents, and work — all in one place. Buffalu's PWA approach but scaled to family coordination.

## Core Integrations

### 1. 📅 Calendar Layer (Unified Family)
**Sources:**
- Kids daycare calendar (Google Calendar)
- Wife's calendar (Google/Apple)
- Your work calendar
- Agent-scheduled events

**Features:**
- Conflict detection ("Kids pickup at 3pm but you have meeting")
- Auto-tagging (Work, Family, Agent Tasks)
- Shared view with wife
- Agent-curated ("Tomorrow you'll have 2 hours free at 10am")

### 2. 📧 Email Intelligence
**Sources:**
- penny.assistants@gmail.com
- thomas@solanafloor.com
- Any other accounts

**Agent Processing:**
- FED scans for macro alerts
- SCALP scans for trading opportunities
- SENTINEL scans for urgent SKRmaxing notifications
- Auto-reply suggestions
- Priority inbox (agent-curated)

### 3. 💰 Finance Dashboard
**Sources:**
- Manual entry (crypto wallets)
- Bank APIs (Plaid - optional)
- Trade history (from our logs)

**Views:**
- Portfolio allocation (BONK % warning)
- Monthly spend vs budget
- Agent-tracked positions
- Wife-shared view (optional transparency)

### 4. ✅ Shared To-Do System
**Structure:**
- Personal (your items)
- Shared (with wife)
- Agent-assigned (from FED, SCALP, etc.)
- Delegated (to agents)

**Sync:**
- Notion database (already have this)
- Mobile notifications
- Voice capture ("Add to my list: buy milk")

### 5. 🤖 Agent Command Center
Buffalu's multi-session approach:
- Visual agent status (active, standby, completed)
- Session transcripts
- Spawn/kill controls
- Resource usage

## Tech Architecture

```
/life-os-pwa
├── public/
│   ├── manifest.json
│   └── service-worker.js
├── src/
│   ├── components/
│   │   ├── Dashboard.jsx       # Main view
│   │   ├── CalendarWidget.jsx  # Unified calendar
│   │   ├── AgentHub.jsx        # Agent control center
│   │   ├── FinanceWidget.jsx   # Portfolio/chart
│   │   ├── Inbox.jsx           # Curated email
│   │   ├── TodoList.jsx        # Shared todos
│   │   └── FamilyStatus.jsx    # Kids/wife updates
│   ├── agents/
│   │   └── agent-client.js     # Agent spawn API
│   ├── sync/
│   │   ├── google-calendar.js  # GCal integration
│   │   ├── gmail.js            # Email processing
│   │   ├── notion-sync.js      # Todo sync
│   │   └── crypto-api.js       # Price/finance
│   └── storage/
│       ├── qdrant-client.js    # Memory
│       └── indexeddb.js        # Offline cache
├── api/
│   ├── agents                  # Agent endpoints
│   ├── calendar                # Calendar proxy
│   ├── email                   # Email processing
│   └── notifications           # Push notifications
└── config/
    └── integrations.json       # API keys, etc.
```

## Data Flow

```
1. External Sources → PWA Backend
   - Google Calendar (kids/wife)
   - Gmail (filter with agents)
   - Notion (shared todos)
   - CoinGecko (prices)

2. PWA Processing
   - Normalize data
   - Agent analysis
   - Conflict detection
   - Priority scoring

3. Dashboard Presentation
   - Unified timeline
   - Actionable cards
   - Family status
   - Agent work queue

4. Push Notifications
   - Urgent only
   - Agent proposals
   - Family reminders
   - Market alerts
```

## Privacy & Sharing

**With Wife:**
- Shared calendar view
- Shared todo list
- Optional finance transparency (budget, not positions)
- Agent-assisted coordination ("Find time for date night")

**Private to You:**
- Trading/secrets
- Agent research
- Business specifics
- Personal notes

## MVP Features (Week 1)

1. **Dashboard shell** — PWA installable
2. **Google Calendar integration** — show all 3 calendars
3. **Todo list** — sync with Notion
4. **Agent hub** — spawn/kill agents
5. **Push notifications** — basic alerts

## Next Week Features

1. **Gmail integration** — agent-filtered inbox
2. **Finance widget** — portfolio view
3. **Family cards** — kids schedule, wife's day
4. **Agent automation** — overnight work triggers
5. **Shared channels** — with wife in Notion/Telegram

## Security Considerations

- API keys stored server-side
- Client-side encryption for sensitive data
- Wife access tiered (optional visibility)
- Seed vault stays separate (never in PWA)
- Agent spawn requires auth

## Deployment

- Host on Vercel/Railway
- Custom domain: life.thomasbahamas.com
- SSL required (for PWA)
- Backup: GitHub repo auto-deploy

---

This becomes your single source of truth. Every domain of life, orchestrated by agents, visible in one dashboard.
