# Content Production Pipeline

Multi-agent content creation system for SolanaFloor

## Agents

- **NOVA** 🎬 - Video production, scripts, thumbnails
- **PIXEL** 🎨 - UI/UX, design, visual assets  
- **SCRIBE** ✍️ - Copywriting, Twitter threads, newsletters
- **ATLAS** 📊 - Data analysis, insights, visualizations

## How It Works

1. **Add Input** → Put JSON in `content-pipeline/inputs/`
2. **Activate Agents** → Say "Scribe, write a thread" or "Nova, create video script"
3. **Get Content** → Full package: script, video, post, title, chapters

## Usage

### Activate an Agent

```
Scribe, write a Twitter thread about BTC signal
Nova, create video script from latest alpha
Pixel, design thumbnail for SOL analysis
Atlas, analyze trading signal accuracy
```

### Content Pipeline (Batch)

```bash
cd /root/clawd/content-pipeline
python3 pipeline.py
```

## Input Format

```json
{
  "title": "Your Content Title",
  "content": "Main content/data...",
  "data": {...},
  "priority": 1-10,
  "content_type": "trading_signal|alpha|market_event|analysis"
}
```

## Output Structure

Each content package includes:
- 🐦 Twitter/X threads
- 📧 Newsletter copy
- 🎬 Video scripts
- 🎨 Thumbnail designs
- 📊 Data visualizations
- 📱 Social media cards

## Automation

Link to your existing tools:
- Trading signals → Auto-generate content
- Alpha hunter → Auto-drafts for review
- Morning briefing → Repurpose into threads

## Next Steps

1. Test each agent with "use [AGENT]"
2. Add your first content input
3. Build automation from existing pipelines
