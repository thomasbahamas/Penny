#!/usr/bin/env python3
"""Legal Analyzer - AI legal team for contracts, compliance, research"""
import os
import sys

def analyze_contract(text):
    """Analyze contract terms and risks"""
    analysis = f"""
LEGAL CONTRACT ANALYSIS
========================

📋 DOCUMENT TYPE: {detect_doc_type(text)}

🔍 KEY CLAUSES IDENTIFIED:
"""
    
    # Check for common clauses
    text_lower = text.lower()
    
    clauses = []
    if "termination" in text_lower:
        clauses.append("✓ Termination clause")
    if "liability" in text_lower:
        clauses.append("✓ Liability limitation")
    if "confidential" in text_lower:
        clauses.append("✓ Confidentiality/NDA")
    if "intellectual property" in text_lower or "ip" in text_lower:
        clauses.append("✓ IP assignment")
    if "indemnif" in text_lower:
        clauses.append("✓ Indemnification")
    if "warranty" in text_lower:
        clauses.append("✓ Warranties")
    if "force majeure" in text_lower:
        clauses.append("✓ Force majeure")
    if "governing law" in text_lower:
        clauses.append("✓ Governing law")
    if "arbitration" in text_lower:
        clauses.append("✓ Arbitration/dispute resolution")
    if "non-compete" in text_lower or "non compete" in text_lower:
        clauses.append("⚠️ Non-compete (check enforceability)")
    if "non-solicit" in text_lower:
        clauses.append("⚠️ Non-solicitation")
    
    if clauses:
        analysis += "\n".join(f"  {c}" for c in clauses)
    else:
        analysis += "  (No standard clauses detected)"
    
    # Risk flags
    analysis += "\n\n⚠️  RISK FLAGS:\n"
    risks = []
    
    if "unlimited liability" in text_lower:
        risks.append("🔴 HIGH: Unlimited liability exposure")
    if "irrevocable" in text_lower and "license" in text_lower:
        risks.append("🟡 MEDIUM: Irrevocable license grant")
    if "perpetual" in text_lower:
        risks.append("🟡 MEDIUM: Perpetual obligations")
    if "sole discretion" in text_lower:
        risks.append("🟡 MEDIUM: Unilateral change rights")
    if "no limitation" in text_lower and "damages" in text_lower:
        risks.append("🔴 HIGH: No limitation of damages")
    if "assign" in text_lower and "without consent" in text_lower:
        risks.append("🟢 LOW: Assignment without consent allowed")
    
    if risks:
        analysis += "\n".join(f"  {r}" for r in risks)
    else:
        analysis += "  No major red flags detected"
    
    # Recommendations
    analysis += """

💡 RECOMMENDATIONS:
  • Have a lawyer review before signing
  • Verify counterparty identity
  • Check governing law jurisdiction
  • Ensure termination rights are balanced
  • Confirm IP ownership is clear

📝 NEXT STEPS:
  1. Save to /legal/contracts/ folder
  2. Add to calendar for renewal date
  3. Share with legal counsel if >$10K value
  4. Document key dates and obligations

⚖️  DISCLAIMER: This is AI analysis, not legal advice.
   Consult a licensed attorney for binding opinions.
"""
    
    return analysis

def detect_doc_type(text):
    """Detect document type"""
    text_lower = text.lower()
    
    if "non-disclosure" in text_lower or "nda" in text_lower:
        return "NDA / Confidentiality Agreement"
    elif "service" in text_lower and "agreement" in text_lower:
        return "Service Agreement"
    elif "employment" in text_lower:
        return "Employment Contract"
    elif "token" in text_lower and "sale" in text_lower:
        return "Token Sale / SAFT"
    elif "partnership" in text_lower:
        return "Partnership Agreement"
    elif "license" in text_lower:
        return "License Agreement"
    else:
        return "General Agreement"

def crypto_compliance_check(project_type):
    """Checklist for crypto project compliance"""
    return f"""
CRYPTO COMPLIANCE CHECKLIST - {project_type.upper()}
=====================================

🇺🇸 UNITED STATES:
☐ SEC registration analysis (Howey test)
☐ CFTC commodity classification
☐ FinCEN MSB registration (if applicable)
☐ State money transmitter licenses
☐ OFAC sanctions screening

🌍 INTERNATIONAL:
☐ EU MiCA compliance (if targeting EU)
☐ UK FCA registration
☐ Singapore MAS licensing
☐ Dubai VARA (if applicable)

📋 OPERATIONAL:
☐ KYC/AML procedures documented
☐ Custody solution audited
☐ Smart contract audits (2+ firms)
☐ Insurance coverage (custody, cyber)
☐ Incident response plan

⚖️  LEGAL STRUCTURE:
☐ Entity formed (Delaware/Cayman/etc)
☐ Cap table documented
☐ Tokenomics legal review
☐ Tax strategy (US + international)
☐ Founders vesting schedules

📢 MARKETING:
☐ No guaranteed returns promised
☐ Risk disclosures included
☐ Not marketed as security
☐ Influencer disclosure compliance

💰 TAX:
☐ Treasury management plan
☐ Token sale proceeds tracking
☐ Employee token compensation structure
☐ 409A valuation (if US employees)

🚨 RED FLAGS TO AVOID:
  • Promising investment returns
  • Unclear token utility
  • Anonymous team
  • No vesting for insiders
  • Unaudited contracts
  • Shell companies

📅 KEY DATES:
  • Token launch: ___________
  • Exchange listings: ___________
  • Lock-up expirations: ___________
  • Tax filing deadlines: ___________

⚖️  DISCLAIMER: Not legal advice. Consult crypto-specialized attorney.
"""

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "contract":
            print("Paste contract text (Ctrl+D when done):")
            text = sys.stdin.read()
            print(analyze_contract(text))
        
        elif command == "compliance":
            project = sys.argv[2] if len(sys.argv) > 2 else "defi"
            print(crypto_compliance_check(project))
        
        else:
            print("Usage:")
            print("  python legal_analyzer.py contract     # Analyze contract")
            print("  python legal_analyzer.py compliance   # Compliance checklist")
    else:
        print("Legal Analyzer Ready")
        print("Commands: contract, compliance")
