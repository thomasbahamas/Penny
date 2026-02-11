const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8765;

function parseTodoFile(content) {
    const incomplete = [];
    const active = [];
    const blocked = [];
    
    const lines = content.split('\n');
    let section = null;
    
    for (const line of lines) {
        if (line.includes('## In Progress')) section = 'active';
        else if (line.includes('## Backlog')) section = 'backlog';
        else if (line.includes('## Completed')) section = 'done';
        
        if (line.startsWith('- [ ]')) {
            const task = line.replace('- [ ]', '').trim();
            if (task.includes('needs') || task.includes('pending')) {
                blocked.push({
                    title: task.split('—')[0].trim(),
                    desc: task.split('—')[1]?.trim() || 'Needs attention',
                    workaround: 'Check dependencies'
                });
            } else {
                incomplete.push({
                    title: task.split('—')[0].trim(),
                    desc: task.split('—')[1]?.trim() || 'In progress',
                    status: 'active'
                });
            }
        }
    }
    
    return { incomplete, active, blocked };
}

function getDashboardData() {
    const data = {
        incomplete: [],
        active: [],
        blocked: [],
        notes: '',
        gitActivity: []
    };
    
    // Read todo.md
    try {
        const todo = fs.readFileSync('/root/clawd/tasks/todo.md', 'utf8');
        const parsed = parseTodoFile(todo);
        data.incomplete = parsed.incomplete;
        data.active = parsed.active;
        data.blocked = parsed.blocked;
    } catch (e) {
        console.error('Error reading todo:', e.message);
    }
    
    // Read today's memory
    try {
        const today = new Date().toISOString().split('T')[0];
        const memory = fs.readFileSync(`/root/clawd/memory/${today}.md`, 'utf8');
        data.notes = memory.substring(0, 500) + '...';
    } catch (e) {
        data.notes = 'No memory file for today';
    }
    
    // Read git activity
    try {
        const gitLog = require('child_process').execSync('cd /root/clawd && git log --oneline -10', { encoding: 'utf8' });
        data.gitActivity = gitLog.split('\n').filter(Boolean);
    } catch (e) {
        data.gitActivity = ['Git log unavailable'];
    }
    
    // Add hardcoded active projects from context
    data.active.push(
        { title: 'Context Retention System', desc: 'FAISS + hourly summarizer', status: 'active', last: 'incomplete' },
        { title: 'SKRmaxi.com', desc: 'Landing page + Telegram alerts', status: 'active', last: 'SSL fixed' },
        { title: 'Meme Coin Group Chat', desc: 'Multi-agent analysis', status: 'pending', last: 'concept' },
        { title: 'Mission Control Dashboard', desc: 'This dashboard!', status: 'active', last: 'now' }
    );
    
    // Add blocked items
    data.blocked.push(
        { title: 'Grok Provider', desc: 'XAI_API_KEY needed from x.ai/api', workaround: 'Use Kimi/OpenRouter for now' },
        { title: 'Python FAISS deps', desc: 'Apt install taking long / stuck', workaround: 'Use SQLite + simple search as MVP' },
        { title: 'Crypto Memo Birdeye', desc: 'Need API key for on-chain data', workaround: 'Use free DEX APIs temporarily' }
    );
    
    // Read SKRmaxi monitor data
    try {
        const skrmaxiLog = fs.readFileSync('/root/clawd/mission-control/skrmaxi_monitor.jsonl', 'utf8');
        const lines = skrmaxiLog.trim().split('\n').filter(Boolean);
        if (lines.length > 0) {
            data.skrmaxi = JSON.parse(lines[lines.length - 1]);
        }
    } catch (e) {
        data.skrmaxi = null;
    }
    
    return data;
}

const server = http.createServer((req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Content-Type', 'application/json');
    
    if (req.url === '/api/data') {
        res.end(JSON.stringify(getDashboardData(), null, 2));
    } else if (req.url === '/') {
        fs.readFile('/root/clawd/mission-control/dashboard.html', 'utf8', (err, html) => {
            if (err) {
                res.writeHead(500);
                res.end('Error loading dashboard');
            } else {
                res.setHeader('Content-Type', 'text/html');
                res.end(html);
            }
        });
    } else {
        res.writeHead(404);
        res.end('Not found');
    }
});

server.listen(PORT, () => {
    console.log(`🪙 Mission Control running at http://localhost:${PORT}`);
    console.log('Press Ctrl+C to stop');
});
