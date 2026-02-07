#!/usr/bin/env python3
"""Opus Orchestrator - smart routing + memory optimization"""
import json
import hashlib
from datetime import datetime, timedelta

MEMORY_LOG = "/root/clawd/mission-control/orchestrator_memory.jsonl"

class OpusOrchestrator:
    """Meta-agent that routes and optimizes"""
    
    def __init__(self):
        self.models = {
            "kimi": {
                "id": "openrouter/moonshotai/kimi-k2.5",
                "cost": 1.0,
                "for": ["simple_qa", "chitchat", "routine", "status", "quick_task"]
            },
            "codex": {
                "id": "openai/gpt-5.3-codex", 
                "cost": 3.0,
                "for": ["coding", "building", "implementation", "scripting", "debugging"]
            },
            "opus": {
                "id": "anthropic/claude-opus-4-5",
                "cost": 15.0,
                "for": ["legal", "complex_analysis", "reasoning", "strategy", "architecture"]
            },
            "opus_46": {
                "id": "anthropic/claude-opus-4-6",
                "cost": 18.0,
                "for": ["emergency", "stuck", "novel_problem", "optimization"]
            }
        }
    
    def analyze_complexity(self, query, context_size=0):
        """Analyze query complexity (0-100)"""
        score = 0
        query_lower = query.lower()
        
        # Simple indicators (low complexity)
        simple_words = ["hi", "hello", "status", "help", "what", "how", "when"]
        if any(w in query_lower for w in simple_words):
            score -= 20
        
        # Complex indicators (high complexity)
        complex_markers = [
            "architecture", "design", "strategy", "optimize", "analyze deeply",
            "legal", "contract", "compliance", "jurisdiction", "reasoning",
            "compare multiple", "trade-off", "implications", "consequences"
        ]
        if any(m in query_lower for m in complex_markers):
            score += 30
        
        # Coding/building indicators
        code_markers = [
            "build", "code", "script", "implement", "function", "api",
            "integrate", "deploy", "debug", "fix", "create", "develop"
        ]
        if any(m in query_lower for m in code_markers):
            score += 10
        
        # Context size factor
        if context_size > 100000:  # Large context
            score += 20
        
        # Emergency/stuck indicators
        stuck_markers = ["stuck", "not working", "broken", "error", "failed", "emergency"]
        if any(m in query_lower for m in stuck_markers):
            score += 50
        
        return max(0, min(100, 40 + score))  # Base 40 + adjustments
    
    def route(self, query, context_size=0, cost_budget=50):
        """Route to best model"""
        complexity = self.analyze_complexity(query, context_size)
        
        # Routing logic
        if complexity > 80:
            model = "opus_46"
            reason = "Emergency/complex novel problem"
        elif complexity > 60:
            model = "opus"
            reason = "Deep analysis, legal, or architecture"
        elif complexity > 30:
            model = "codex"
            reason = "Building/coding task"
        else:
            model = "kimi"
            reason = "Quick task, simple query"
        
        return {
            "model": self.models[model]["id"],
            "alias": model,
            "cost_tier": self.models[model]["cost"],
            "complexity_score": complexity,
            "reason": reason
        }
    
    def optimize_memory(self, current_context, max_tokens=150000):
        """Optimize memory to avoid repetition"""
        
        # Parse context into messages
        lines = current_context.split('\n')
        
        # Identify repetitive patterns
        patterns = self._find_patterns(lines)
        
        # Build optimized context
        optimized = []
        summaries = {}
        
        for i, line in enumerate(lines):
            # Skip tool call noise
            if any(x in line for x in ["exec: command", "toolu_", "Writing"]):
                continue
            
            # Summarize repetitive content
            if self._is_repetitive(line, patterns):
                key = self._summarize_key(line)
                if key not in summaries:
                    summaries[key] = line[:100]
                    optimized.append(f"[Earlier: {summaries[key]}...]")
            else:
                optimized.append(line)
        
        result = '\n'.join(optimized)
        
        # If still too long, keep only last N tokens worth
        if len(result) > max_tokens * 4:  # Rough char estimate
            result = self._compress_history(result, max_tokens)
        
        return result
    
    def _find_patterns(self, lines):
        """Find repetitive patterns"""
        patterns = {}
        for line in lines:
            key = hashlib.md5(line[:50].encode()).hexdigest()[:8]
            patterns[key] = patterns.get(key, 0) + 1
        return {k: v for k, v in patterns.items() if v > 2}
    
    def _is_repetitive(self, line, patterns):
        """Check if line is repetitive"""
        key = hashlib.md5(line[:50].encode()).hexdigest()[:8]
        return key in patterns
    
    def _summarize_key(self, line):
        """Create summary key"""
        return hashlib.md5(line.encode()).hexdigest()[:16]
    
    def _compress_history(self, text, max_tokens):
        """Keep only recent relevant history"""
        lines = text.split('\n')
        
        # Keep header + last 80% (most recent)
        header = lines[:10] if len(lines) > 10 else []
        recent = lines[-int(len(lines) * 0.8):]
        
        # Add compression notice
        compressed = header + ["\n[... earlier context compressed ...]\n"] + recent
        
        return '\n'.join(compressed)
    
    def log_decision(self, query, routing, actual_cost=0):
        """Log routing decisions"""
        import os
        os.makedirs(os.path.dirname(MEMORY_LOG), exist_ok=True)
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "query_preview": query[:100],
            "routed_to": routing["alias"],
            "complexity": routing["complexity_score"],
            "estimated_cost_tier": routing["cost_tier"],
            "actual_cost": actual_cost
        }
        
        with open(MEMORY_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")

# Example usage
if __name__ == "__main__":
    orch = OpusOrchestrator()
    
    test_queries = [
        "What's the status?",
        "Build me a trading bot",
        "Analyze this contract for legal risks",
        "We're stuck - the server keeps crashing",
        "Optimize the memory system"
    ]
    
    print("=" * 60)
    print("OPUS ORCHESTRATOR - Routing Tests")
    print("=" * 60)
    
    for q in test_queries:
        route = orch.route(q)
        print(f"\nQuery: {q}")
        print(f"  → {route['alias'].upper()} (complexity: {route['complexity_score']})")
        print(f"  Reason: {route['reason']}")
        print(f"  Cost tier: ${route['cost_tier']}/M tokens")
