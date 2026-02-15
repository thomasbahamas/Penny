#!/usr/bin/env python3
"""Penny Alpha Research - Overnight crypto analysis for Thomas"""
import json
import requests
from datetime import datetime, timedelta
import os

class AlphaResearcher:
    def __init__(self):
        self.reports_dir = "/root/clawd/projects/crypto-research/reports"
        os.makedirs(self.reports_dir, exist_ok=True)
        
    def scan_onchain(self):
        """Scan for on-chain signals"""
        signals = []
        
        try:
            # Solana price via CoinGecko
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": "solana,bitcoin,bonk,jupiter,marinade-staked-sol",
                "vs_currencies": "usd",
                "include_24hr_change": "true",
                "include_24hr_vol": "true",
                "include_market_cap": "true"
            }
            resp = requests.get(url, params=params, timeout=10)
            data = resp.json()
            
            for token_id, info in data.items():
                change = info.get("usd_24h_change", 0)
                vol = info.get("usd_24h_vol", 0)
                
                if abs(change) > 5:  # Significant mover
                    signals.append({
                        "type": "mover",
                        "token": token_id,
                        "change_24h": change,
                        "volume_24h": vol,
                        "signal": "up" if change > 0 else "down"
                    })
                    
        except Exception as e:
            signals.append({"type": "error", "message": str(e)})
            
        return signals
    
    def check_whale_movements(self):
        """Check for large wallet movements"""
        # Placeholder - would need dedicated whale tracking
        return {
            "status": "placeholder",
            "note": "Helius/Flipside integration needed for real whale tracking"
        }
    
    def analyze_bonk_position(self, wallet="goatd.sol"):
        """Track BONK position metrics"""
        try:
            # Get BONK data
            url = "https://api.coingecko.com/api/v3/coins/bonk"
            resp = requests.get(url, timeout=10)
            data = resp.json()
            
            price = data["market_data"]["current_price"]["usd"]
            change_24h = data["market_data"]["price_change_percentage_24h"]
            change_7d = data["market_data"]["price_change_percentage_7d"]
            change_30d = data["market_data"]["price_change_percentage_30d"]
            
            # RSI approximation from price action
            ath = data["market_data"]["ath"]["usd"]
            atl = data["market_data"]["atl"]["usd"]
            
            from_ath = ((price - ath) / ath) * 100
            
            return {
                "token": "BONK",
                "price": price,
                "change_24h": change_24h,
                "change_7d": change_7d,
                "change_30d": change_30d,
                "from_ath": from_ath,
                "risk_level": "high" if from_ath < -50 else "medium" if from_ath < -25 else "low"
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def find_rwa_opportunities(self):
        """Track RWA yield opportunities"""
        opportunities = [
            {
                "name": "Ondo OUSG",
                "type": "Treasury",
                "apy": "~4.2%",
                "risk": "Low",
                "min": "Varies",
                "chain": "Solana",
                "notes": "Institutional grade, BlackRock backed"
            },
            {
                "name": "Maple Finance",
                "type": "Private Credit",
                "apy": "4-8%",
                "risk": "Medium",
                "min": "Varies",
                "chain": "Multi-chain",
                "notes": "May require KYC"
            },
            {
                "name": "Credix",
                "type": "Invoice Financing",
                "apy": "10-14%",
                "risk": "Higher",
                "min": "Varies",
                "chain": "Solana",
                "notes": "Emerging markets, higher default risk"
            }
        ]
        return opportunities
    
    def build_thesis(self, opportunity):
        """Build structured thesis for an opportunity"""
        template = f"""
## THESIS: {opportunity.get('name', 'Unknown')}

### Overview
- **Type:** {opportunity.get('type', 'Crypto')}
- **Timeframe:** {opportunity.get('timeframe', 'Medium-term')}
- **Confidence:** {opportunity.get('confidence', 'Medium')}/10

### Catalyst
{opportunity.get('catalyst', 'On-chain metrics suggest accumulation')}

### Risk Factors
{opportunity.get('risks', '- Volatility\n- Market correlation')}

### Position Sizing
- **Max allocation:** {opportunity.get('max_position', '5%')} of portfolio
- **Stop loss:** {opportunity.get('stop_loss', '20%')}
- **Take profit:** {opportunity.get('take_profit', '50%')}

### Execution
{opportunity.get('execution', 'Enter via Jupiter, DCA over 3 days')}

### Exit Plan
{opportunity.get('exit', 'Take profits at targets or on thesis breakdown')}

---
Generated: {datetime.now().isoformat()}
"""
        return template
    
    def generate_daily_brief(self):
        """Generate complete daily research brief"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        brief = []
        brief.append(f"# Alpha Research Brief | {date_str}")
        brief.append("=" * 60)
        brief.append("")
        
        # Market snapshot
        brief.append("## 📊 Market Snapshot")
        onchain = self.scan_onchain()
        for signal in onchain[:3]:  # Top 3 movers
            if signal.get("type") == "mover":
                emoji = "🟢" if signal["signal"] == "up" else "🔴"
                brief.append(f"{emoji} {signal['token'].upper()}: {signal['change_24h']:+.2f}% | Vol: ${signal['volume_24h']:,.0f}")
        brief.append("")
        
        # BONK position
        bonk = self.analyze_bonk_position()
        if "error" not in bonk:
            brief.append("## 🪙 BONK Position Update")
            brief.append(f"- Price: ${bonk['price']:.9f}")
            brief.append(f"- 24h: {bonk['change_24h']:+.2f}%")
            brief.append(f"- From ATH: {bonk['from_ath']:.1f}%")
            brief.append(f"- Risk Level: {bonk['risk_level'].upper()}")
            if bonk['from_ath'] < -50:
                brief.append("⚠️ Deep drawdown - consider DCA if conviction holds")
            brief.append("")
        
        # RWA opportunities
        brief.append("## 🏛️ RWA Yield Opportunities")
        for opp in self.find_rwa_opportunities():
            brief.append(f"- **{opp['name']}**: {opp['apy']} APY ({opp['risk']} risk)")
        brief.append("")
        
        # Today's opportunity thesis
        brief.append("## 🎯 Today's Recommendation")
        brief.append("""
**NO SPECIFIC TRADE RECOMMENDATION**

Research priorities for today:
1. Review BONK position size vs. portfolio concentration
2. Research 1 RWA protocol in depth (suggest starting with Ondo)
3. Check any positions for rebalancing needs

**Risk Rule**: No position should exceed 10% of portfolio
**Action Rule**: DCA entries, never all-in
""")
        
        # Write to file
        filename = f"{self.reports_dir}/brief-{date_str}.md"
        with open(filename, 'w') as f:
            f.write("\n".join(brief))
        
        return filename

    def store_in_memory(self, brief_text: str, date_str: str):
        """Store the brief in Qdrant memory"""
        try:
            sys.path.insert(0, '/root/clawd/projects/memory')
            from penny_memory import PennyMemory
            memory = PennyMemory()
            
            if memory.client:
                memory.remember(
                    f"Alpha Research Brief {date_str}: {brief_text[:500]}",
                    {
                        "type": "alpha_research",
                        "date": date_str,
                        "full_path": f"{self.reports_dir}/brief-{date_str}.md"
                    }
                )
                print(f"✅ Stored in memory")
        except Exception as e:
            print(f"⚠️ Memory storage failed: {e}")
    
    def recall_relevant_research(self, query: str) -> list:
        """Recall past research relevant to query"""
        try:
            sys.path.insert(0, '/root/clawd/projects/memory')
            from penny_memory import PennyMemory
            memory = PennyMemory()
            
            if memory.client:
                results = memory.recall(query, limit=3)
                return [r['text'] for r in results if r.get('metadata', {}).get('type') == 'alpha_research']
            return []
        except:
            return []

if __name__ == "__main__":
    researcher = AlphaResearcher()
    report_path = researcher.generate_daily_brief()
    print(f"✅ Research brief generated: {report_path}")
    print(f"\nRun: cat {report_path}")
    
    # Store in memory
    with open(report_path) as f:
        brief_content = f.read()
    researcher.store_in_memory(brief_content, datetime.now().strftime("%Y-%m-%d"))
