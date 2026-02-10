#!/usr/bin/env python3
"""
Daily Security Scanner
Checks for exposed keys, tokens, and sensitive data
"""
import os
import re
import json
import subprocess
from datetime import datetime
import sys

REPO_PATH = "/root/clawd"
SCAN_LOG = "/root/clawd/mission-control/security_scan.jsonl"
ALERT_THRESHOLD = 1  # Number of findings to trigger alert

# Patterns to detect
PATTERNS = {
    "telegram_token": {
        "pattern": r"\d{9,10}:[A-Za-z0-9_-]{35}",
        "severity": "CRITICAL",
        "description": "Telegram Bot Token"
    },
    "openai_key": {
        "pattern": r"sk-[a-zA-Z0-9]{20,}",
        "severity": "CRITICAL", 
        "description": "OpenAI API Key"
    },
    "anthropic_key": {
        "pattern": r"sk-ant-[a-zA-Z0-9]{20,}",
        "severity": "CRITICAL",
        "description": "Anthropic API Key"
    },
    "private_key": {
        "pattern": r"BEGIN.*PRIVATE.*KEY",
        "severity": "CRITICAL",
        "description": "Private Key"
    },
    "aws_key": {
        "pattern": r"AKIA[0-9A-Z]{16}",
        "severity": "CRITICAL",
        "description": "AWS Access Key"
    },
    "email_address": {
        "pattern": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com|net|org|io|co|ai|app|dev)",
        "severity": "WARNING",
        "description": "Email Address"
    },
    "api_key_generic": {
        "pattern": r"api[_-]?key\s*[:=]\s*[a-zA-Z0-9]{16,}",
        "severity": "HIGH",
        "description": "Generic API Key"
    },
    "password": {
        "pattern": r"password\s*[:=]\s*[^\s]{8,}",
        "severity": "HIGH",
        "description": "Password in code"
    },
    "database_url": {
        "pattern": r"(postgres|mysql|mongodb)://[^:]+:[^@]+@",
        "severity": "HIGH",
        "description": "Database URL with credentials"
    }
}

# Safe files/directories to skip
SKIP_PATHS = [
    ".git",
    "node_modules",
    "__pycache__",
    ".pyc",
    ".sample",
    ".example",
    "README",
    "LICENSE",
    "CHANGELOG",
    "PERSONA.md",  # Agent personas contain emails intentionally
    "USER.md",     # User config
    "memory/",     # Memory files
    "mission-control/security_scan.jsonl"  # Don't scan self
]

def should_skip(path):
    """Check if path should be skipped"""
    for skip in SKIP_PATHS:
        if skip in path:
            return True
    return False

def scan_file(filepath):
    """Scan a single file for secrets"""
    findings = []
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except:
        return findings
    
    for name, config in PATTERNS.items():
        matches = re.finditer(config["pattern"], content, re.IGNORECASE)
        for match in matches:
            # Skip if in comment or example
            line_start = content.rfind('\n', 0, match.start()) + 1
            line = content[line_start:content.find('\n', match.end())]
            
            if any(x in line.lower() for x in ['example', 'sample', 'test', 'demo', 'fake', 'placeholder', '#', '//']):
                continue
            
            # Mask the secret
            secret = match.group(0)
            if len(secret) > 10:
                masked = secret[:4] + "****" + secret[-4:]
            else:
                masked = "****"
            
            findings.append({
                "type": name,
                "severity": config["severity"],
                "description": config["description"],
                "file": filepath,
                "line": line[:80] + "..." if len(line) > 80 else line,
                "masked": masked,
                "position": match.start()
            })
    
    return findings

def scan_repository():
    """Scan entire repository"""
    all_findings = []
    
    for root, dirs, files in os.walk(REPO_PATH):
        # Skip directories
        dirs[:] = [d for d in dirs if not should_skip(os.path.join(root, d))]
        
        for file in files:
            filepath = os.path.join(root, file)
            
            if should_skip(filepath):
                continue
            
            # Only scan text files
            if not any(file.endswith(ext) for ext in ['.py', '.js', '.json', '.md', '.txt', '.sh', '.yaml', '.yml', '.conf', '.cfg']):
                continue
            
            findings = scan_file(filepath)
            all_findings.extend(findings)
    
    return all_findings

