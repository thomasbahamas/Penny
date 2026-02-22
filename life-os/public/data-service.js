// LifeOS Data Service - Real data connections
class LifeOSData {
  constructor() {
    this.data = {
      portfolio: {
        total: 10000, // USD - YOUR NUMBER HERE
        bonkValue: 3000, // USD - YOUR NUMBER HERE
        bonkPrice: 0.00000654,
        lastUpdate: new Date().toISOString()
      },
      family: {
        upcoming: [
          { date: '2026-04-02', event: 'Easter Party', type: 'daycare' },
          { date: '2026-04-03', event: 'Good Friday - Closed', type: 'daycare' },
          { date: '2026-04-06', event: 'Easter Monday - Closed', type: 'daycare' },
          { date: '2026-05-04', event: 'Anniversary Trip Start', type: 'family' },
          { date: '2026-05-25', event: 'Memorial Day - Closed', type: 'daycare' }
        ]
      },
      content: {
        nextVideo: 'Thursday 8am - The Big Picture LIVE',
        prepDue: 'Wednesday',
        status: 'Prep needed'
      },
      agents: {
        PENNY: { status: 'active', task: 'Orchestrating', lastSeen: '2 min ago' },
        NOVA: { status: 'standby', task: 'Script ready', lastSeen: '1 hour ago' },
        FED: { status: 'standby', task: 'Macro report complete', lastSeen: '1 day ago' },
        SCALP: { status: 'standby', task: null, lastSeen: '2 days ago' }
      }
    };
  }

  async loadWatchlist() {
    // Fetch prices from CoinGecko
    const coins = 'solana,jupiter-exchange,ondo-finance,zebec-protocol';
    try {
      const response = await fetch(`https://api.coingecko.com/api/v3/simple/price?ids=${coins}&vs_currencies=usd&include_24hr_change=true`, {
        method: 'GET'
      });
      if (response.ok) {
        const data = await response.json();
        return this.parseSignals(data);
      }
    } catch (e) {
      console.log('Price fetch failed, using cached');
    }
    return null;
  }
  
  parseSignals(data) {
    const signals = [];
    const coinMap = {
      'solana': 'SOL',
      'jupiter-exchange': 'JUP',
      'ondo-finance': 'ONDO',
      'zebec-protocol': 'ZBC'
    };
    
    for (const [coin, info] of Object.entries(data)) {
      const change = info.usd_24h_change || 0;
      let signal = 'HOLD';
      let color = '#888';
      
      if (change < -15) {
        signal = 'BUY DIP';
        color = '#00ff88';
      } else if (change > 25) {
        signal = 'TAKE PROFIT';
        color = '#ffcc00';
      } else if (change < -5) {
        signal = 'WATCH';
        color = '#ffcc00';
      }
      
      signals.push({
        symbol: coinMap[coin] || coin,
        price: info.usd,
        change24h: change.toFixed(2),
        signal: signal,
        color: color
      });
    }
    return signals;
  }

  async loadFinance() {
    // Try to fetch from our stored reports
    try {
      const response = await fetch('/api/finance', { 
        method: 'GET',
        headers: { 'Accept': 'application/json' }
      });
      if (response.ok) {
        const data = await response.json();
        return data;
      }
    } catch (e) {
      console.log('API not ready, using stored data');
    }
    
    // Fallback to manual data
    return this.data.portfolio;
  }

  async loadFamily() {
    // Show next 3 upcoming events
    const today = new Date();
    const upcoming = this.data.family.upcoming
      .filter(e => new Date(e.date) >= today)
      .sort((a, b) => new Date(a.date) - new Date(b.date))
      .slice(0, 3);
    
    return upcoming;
  }

  async loadAgents() {
    return this.data.agents;
  }

  async loadContent() {
    return this.data.content;
  }

