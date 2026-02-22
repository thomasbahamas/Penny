#!/bin/bash
# THOMAS OPTIMISM PROTOCOL CRON JOBS
# Add these to crontab with: crontab -e

# Morning Optimism Priming — 5:10am PST daily
10 5 * * * cd /root/clawd/projects/morning-brief && python3 alpha_brief_generator_v2.py 2>&1 | tee /tmp/optimism_priming.log

# Evening Win Log — 6:00pm PST daily  
0 18 * * * cd /root/clawd/templates && python3 evening_win_log.py 2>&1 | tee /tmp/evening_win.log

# Alpha Brief with Optimism — 5:30am PST daily
30 5 * * * cd /root/clawd/projects/morning-brief && python3 alpha_brief_generator_v2.py 2>&1 | tee /tmp/alpha_brief_v2.log

# Existing jobs (keep these):
# 5:55am warning, 7:00am X time, 7:30am work mode
# 9:30am, 12pm, 3pm, 6pm agency checks
# Sunday 8pm wealth ritual
