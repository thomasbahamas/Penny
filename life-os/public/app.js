// Life OS - Main Application
// Connects to existing infrastructure: Qdrant, Notion, agents, etc.

const API_BASE = '/api'; // Will proxy to backend

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
  initClock();
  loadData();
  setupNotifications();
});

// Clock
function initClock() {
  const update = () => {
    const now = new Date();
    document.getElementById('clock').textContent = 
      now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
  };
  update();
  setInterval(update, 1000);
}

// Load all data
async function loadData() {
  await Promise.all([
    loadFamilyStatus(),
    loadCalendar(),
    loadAgents(),
    loadInbox(),
    loadFinance(),
    loadTodos()
  ]);
}

// Family Status
async function loadFamilyStatus() {
  try {
    // This would integrate with Google Calendar API
    // For now, showing placeholder
    document.getElementById('kids-status').textContent = 'School until 3pm';
    document.getElementById('wife-status').textContent = 'Work meetings';
    
    // Check for conflicts
    const conflicts = checkConflicts();
    if (conflicts.length > 0) {
      document.getElementById('conflicts').innerHTML = conflicts.map(c => 
        `<div class="alert">⚠️ ${c}</div>`
      ).join('');
    }
  } catch (e) {
    console.error('Family status error:', e);
  }
}

function checkConflicts() {
  // Agent would analyze calendars for conflicts
  const conflicts = [];
  
  // Example conflict detection
  const now = new Date();
  if (now.getHours() === 14) {
    conflicts.push("Kids pickup in 1 hour but you have a meeting");
  }
  
  return conflicts;
}

// Calendar Integration
async function loadCalendar() {
  try {
    // Would fetch from Google Calendar API
    // For now, mock data showing structure
    const events = [
      { time: '9:00', title: 'Morning standup', source: 'Work' },
      { time: '11:00', title: 'Agent briefing with FED', source: 'Agent' },
      { time: '15:00', title: 'Kids pickup', source: 'Family' },
      { time: '19:00', title: 'Dinner with family', source: 'Family' }
    ];
    
    const html = events.map(e => `
      <div class="calendar-event">
        <span class="event-time">${e.time}</span>
        <span class="event-title">${e.title}</span>
        <span class="event-source">${e.source}</span>
      </div>
    `).join('');
    
    document.getElementById('calendar-widget').innerHTML = html;
  } catch (e) {
    console.error('Calendar error:', e);
  }
}

function refreshCalendars() {
  document.getElementById('calendar-widget').innerHTML = '<div class="loading">Refreshing...</div>';
  setTimeout(loadCalendar, 1000);
}

// Agent Hub
const AGENTS = [
  { id: 'PENNY', name: 'PENNY', icon: '🦞', role: 'Orchestrator', status: 'active' },
  { id: 'NOVA', name: 'NOVA', icon: '🎬', role: 'Video', status: 'standby' },
  { id: 'FED', name: 'FED', icon: '🌍', role: 'Macro', status: 'standby' },
  { id: 'SCALP', name: 'SCALP', icon: '⚡', role: 'Trading', status: 'standby' },
  { id: 'SCRIBE', name: 'SCRIBE', icon: '✍️', role: 'Copy', status: 'standby' },
  { id: 'ATLAS', name: 'ATLAS', icon: '📊', role: 'Research', status: 'standby' },
  { id: 'PIXEL', name: 'PIXEL', icon: '🎨', role: 'Design', status: 'standby' }
];

function loadAgents() {
  const html = AGENTS.map(a => `
    <div class="agent-item ${a.status}">
      <div>${a.icon}</div>
      <div>${a.name}</div>
      <div style="font-size: 10px; color: #666">${a.role}</div>
    </div>
  `).join('');
  
  document.getElementById('agent-grid').innerHTML = html;
}

async function spawnAgent(agentId) {
  // Update UI
  const agent = AGENTS.find(a => a.id === agentId);
  if (agent) {
    agent.status = 'active';
    loadAgents();
    
    // In real implementation, this would call your OpenClaw API
    // sessions_spawn(agentId, task, ...)
    alert(`Spawning ${agentId}... In real version, this connects to your OpenClaw backend`);
    
    // Simulate completion
    setTimeout(() => {
      agent.status = 'standby';
      loadAgents();
    }, 3000);
  }
}