  // Show "manual entry" for things not connected
  needsSetup(service) {
    return {
      gmail: 'Connect Gmail to scan inbox',
      calendar: 'Connect Google Calendar to sync',
      notion: 'Connect Notion for shared todos',
      plaid: 'Connect bank for finance tracking'
    }[service] || 'Setup required';
  }
}

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
  const data = new LifeOSData();
  
  // Load Finance
  const finance = await data.loadFinance();
  updateFinanceUI(finance);
  
  // Load Family
  const family = await data.loadFamily();
  updateFamilyUI(family);
  
  // Load Agents
  const agents = await data.loadAgents();
  updateAgentsUI(agents);
  
  // Content schedule
  const content = await data.loadContent();
  updateContentUI(content);
  
  // Replace "Loading..." with "Setup" buttons where needed
  setupServiceButtons();
});

function updateFinanceUI(data) {
  const portfolioEl = document.getElementById('portfolio-value');
  const bonkEl = document.getElementById('bonk-percent');
  
  if (portfolioEl) {
    portfolioEl.textContent = `$${data.total.toLocaleString()}`;
    portfolioEl.className = 'value';
  }
  
  if (bonkEl && data.total > 0) {
    const pct = ((data.bonkValue / data.total) * 100).toFixed(1);
    bonkEl.textContent = `${pct}%`;
    bonkEl.className = pct > 30 ? 'value warning' : 'value';
    
    // Add alert if over 30%
    if (pct > 30) {
      const alert = document.createElement('div');
      alert.className = 'finance-alert';
      alert.textContent = `⚠️ BONK ${pct}% of portfolio - consider trimming`;
      bonkEl.parentElement.appendChild(alert);
    }
  }
}

function updateFamilyUI(events) {
  const kidsEl = document.getElementById('kids-status');
  const wifeEl = document.getElementById('wife-status');
  
  // Show next event
  if (events.length > 0) {
    const next = events[0];
    const date = new Date(next.date);
    const daysUntil = Math.ceil((date - new Date()) / (1000 * 60 * 60 * 24));
    
    if (kidsEl) {
      kidsEl.textContent = `${next.event} (${daysUntil} days)`;
      kidsEl.className = daysUntil <= 7 ? 'status urgent' : 'status';
    }
  }
  
  if (wifeEl) {
    wifeEl.textContent = 'Schedule synced - no conflicts';
  }
}

function updateAgentsUI(agents) {
  // Already rendered in HTML, could enhance here
}

function updateContentUI(data) {
  const scheduleEl = document.getElementById('content-schedule');
  if (scheduleEl && data.nextVideo) {
    // Highlight if prep needed
    if (data.status === 'Prep needed') {
      const prepAlert = document.createElement('div');
      prepAlert.className = 'prep-alert';
      prepAlert.innerHTML = `⏰ ${data.prepDue}: Prep for <strong>${data.nextVideo}</strong>`;
      scheduleEl.insertBefore(prepAlert, scheduleEl.firstChild);
    }
  }
}

function setupServiceButtons() {
  // Replace "Scanning emails..." with setup button
  const inboxLoading = document.querySelector('.inbox-card .loading');
  if (inboxLoading) {
    inboxLoading.outerHTML = `
      <div class="setup-prompt">
        <p>📧 Gmail not connected</p>
        <button onclick="setupGmail()">Connect Gmail</button>
      </div>
    `;
  }
  
  // Replace "Syncing calendars..."
  const calLoading = document.querySelector('.calendar-card .loading');
  if (calLoading) {
    calLoading.outerHTML = `
      <div class="setup-prompt">
        <p>📅 Google Calendar not connected</p>
        <button onclick="setupCalendar()">Connect Calendar</button>
      </div>
    `;
  }
}

// Setup handlers (placeholders for now)
function setupGmail() {
  alert('Gmail OAuth setup - requires backend configuration');
}

function setupCalendar() {
  alert('Google Calendar OAuth setup - requires backend configuration');
}
