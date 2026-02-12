
# portfolio_simulator.py - Save and run locally
# Usage: python3 portfolio_simulator.py

def simulate_rebalance(
    total_portfolio_usd: float,
    bonk_current_usd: float,
    bonk_target_pct: float,
    rwa_allocation: dict
):
    """
    Simulate portfolio rebalancing
    
    Example:
    simulate_rebalance(
        total_portfolio_usd=100000,
        bonk_current_usd=45000,  # 45% currently
        bonk_target_pct=20,       # Want 20%
        rwa_allocation={
            'ondo_treasuries': 40,
            'credix_credit': 25,
            'homebase_realestate': 15
        }
    )
    """
    bonk_current_pct = (bonk_current_usd / total_portfolio_usd) * 100
    bonk_target_usd = total_portfolio_usd * (bonk_target_pct / 100)
    bonk_sell_usd = bonk_current_usd - bonk_target_usd
    
    print(f"\n📊 PORTFOLIO REBALANCE SIMULATION")
    print(f"="*50)
    print(f"Total Portfolio: ${total_portfolio_usd:,.2f}")
    print(f"\n🪙 BONK:")
    print(f"   Current: ${bonk_current_usd:,.2f} ({bonk_current_pct:.1f}%)")
    print(f"   Target:  ${bonk_target_usd:,.2f} ({bonk_target_pct:.1f}%)")
    print(f"   Action:  SELL ${bonk_sell_usd:,.2f} worth of BONK")
    
    print(f"\n🏛️ RWA ALLOCATION:")
    remaining = bonk_sell_usd
    for rwa, pct in rwa_allocation.items():
        amount = total_portfolio_usd * (pct / 100)
        print(f"   {rwa}: ${amount:,.2f} ({pct}%)")
        remaining -= amount
    
    print(f"\n💰 CASH/DRY POWDER: ${remaining:,.2f}")
    return {
        'sell_bonk_usd': bonk_sell_usd,
        'rwa_allocations': {k: total_portfolio_usd * (v/100) for k,v in rwa_allocation.items()},
        'remaining_cash': remaining
    }

# Example usage - edit these numbers
if __name__ == "__main__":
    YOUR_PORTFOLIO_SIZE = 50000  # Edit this
    YOUR_BONK_VALUE = 20000      # Edit this
    
    result = simulate_rebalance(
        total_portfolio_usd=YOUR_PORTFOLIO_SIZE,
        bonk_current_usd=YOUR_BONK_VALUE,
        bonk_target_pct=15,  # Reduce BONK to 15%
        rwa_allocation={
            'ondo_treasuries': 35,
            'credix_credit': 20,
            'homebase_realestate': 15,
            'sol_opportunities': 15  # Dry powder for dips
        }
    )