// Smart Inbox
async function loadInbox() {
  try {
    // Would integrate with Gmail API + agent filtering
    const emails = [
      { from: 'FED Agent', subject: 'Macro outlook: Soft landing confirmed', priority: 'high', unread: true },
      { from: 'Notion', subject: 'Daily briefing synced', priority: 'low', unread: false },
      { from: 'SKRmaxing', subject: 'Trade proposal: SOL at $80', priority: 'high', unread: true }
    ];
    
    const unreadCount = emails.filter(e => e.unread).length;
    document.getElementById('unread-count').textContent = unreadCount > 0 ? `(${unreadCount})` : '';
    
    const html = emails.map(e => `
      <div class="calendar-event" style="${e.unread ? 'font-weight: bold;' : ''}">
        <span class="event-title">${e.from}: ${e.subject}</span>
        ${e.priority === 'high' ? '<span style="color: #ff6b35">●</span>' : ''}
      </div>
    `).join('');
    
    document.getElementById('inbox-list').innerHTML = html;
  } catch (e) {
    console.error('Inbox error:', e);
  }
}

// Finance
async function loadFinance() {
  try {
    // Would integrate with your crypto APIs
    document.getElementById('portfolio-value').textContent = '$47,500';
    document.getElementById('bonk-percent').textContent = '42%';
    
    // Alerts
    const alerts = [
      '⚠️ BONK >40% of portfolio - consider rebalancing',
      '📈 SOL showing support at $80'
    ];
    
    document.getElementById('finance-alerts').innerHTML = alerts.map(a => 
      `<div class="alert">${a}</div>`
    ).join('');
  } catch (e) {
    console.error('Finance error:', e);
  }
}

// Shared Todos (Notion Integration)
async function loadTodos() {
  try {
    // Would fetch from Notion database
    const todos = [
      { text: 'Review FED macro analysis', shared: false, done: false },
      { text: 'Pick up milk', shared: true, done: false },
      { text: 'Script x402 video', shared: false, done: true }
    ];
    
    const html = todos.map(t => `
      <div class="todo-item ${t.shared ? 'shared' : ''}">
        <input type="checkbox" ${t.done ? 'checked' : ''}>
        <span style="${t.done ? 'text-decoration: line-through; opacity: 0.5' : ''}">${t.text}</span>
      </div>
    `).join('');
    
    document.getElementById('todo-list').innerHTML = html;
  } catch (e) {
    console.error('Todos error:', e);
  }
}

async function addTodo() {
  const input = document.getElementById('new-todo');
  const text = input.value.trim();
  if (!text) return;
  
  // Would sync to Notion
  // notion_sync.add_content_idea(text, ...)
  
  // Add to UI immediately
  const div = document.createElement('div');
  div.className = 'todo-item shared';
  div.innerHTML = `
    <input type="checkbox">
    <span>${text}</span>
  `;
  document.getElementById('todo-list').appendChild(div);
  
  input.value = '';
  
  // Background sync
  setTimeout(() => {
    showNotification('Todo synced', 'Shared with wife via Notion');
  }, 1000);
}

// Voice Capture
function startVoiceCapture() {
  if (!('webkitSpeechRecognition' in window)) {
    alert('Voice capture not supported on this device');
    return;
  }
  
  const recognition = new webkitSpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;
  
  recognition.onresult = (event) => {
    const text = event.results[0][0].transcript;
    document.getElementById('captured-items').innerHTML += `
      <div style="padding: 8px; background: #1a1a2e; margin: 4px 0; border-radius: 4px;">
        🎤 "${text}"
      </div>
    `;
    
    // Auto-categorize with agents
    categorizeCapture(text);
  };
  
  recognition.start();
}

function categorizeCapture(text) {
  // Simple keyword matching (agent would do better)
  if (text.includes('buy') || text.includes('trade')) {
    showNotification('Captured', 'Trade idea sent to SCALP');
  } else if (text.includes('kids') || text.includes('pickup')) {
    showNotification('Captured', 'Family task added');
  } else {
    showNotification('Captured', 'Added to todo list');
  }
}

// Notifications
function setupNotifications() {
  if ('Notification' in window) {
    Notification.requestPermission();
  }
}

function requestNotificationPermission() {
  if ('Notification' in window) {
    Notification.requestPermission().then(permission => {
      if (permission === 'granted') {
        showNotification('Notifications enabled', 'You\'ll get alerts for urgent items');
      }
    });
  }
}

function showNotification(title, body) {
  if ('Notification' in window && Notification.permission === 'granted') {
    new Notification(title, { body, icon: '/icon-192.png' });
  }
  
  // Also show in-app toast
  console.log(`[Notification] ${title}: ${body}`);
}

// Navigation
function showView(view) {
  document.querySelectorAll('.bottom-nav button').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
  
  // In full app, this would switch views
  console.log(`Switching to ${view}`);
}

// Background sync (when back online)
window.addEventListener('online', () => {
  document.getElementById('sync-status').textContent = '🟢';
  loadData(); // Refresh all data
});

window.addEventListener('offline', () => {
  document.getElementById('sync-status').textContent = '🔴';
});