def check_git_history():
    """Check recent commits for secrets"""
    try:
        result = subprocess.run(
            ["git", "log", "-p", "--since=yesterday", "--format=fuller"],
            cwd=REPO_PATH,
            capture_output=True,
            text=True
        )
        
        history_findings = []
        
        for name, config in PATTERNS.items():
            matches = re.finditer(config["pattern"], result.stdout, re.IGNORECASE)
            for match in matches:
                secret = match.group(0)
                masked = secret[:4] + "****" + secret[-4:] if len(secret) > 10 else "****"
                history_findings.append({
                    "type": name,
                    "severity": config["severity"],
                    "description": config["description"],
                    "source": "git_history",
                    "masked": masked
                })
        
        return history_findings
    except:
        return []

def send_alert(findings):
    """Send alert if critical findings"""
    critical = [f for f in findings if f["severity"] == "CRITICAL"]
    high = [f for f in findings if f["severity"] == "HIGH"]
    
    if len(critical) > 0 or len(high) > 0:
        print("\n" + "=" * 70)
        print("🚨 SECURITY ALERT")
        print("=" * 70)
        print(f"Critical findings: {len(critical)}")
        print(f"High severity: {len(high)}")
        print("\nIMMEDIATE ACTION REQUIRED")
        print("1. Rotate exposed credentials")
        print("2. Remove from repository")
        print("3. Use environment variables instead")
        print("=" * 70)
        return True
    return False

def main():
    """Run daily security scan"""
    print("=" * 70)
    print("🔒 DAILY SECURITY SCAN")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Scan current files
    print("\n📁 Scanning repository files...")
    findings = scan_repository()
    
    # Scan git history
    print("🔍 Checking recent commits...")
    history_findings = check_git_history()
    findings.extend(history_findings)
    
    # Deduplicate
    seen = set()
    unique_findings = []
    for f in findings:
        key = f"{f['type']}:{f.get('file', f.get('source', 'unknown'))}"
        if key not in seen:
            seen.add(key)
            unique_findings.append(f)
    
    findings = unique_findings
    
    # Report
    print(f"\n{'=' * 70}")
    print(f"📊 SCAN RESULTS: {len(findings)} findings")
    print(f"{'=' * 70}")
    
    by_severity = {"CRITICAL": 0, "HIGH": 0, "WARNING": 0}
    for f in findings:
        by_severity[f["severity"]] = by_severity.get(f["severity"], 0) + 1
    
    print(f"  🔴 Critical: {by_severity.get('CRITICAL', 0)}")
    print(f"  🟠 High: {by_severity.get('HIGH', 0)}")
    print(f"  🟡 Warning: {by_severity.get('WARNING', 0)}")
    
    if findings:
        print(f"\n📋 DETAILS:")
        for f in findings[:10]:  # Show first 10
            print(f"\n  [{f['severity']}] {f['description']}")
            print(f"    File: {f.get('file', f.get('source', 'N/A'))}")
            print(f"    Found: {f['masked']}")
            if 'line' in f:
                print(f"    Context: {f['line']}")
    
    # Log results
    os.makedirs(os.path.dirname(SCAN_LOG), exist_ok=True)
    scan_result = {
        "timestamp": datetime.now().isoformat(),
        "findings_count": len(findings),
        "by_severity": by_severity,
        "findings": findings
    }
    
    with open(SCAN_LOG, "a") as f:
        f.write(json.dumps(scan_result) + "\n")
    
    # Alert if needed
    alerted = send_alert(findings)
    
    print(f"\n{'=' * 70}")
    if len(findings) == 0:
        print("✅ No security issues detected")
    elif not alerted:
        print("⚠️  Warnings found - review recommended")
    else:
        print("🚨 CRITICAL ISSUES - IMMEDIATE ACTION REQUIRED")
    print(f"{'=' * 70}")
    
    # Return exit code
    return 1 if len([f for f in findings if f["severity"] == "CRITICAL"]) > 0 else 0

if __name__ == "__main__":
    sys.exit(main())
