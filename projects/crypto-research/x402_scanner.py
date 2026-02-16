#!/usr/bin/env python3
"""x402 Protocol Scanner - Weekly discovery for SKRmaxing v2"""
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict

class X402Scanner:
    def __init__(self):
        self.sources = {
            "github": "https://api.github.com/search/repositories",
            "twitter": None,  # Would need API keys
            "solana_forums": [
                "https://forum.solana.com",
                "https://solana.stackexchange.com"
            ]
        }
        self.report_file = "/root/clawd/projects/crypto-research/x402_weekly_report.md"
    
    def scan_github(self) -> List[Dict]:
        """Scan GitHub for new x402 projects"""
        projects = []
        
        search_terms = [
            "x402",
            "micropayment",
            "solana agent payment",
            "pay-per-request"
        ]
        
        for term in search_terms:
            try:
                # Search without strict date filter (broader results)
                resp = requests.get(
                    self.sources["github"],
                    params={
                        "q": f"{term} language:typescript OR language:rust OR language:python",
                        "sort": "updated",
                        "order": "desc"
                    },
                    headers={"Accept": "application/vnd.github.v3+json"},
                    timeout=15
                )
                
                if resp.status_code == 200:
                    data = resp.json()
                    for item in data.get("items", [])[:3]:  # Top 3 per term
                        # Check if recently updated (within 14 days)
                        updated = datetime.fromisoformat(item["updated_at"].replace('Z', '+00:00'))
                        if datetime.now(updated.tzinfo) - updated < timedelta(days=14):
                            projects.append({
                                "name": item["name"],
                                "description": item["description"],
                                "url": item["html_url"],
                                "stars": item["stargazers_count"],
                                "created": item["created_at"],
                                "updated": item["updated_at"],
                                "language": item["language"],
                                "source": f"GitHub: {term}"
                            })
                        
            except Exception as e:
                print(f"GitHub scan error for '{term}': {e}")
        
        # Remove duplicates by URL
        seen = set()
        unique = []
        for p in projects:
            if p["url"] not in seen:
                seen.add(p["url"])
                unique.append(p)
        
        return sorted(unique, key=lambda x: x["stars"], reverse=True)
    
    def get_tracked_protocols(self) -> List[Dict]:
        """Return manually tracked x402 protocols"""
        # These are known x402/Solana payment protocols to monitor
        return [
            {
                "name": "AgentWallet",
                "description": "PDA-based agent payment vaults on Solana",
                "url": "https://agentwallet.fun",
                "category": "infrastructure",
                "skrmxing_relevance": "HIGH - Core payment rails"
            },
            {
                "name": "x402 Protocol (Original)",
                "description": "HTTP 402 micropayments for AI agents",
                "url": "https://x402.org",
                "category": "standard",
                "skrmxing_relevance": "HIGH - Spec compliance"
            },
            {
                "name": "Payman",
                "description": "Agent payment infrastructure",
                "url": "https://payman.ai",
                "category": "infrastructure",
                "skrmxing_relevance": "MEDIUM - Alternative rails"
            }
        ]
    
    def scan_dune_analytics(self) -> List[Dict]:
        """Track x402 adoption metrics (manual for now)"""
        # Note: Would need Dune API key for real queries
        return {
            "note": "Dune Analytics integration available with API key",
            "metrics_to_track": [
                "Total x402 transactions",
                "Active x402 receivers",
                "Volume by protocol"
            ],
            "dashboard_url": "https://dune.com"  # Placeholder
        }
    
    def research_protocol(self, project: Dict) -> Dict:
        """Deep research on a promising protocol"""
        research = {
            **project,
            "integration_potential": None,
            "risk_level": None,
            "traction_signals": [],
            "why_skrmxing_cares": None
        }
        
        # Heuristic scoring for SKRmaxing v2 fit
        score = 0
        reasons = []
        
        if project.get("stars", 0) > 50:
            score += 20
            reasons.append("Strong community interest")
        
        desc = (project.get("description") or "").lower()
        if any(word in desc for word in ["agent", "ai", "autonomous"]):
            score += 30
            reasons.append("AI/Agent focused (perfect for SKRmaxing)")
        
        if any(word in desc for word in ["payment", "micropayment", "usdc", "sol"]):
            score += 25
            reasons.append("Payment infrastructure")
        
        research["skrmxing_score"] = score
        research["integration_reasons"] = reasons
        
        if score >= 50:
            research["priority"] = "HIGH - Evaluate for integration"
        elif score >= 30:
            research["priority"] = "MEDIUM - Monitor development"
        else:
            research["priority"] = "LOW - Track passively"
        
        return research
    
    def generate_report(self, projects: List[Dict]) -> str:
        """Generate weekly report"""
        lines = []
        lines.append(f"# 🔍 x402 Protocol Weekly Scan")
        lines.append(f"**Week of:** {datetime.now().strftime('%Y-%m-%d')}")
        lines.append(f"**For:** SKRmaxing v2 Integration Pipeline")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # High priority protocols
        high_priority = [p for p in projects if p.get("skrmxing_score", 0) >= 50]
        
        if high_priority:
            lines.append("## 🎯 HIGH PRIORITY: Evaluate for Integration")
            lines.append("")
            for p in high_priority[:5]:
                lines.append(f"### [{p['name']}]({p['url']})")
                lines.append(f"- **Description:** {p.get('description', 'No description')}")
                lines.append(f"- **Stars:** {p.get('stars', 0)} ⭐")
                lines.append(f"- **SKRmaxing Score:** {p.get('skrmxing_score', 0)}/100")
                lines.append(f"- **Why integrate:** {', '.join(p.get('integration_reasons', []))}")
                lines.append("")
        
        # All discoveries
        lines.append("## 📊 All New Discoveries")
        lines.append("")
        lines.append(f"*Found {len(projects)} new x402-related projects this week*")
        lines.append("")
        
        for p in projects[:10]:
            lines.append(f"- **{p['name']}** ({p.get('stars', 0)}⭐) - {p.get('description', 'N/A')[:80]}...")
            lines.append(f"  - [{p['url']}]({p['url']})")
            lines.append(f"  - Priority: {p.get('priority', 'Unknown')}")
            lines.append("")
        
        # Recommendations
        lines.append("## 🚀 Integration Recommendations")
        lines.append("")
        lines.append("### Next Steps for SKRmaxing v2:")
        lines.append("1. **Review top 3 HIGH priority protocols above**")
        lines.append("2. **Test integration complexity** - Check README/docs for API")
        lines.append("3. **Community validation** - Check Discord/Twitter for usage")
        lines.append("4. **Build prototype** - Test payment flow in staging")
        lines.append("")
        lines.append("### Key Metrics to Monitor:")
        lines.append("- Daily active wallets using protocol")
        lines.append("- Transaction volume growth")
        lines.append("- Developer activity (GitHub commits)")
        lines.append("- Community sentiment")
        lines.append("")
        lines.append("---")
        lines.append(f"*Report generated: {datetime.now().isoformat()}*")
        lines.append("*Next scan: 7 days*")
        
        return "\n".join(lines)
    
    def run_weekly_scan(self) -> str:
        """Execute full weekly scan"""
        print("🔍 Starting x402 weekly scan...")
        
        # Phase 1: Discovery
        print("Phase 1: Scanning GitHub...")
        projects = self.scan_github()
        print(f"  Found {len(projects)} projects")
        
        # Phase 2: Research
        print("Phase 2: Researching top candidates...")
        researched = [self.research_protocol(p) for p in projects[:20]]
        
        # Phase 3: Report
        print("Phase 3: Generating report...")
        report = self.generate_report(researched)
        
        # Save
        with open(self.report_file, 'w') as f:
            f.write(report)
        
        return report

if __name__ == "__main__":
    scanner = X402Scanner()
    report = scanner.run_weekly_scan()
    print(f"\n✅ Report saved to: {scanner.report_file}")
    print("\n" + "="*60)
    print(report[:1000] + "...")
