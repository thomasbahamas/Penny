// LifeOS App - Thomas's Personal Dashboard

class LifeOS {
  constructor() {
    this.agents = {
      PENNY: { status: 'active', task: 'Orchestrating' },
      NOVA: { status: 'standby', task: null },
      FED: { status: 'standby', task: null },
      SCALP: { status: 'standby', task: null },
      SCRIBE: { status: 'standby', task: null },
      ATLAS: { status: 'standby', task: null }
    };
    this.init();
  }

  init() {
    this.updateClock();
    setInterval(() => this.updateClock(), 1000);
    this.renderAgents();
    this.loadSchedule();
    this.checkConflicts();
  }

  updateClock() {
    const now = new Date();
    document.getElementById('clock').textContent = 
      now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
  }

  renderAgents() {
    const grid = document.getElementById('agent-grid');
    if (!grid) return;
    
    grid.innerHTML = Object.entries(this.agents).map(([name, data]) => `
      <div class="agent-tile ${data.status}">
        <span class="agent-icon">${this.getAgentIcon(name)}</span>
        <span class="agent-name">${name}</span>
        <span class="agent-status">${data.status}</span>
        ${data.task ? `<span class="agent-task">${data.task}</span>` : ''}
      </div>
    `).join('');
  }

  getAgentIcon(name) {
    const icons = {
      PENNY: '🦞', NOVA: '🎬', FED: '🌍', 
      SCALP: '⚡', SCRIBE: '✍️', ATLAS: '📊'
    };
    return icons[name] || '🤖';
  }

  async spawnAgent(agentName) {
    // Update UI
    if (this.agents[agentName]) {
      this.agents[agentName].status = 'running';
      this.agents[agentName].task = 'Initializing...';
      this.renderAgents();
    }

    // Send to Telegram for actual spawn
    await this.notifyTelegram(`Spawn ${agentName} for Thomas`);
    
    alert(`${agentName} spawning... Check Telegram for results.`);
  }

  async notifyTelegram(message) {
    // This would call your Telegram bot API
    console.log('Telegram:', message);
  }

  loadSchedule() {
    const today = new Date().getDay();
    const schedule = {
      1: { // Monday
        content: 'Research hottest topics for Video #1',
        agent: 'ATLAS',
        prep: 'Thu Big Picture Livestream'
      },
      2: { // Tuesday
        content: 'Shoot Video #1 (trending topic)',
        agent: 'NOVA',
        prep: 'Edit and schedule'
      },
      3: { // Wednesday
        content: 'Shoot Video #2 (2nd trending topic)',
        agent: 'NOVA',
        prep: 'Fri Solana Weekly prep'
      },
      4: { // Thursday
        content: '🔴 The Big Picture LIVE at 8am',
        agent: 'LIVE',
        prep: 'Script ready, camera check'
      },
      5: { // Friday
        content: '🔴 Solana Weekly LIVE at 8am',
        agent: 'LIVE',
        prep: 'Weekly recap prepared'
      },
      6: { // Saturday
        content: 'Review analytics, plan next week',
        agent: 'ANALYSIS',
        prep: 'Rest + family time'
      },
      0: { // Sunday
        content: 'Prep for week ahead',
        agent: 'PLANNING',
        prep: 'Check trending topics'
      }
    };

    const dayPlan = schedule[today];
    if (dayPlan) {
      this.showTodayFocus(dayPlan);
    }
  }

  showTodayFocus(plan) {
    const familyCard = document.querySelector('.family-card');
    if (familyCard) {
      const workDiv = document.createElement('div');
      workDiv.className = 'work-priority';
      workDiv.innerHTML = `
        <h3>🎥 Today's Focus</h3>
        <p><strong>${plan.content}</strong></p>
        <p>Agent: ${plan.agent} | Prep: ${plan.prep}</p>
      `;
      familyCard.appendChild(workDiv);
    }
  }

  checkConflicts() {
    // Check for calendar conflicts
    // Example: Kids pickup vs livestream prep
    const conflicts = [];
    
    // This would integrate with Google Calendar API
    // For now, placeholder logic
    
    if (conflicts.length > 0) {
      document.getElementById('conflicts').innerHTML = conflicts.map(c => `
        <div class="conflict-alert">⚠️ ${c}</div>
      `).join('');
    }
  }
}

// Content Schedule Functions
function generateTopics() {
  alert('Spawning ATLAS to find hottest Solana topics...');
  // This would trigger agent research
  setTimeout(() => {
    document.getElementById('topic-1').textContent = 'x402 Protocol - 75M transactions';
    document.getElementById('topic-2').textContent = 'Solana RWA Institutional Migration';
  }, 2000);
}

function spawnNOVA() {
  alert('Spawning NOVA for video production planning...');
}

// Other functions
function refreshCalendars() {
  alert('Syncing Google Calendars...');
}

function addTodo() {
  const input = document.getElementById('new-todo');
  if (input.value) {
    alert(`Added shared todo: ${input.value}`);
    input.value = '';
  }
}

function startVoiceCapture() {
  alert('Voice capture starting... (Integration needed)');
}

function requestNotificationPermission() {
  if ('Notification' in window) {
    Notification.requestPermission();
  }
}

function showView(view) {
  console.log('Switching to view:', view);
}

// Initialize
const lifeOS = new LifeOS();

// Service Worker for offline
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/service-worker.js')
    .then(reg => console.log('SW registered'))
    .catch(err => console.log('SW error:', err));
}

// Push notification handler
function showPushNotification(title, body) {
  if (Notification.permission === 'granted') {
    new Notification(title, { body });
  }
}
