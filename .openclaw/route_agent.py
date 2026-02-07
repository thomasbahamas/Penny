#!/usr/bin/env python3
"""
Agent Request Router - Integrates Opus Orchestrator with OpenClaw
Analyzes each query and routes to optimal model
"""
import json
import sys
import os

# Load config
CONFIG_FILE = "/root/clawd/.openclaw/orchestrator_config.json"

def load_config():
    """Load orchestrator config"""
    try:
        with open(CONFIG_FILE) as f:
            return json.load(f)
    except:
        return {
            "model_routing": {
                "enabled": True,
                "routes": {
                    "simple": {"model": "openrouter/moonshotai/kimi-k2.5", "max_complexity": 30},
                    "coding": {"model": "openai/gpt-5.3-codex", "complexity_range": [30, 60]},
                    "complex": {"model": "anthropic/claude-opus-4-5", "complexity_range": [60, 80]},
                    "emergency": {"model": "anthropic/claude-opus-4-6", "min_complexity": 80}
                }
            }
        }

def analyze_query(query):
    """Analyze query complexity"""
    score = 40  # Base
    query_lower = query.lower()
    
    # Simple patterns
    simple = ["status", "hello", "help", "what is", "what's", "when", "where", "how"]
    if any(s in query_lower for s in simple):
        score -= 20
    
    # Code patterns  
    code = ["build", "code", "script", "implement", "deploy", "function", "api"]
    if any(c in query_lower for c in code):
        score += 10
    
    # Complex patterns
    complex_p = ["analyze", "legal", "contract", "strategy", "architecture", "optimize"]
    if any(c in query_lower for c in complex_p):
        score += 30
    
    # Emergency
    emergency = ["stuck", "broken", "error", "failed", "emergency", "urgent"]
    if any(e in query_lower for e in emergency):
        score += 50
    
    return max(0, min(100, score))

def route_query(query):
    """Route query to best model"""
    config = load_config()
    
    if not config.get("model_routing", {}).get("enabled"):
        return None
    
    complexity = analyze_query(query)
    routes = config["model_routing"]["routes"]
    
    if complexity >= 80:
        return routes["emergency"]["model"], "emergency", complexity
    elif complexity >= 60:
        return routes["complex"]["model"], "complex", complexity
    elif complexity >= 30:
        return routes["coding"]["model"], "coding", complexity
    else:
        return routes["simple"]["model"], "simple", complexity

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        model, route_type, complexity = route_query(query)
        
        print(f"Query: {query}")
        print(f"Complexity: {complexity}/100")
        print(f"Routed to: {model}")
        print(f"Type: {route_type}")
        
        # Save to temp for OpenClaw to read
        with open("/tmp/orchestrator_route.json", "w") as f:
            json.dump({
                "model": model,
                "type": route_type,
                "complexity": complexity,
                "original_query": query
            }, f)
    else:
        print("Usage: python3 route_agent.py 'your query here'")
        print("\nTest queries:")
        print("  'What is the status?' → Simple (Kimi)")
        print("  'Build me a bot' → Coding (GPT-Codex)")
        print("  'Analyze contract' → Complex (Opus 4.5)")
        print("  'Server stuck!' → Emergency (Opus 4.6)")
