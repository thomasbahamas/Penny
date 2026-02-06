#!/usr/bin/env python3
"""Global search - search through all OpenClaw data"""
import os
import json
import re
from pathlib import Path

WORKSPACE = "/root/clawd"

def search_files(query, max_results=20):
    """Search through all workspace files"""
    results = []
    query_lower = query.lower()
    
    for root, dirs, files in os.walk(WORKSPACE):
        # Skip node_modules, .git, etc
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
        
        for file in files:
            if file.endswith(('.md', '.txt', '.json', '.jsonl', '.py', '.js')):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if query_lower in content.lower():
                            # Find context around match
                            lines = content.split('\n')
                            for i, line in enumerate(lines):
                                if query_lower in line.lower():
                                    context = '\n'.join(lines[max(0,i-2):i+3])
                                    results.append({
                                        "file": filepath.replace(WORKSPACE, ""),
                                        "line": i+1,
                                        "context": context[:200]
                                    })
                                    if len(results) >= max_results:
                                        return results
                                    break
                except:
                    continue
    
    return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        query = sys.argv[1]
        results = search_files(query)
        print(f"🔍 Search: '{query}'")
        print(f"Found {len(results)} matches\n")
        for r in results[:10]:
            print(f"📄 {r['file']}:{r['line']}")
            print(f"   {r['context'][:150]}...")
            print()
    else:
        print("Usage: python global_search.py <query>")
