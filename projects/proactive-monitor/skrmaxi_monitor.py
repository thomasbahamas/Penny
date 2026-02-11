#!/usr/bin/env python3
"""SKRmaxi site monitor - tracks user activity and sends alerts"""
import json
import requests
from datetime import datetime
import os

# SKRmaxi endpoints to monitor
ENDPOINTS = {
    'health': 'https://skrmaxin.com/api/health',
    'stats': 'https://skrmaxin.com/api/stats',
    'recent_users': 'https://skrmaxin.com/api/users/recent',
}

ALERT_THRESHOLD = {
    'error_rate': 0.05,  # 5% error rate triggers alert
    'response_time': 5000,  # 5 seconds
}

def check_endpoint(name, url):
    """Check endpoint health"""
    try:
        start = datetime.now()
        resp = requests.get(url, timeout=10)
        latency = (datetime.now() - start).total_seconds() * 1000
        
        return {
            'name': name,
            'status': 'up' if resp.status_code == 200 else 'down',
            'status_code': resp.status_code,
            'latency_ms': round(latency, 2),
            'timestamp': datetime.now().isoformat(),
            'data': resp.json() if resp.status_code == 200 else None
        }
    except Exception as e:
        return {
            'name': name,
            'status': 'error',
            'error': str(e)[:100],
            'timestamp': datetime.now().isoformat()
        }

def format_alert(results):
    """Format results for dashboard/briefing"""
    output = "📊 SKRmaxi Status:\n\n"
    
    for r in results:
        emoji = "🟢" if r['status'] == 'up' else "🔴"
        output += f"{emoji} {r['name'].upper()}: {r['status']}"
        if r.get('latency_ms'):
            output += f" ({r['latency_ms']}ms)"
        if r.get('data'):
            # Extract key metrics
            data = r['data']
            if 'active_users' in data:
                output += f" | Users: {data['active_users']}"
            if 'total_wallets' in data:
                output += f" | Wallets: {data['total_wallets']}"
        output += "\n"
    
    return output

def save_to_log(results):
    """Save results for dashboard"""
    log_file = '/root/clawd/mission-control/skrmaxi_monitor.jsonl'
    entry = {
        'timestamp': datetime.now().isoformat(),
        'results': results
    }
    with open(log_file, 'a') as f:
        f.write(json.dumps(entry) + '\n')

def send_alert_if_needed(results):
    """Send Telegram alert if issues detected"""
    issues = [r for r in results if r['status'] != 'up']
    
    if issues:
        token = os.environ.get('TELEGRAM_BOT_TOKEN', '')
        chat_id = os.environ.get('TELEGRAM_CHAT_ID', '1123064049')
        
        if not token:
            return
        
        message = "🚨 SKRmaxi Alert!\n\n"
        for issue in issues:
            message += f"❌ {issue['name']}: {issue.get('error', issue['status'])}\n"
        
        try:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            requests.post(url, json={'chat_id': chat_id, 'text': message}, timeout=10)
        except:
            pass

if __name__ == "__main__":
    results = []
    for name, url in ENDPOINTS.items():
        results.append(check_endpoint(name, url))
    
    save_to_log(results)
    
    output = format_alert(results)
    print(output)
    
    send_alert_if_needed(results)
