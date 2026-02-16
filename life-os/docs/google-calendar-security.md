# Google Calendar Integration - Security Guide

## Architecture (Secure)

```
LifeOS PWA (Frontend)
    ↓ HTTPS
Backend API (Your VPS)
    ↓ OAuth 2.0
Google Calendar API
```

**Why this matters:**
- OAuth tokens stay server-side
- PWA never sees sensitive credentials
- Can revoke access centrally

## Implementation Steps

### 1. Create Google Cloud Project
- Go to console.cloud.google.com
- Create project "Thomas LifeOS"
- Enable Google Calendar API
- Create OAuth 2.0 credentials
- Add authorized redirect: `https://your-domain.com/auth/callback`

### 2. Backend Auth Handler (Node.js/Python)
```javascript
// /api/auth/google - initiates OAuth
app.get('/auth/google', (req, res) => {
  const authUrl = oauth2Client.generateAuthUrl({
    access_type: 'offline',  // Get refresh token
    scope: ['https://www.googleapis.com/auth/calendar.readonly']
  });
  res.redirect(authUrl);
});

// /api/auth/callback - handles OAuth callback
app.get('/auth/callback', async (req, res) => {
  const { tokens } = await oauth2Client.getToken(req.query.code);
  // Store tokens securely (encrypted DB)
  await saveTokens(req.user.id, tokens);
  res.redirect('/?auth=success');
});

// /api/calendar/events - proxy to Google
app.get('/api/calendar/events', async (req, res) => {
  const tokens = await getTokens(req.user.id);
  oauth2Client.setCredentials(tokens);
  const calendar = google.calendar({ version: 'v3', auth: oauth2Client });
  const events = await calendar.events.list({...});
  res.json(events.data);
});
```

### 3. Token Security
- **Never** store in localStorage (XSS vulnerable)
- Use httpOnly cookies OR
- Encrypt tokens in IndexedDB with user-derived key
- Rotate refresh tokens periodically

### 4. PWA Integration
```javascript
// Frontend only talks to YOUR backend
const events = await fetch('/api/calendar/events').then(r => r.json());
```

## Option 2: Public ICS Feed Import (Read-Only, Simplest)

Google Calendar allows public sharing via ICS:
1. Google Calendar → Settings → Integrate calendar
2. Copy "Public address in iCal format"
3. PWA fetches: `https://calendar.google.com/calendar/ical/.../basic.ics`
4. Parse with ical.js library

**Pros:**
- No OAuth complexity
- No server required
- Read-only (safer)

**Cons:**
- Only works if calendar is public
- No write access
- 12-24 hour sync delay

## Option 3: Service Account (For Workspace/Org Calendars)

If using Google Workspace:
1. Create service account in Google Cloud
2. Share specific calendars with service account email
3. Server authenticates with JSON key file
4. No user OAuth flow needed

**Best for:** Multiple family calendars, workspace integration

## Current Recommendation for LifeOS

**Phase 1 (Now):** Manual ICS import
- Export family calendars to ICS
- PWA imports and caches locally
- Simple, no auth complexity

**Phase 2 (Later):** OAuth with backend
- Set up proper domain (not Cloudflare tunnel)
- Implement backend proxy
- Full two-way sync

## Security Checklist

- [ ] OAuth tokens stored server-side only
- [ ] HTTPS everywhere (no http)
- [ ] Content Security Policy headers
- [ ] Rate limiting on API endpoints
- [ ] Token refresh logic
- [ ] Revoke access capability
- [ ] Audit logging

## Immediate Next Steps

Want me to:
1. **Implement ICS import** (quick win, no auth needed)
2. **Set up OAuth backend** (full integration, more work)
3. **Deploy to custom domain** (needed for OAuth)

Current Cloudflare tunnel URL won't work for OAuth (temporary domains).
