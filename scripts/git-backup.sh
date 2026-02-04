#!/bin/bash
cd /root/clawd
git add -A
git commit -m "Auto-backup $(date '+%Y-%m-%d %H:%M')" 2>/dev/null || true
git push origin main 2>/dev/null || true
