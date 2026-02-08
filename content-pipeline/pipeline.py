#!/usr/bin/env python3
"""
Content Production Pipeline
Takes input (trading signal, alpha finding, market event) 
and produces: script, video, post, title, chapters
"""
import json
import os
from datetime import datetime

INPUT_DIR = "/root/clawd/content-pipeline/inputs"
OUTPUT_DIR = "/root/clawd/content-pipeline/outputs"

def load_persona(agent_name):
    """Load agent persona"""
    persona_file = f"/root/clawd/agents/{agent_name.lower()}/PERSONA.md"
    try:
        with open(persona_file) as f:
            return f.read()
    except:
        return f"{agent_name} persona not found"

def create_content_package(source_data, content_type="trading_signal"):
    """
    Create full content package from source data
    
    source_data: dict with 'title', 'content', 'data'
    content_type: 'trading_signal', 'alpha', 'market_event', 'analysis'
    """
    
    package = {
        "source": source_data,
        "created_at": datetime.now().isoformat(),
        "content_type": content_type,
        "outputs": {}
    }
    
    # Structure for each agent to fill
    package["outputs"] = {
        "scribe": {
            "twitter_thread": "",
            "newsletter_blurb": "",
            "linkedin_post": "",
            "email_subject_lines": []
        },
        "nova": {
            "video_title_options": [],
            "hook_script": "",
            "video_structure": [],
            "thumbnail_concept": "",
            "b_roll_suggestions": [],
            "chapters": []
        },
        "pixel": {
            "thumbnail_design": "",
            "social_cards": [],
            "data_visualization": ""
        },
        "atlas": {
            "data_insights": "",
            "chart_suggestions": [],
            "key_metrics": {}
        }
    }
    
    return package

def save_package(package, filename=None):
    """Save content package"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"content_{timestamp}.json"
    
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    with open(filepath, 'w') as f:
        json.dump(package, f, indent=2)
    
    return filepath

def get_pending_inputs():
    """Get list of content waiting to be processed"""
    os.makedirs(INPUT_DIR, exist_ok=True)
    
    inputs = []
    for f in os.listdir(INPUT_DIR):
        if f.endswith('.json'):
            with open(os.path.join(INPUT_DIR, f)) as file:
                data = json.load(file)
                data['filename'] = f
                inputs.append(data)
    
    return sorted(inputs, key=lambda x: x.get('priority', 0), reverse=True)

def generate_prompt_for_agent(agent_name, source_data):
    """Generate specific prompt for an agent based on source"""
    
    prompts = {
        "scribe": f"""
Source: {source_data.get('title', 'Untitled')}
Content: {source_data.get('content', '')[:500]}...

Create:
1. Twitter/X thread (5-7 tweets)
2. Newsletter paragraph (100 words)
3. LinkedIn post (professional tone)
4. 3 email subject line options

Use your SCRIBE persona principles.
""",
        "nova": f"""
Source: {source_data.get('title', 'Untitled')}
Content: {source_data.get('content', '')[:500]}...

Create:
1. 3 video title options (clickbait, educational, curiosity gap)
2. 30-second hook script
3. Video structure with timestamps
4. Thumbnail concept (text + visual)
5. B-roll suggestions
6. Chapter markers

Use your NOVA persona principles.
""",
        "pixel": f"""
Source: {source_data.get('title', 'Untitled')}
Content: {source_data.get('content', '')[:500]}...

Create:
1. Thumbnail design (colors, layout, text)
2. Social media card designs
3. Data visualization concept (if data present)

Use your PIXEL persona principles.
Dark mode, crypto aesthetic.
""",
        "atlas": f"""
Source: {source_data.get('title', 'Untitled')}
Data: {json.dumps(source_data.get('data', {}))}

Create:
1. Key data insights (2-3 bullets)
2. Chart/visualization suggestions
3. Important metrics to highlight

Use your ATLAS persona principles.
Statistical rigor matters.
"""
    }
    
    return prompts.get(agent_name.lower(), "No specific prompt available")

if __name__ == "__main__":
    print("=" * 60)
    print("CONTENT PRODUCTION PIPELINE")
    print("=" * 60)
    
    # Check for pending inputs
    pending = get_pending_inputs()
    
    if pending:
        print(f"\nFound {len(pending)} items to process:")
        for item in pending:
            print(f"  - {item.get('title', 'Untitled')} (priority: {item.get('priority', 0)})")
    else:
        print("\nNo pending inputs.")
        print(f"\nAdd inputs to: {INPUT_DIR}")
        print("\nFormat:")
        print(json.dumps({
            "title": "Example Trading Signal",
            "content": "BTC showing strong buy signal...",
            "data": {"price": 45000, "rsi": 28},
            "priority": 5,
            "content_type": "trading_signal"
        }, indent=2))
    
    print("\n" + "=" * 60)
    print("Usage:")
    print("1. Add input to content-pipeline/inputs/")
    print("2. Run: python3 content_pipeline.py")
    print("3. I'll generate prompts for each agent")
    print("4. Agents create content")
    print("5. Package saved to outputs/")
    print("=" * 60)
