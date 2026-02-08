# Security Incident Report

**Date:** February 7, 2025
**Severity:** High
**Status:** Resolved (Token Rotated)

## Incident Summary

Telegram bot token was inadvertently committed to the GitHub repository `thomasbahamas/Penny` and was detected by GitGuardian.

## Timeline

- **08:52 AM PST** - GitGuardian alert sent to penny.assistants@gmail.com (immediately rotated)
- **14:23 UTC** - Token confirmed exposed in repository
- **Resolved** - Token rotated, new token configured

## How It Happened

The Telegram bot token was stored in the OpenClaw configuration file which was then committed to the GitHub repository. This file was located at:
`/root/.openclaw/openclaw.json`

## Immediate Actions Taken

1. ✓ Old token revoked via @BotFather
2. ✓ New token generated
3. ✓ OpenClaw configuration updated
4. ✓ Gateway restarted with new credentials
5. ✓ Old token no longer functional

## Prevention Measures

1. **Git Secrets**: Configured `.gitignore` to exclude config files
2. **Environment Variables**: Tokens now loaded from env vars
3. **Pre-commit Hooks**: Added git-secrets scanning
4. **Regular Audits**: Monthly security reviews

## Impact

- **Risk Level**: High (exposed credentials)
- **Actual Abuse**: None detected (token rotated immediately)
- **Data Compromised**: None
- **Service Disruption**: Minimal (brief restart required)

## Lessons Learned

- Never commit secrets to version control
- Use environment variables for sensitive data
- Enable secret scanning on all repositories
- Respond immediately to security alerts

---
**Next Review:** March 7, 2025
