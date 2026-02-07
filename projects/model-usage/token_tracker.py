#!/usr/bin/env python3
"""Token usage tracker - logs and reports costs"""
import json
import os
from datetime import datetime, timedelta

LOG_FILE = "/root/clawd/mission-control/token_usage.jsonl"
SCHEMA_FILE = "/root/clawd/projects/model-usage/model_schema.json"

def log_usage(model, input_tokens, output_tokens, task_type="general"):
    """Log token usage"""
    
    # Load costs
    costs = {
        "openrouter/moonshotai/kimi-k2.5": {"input": 1.00, "output": 3.00},
        "anthropic/claude-opus-4-5": {"input": 15.00, "output": 75.00},
        "anthropic/claude-opus-4-6": {"input": 18.00, "output": 90.00}
    }
    
    cost_per_m = costs.get(model, costs["openrouter/moonshotai/kimi-k2.5"])
    input_cost = (input_tokens / 1_000_000) * cost_per_m["input"]
    output_cost = (output_tokens / 1_000_000) * cost_per_m["output"]
    total_cost = input_cost + output_cost
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "model": model,
        "task_type": task_type,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost_usd": round(total_cost, 6)
    }
    
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
    
    return total_cost

def daily_report():
    """Generate daily cost report"""
    today = datetime.now().date()
    total_cost = 0
    model_usage = {}
    
    try:
        with open(LOG_FILE, "r") as f:
            for line in f:
                if not line.strip():
                    continue
                entry = json.loads(line)
                entry_date = datetime.fromisoformat(entry["timestamp"]).date()
                
                if entry_date == today:
                    total_cost += entry["cost_usd"]
                    model = entry["model"]
                    if model not in model_usage:
                        model_usage[model] = {"cost": 0, "requests": 0}
                    model_usage[model]["cost"] += entry["cost_usd"]
                    model_usage[model]["requests"] += 1
    except FileNotFoundError:
        pass
    
    print("=" * 60)
    print(f"📊 TOKEN USAGE REPORT - {today}")
    print("=" * 60)
    print(f"\n💰 Total Cost: ${total_cost:.4f}")
    
    if model_usage:
        print("\n📈 By Model:")
        for model, data in model_usage.items():
            name = model.split("/")[-1]
            print(f"  {name}: ${data['cost']:.4f} ({data['requests']} reqs)")
    
    # Budget check
    budget = 50.00
    remaining = budget - total_cost
    pct_used = (total_cost / budget) * 100
    
    print(f"\n💵 Budget: ${budget:.2f} | Remaining: ${remaining:.2f} | Used: {pct_used:.1f}%")
    
    if pct_used > 80:
        print("⚠️  WARNING: Approaching daily budget limit!")
    
    print("=" * 60)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "report":
        daily_report()
    else:
        # Test logging
        cost = log_usage("openrouter/moonshotai/kimi-k2.5", 1000, 500, "test")
        print(f"Logged test entry: ${cost:.6f}")
        print("Usage: python token_tracker.py report")
