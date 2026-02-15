#!/usr/bin/env python3
"""Position sizing and risk calculator for Thomas"""

class RiskCalculator:
    def __init__(self, total_portfolio, max_position_pct=10, max_daily_loss=50):
        self.total_portfolio = total_portfolio
        self.max_position_pct = max_position_pct
        self.max_daily_loss = max_daily_loss
        
    def calculate_position(self, conviction_level, stop_loss_pct=20):
        """Calculate position size based on conviction and risk"""
        
        # Conviction multiplier (1-10 scale)
        conviction_mult = conviction_level / 10
        
        # Position size formula
        max_position = self.total_portfolio * (self.max_position_pct / 100)
        suggested_position = max_position * conviction_mult
        
        # Risk amount
        risk_amount = suggested_position * (stop_loss_pct / 100)
        
        return {
            "max_position_allowed": max_position,
            "suggested_position": suggested_position,
            "risk_amount": risk_amount,
            "position_pct_of_portfolio": (suggested_position / self.total_portfolio) * 100,
            "stop_loss_pct": stop_loss_pct,
            "max_loss_if_stopped": risk_amount
        }
    
    def check_concentration(self, current_holdings):
        """Check if portfolio is too concentrated"""
        total = sum(current_holdings.values())
        warnings = []
        
        for token, value in current_holdings.items():
            pct = (value / self.total_portfolio) * 100
            if pct > 30:
                warnings.append(f"⚠️ {token}: {pct:.1f}% - HIGH CONCENTRATION RISK")
            elif pct > 20:
                warnings.append(f"⚡ {token}: {pct:.1f}% - Monitor closely")
        
        return warnings

# Example usage
def main():
    # Edit these values
    YOUR_PORTFOLIO_SIZE = 10000  # Total portfolio in USD
    YOUR_BONK_VALUE = 3000       # Current BONK position
    
    calc = RiskCalculator(YOUR_PORTFOLIO_SIZE)
    
    # BONK rebalance scenario
    print("=" * 60)
    print("BONK REBALANCE SCENARIO")
    print("=" * 60)
    
    current_bonk_pct = (YOUR_BONK_VALUE / YOUR_PORTFOLIO_SIZE) * 100
    print(f"Current BONK: ${YOUR_BONK_VALUE} ({current_bonk_pct:.1f}% of portfolio)")
    print(f"Risk: {'HIGH' if current_bonk_pct > 30 else 'MEDIUM' if current_bonk_pct > 20 else 'OK'}")
    print()
    
    # Scenarios
    for target_pct in [15, 10, 5]:
        target_value = YOUR_PORTFOLIO_SIZE * (target_pct / 100)
        to_sell = YOUR_BONK_VALUE - target_value
        print(f"Trim to {target_pct}%: Sell ${to_sell:.0f} worth, free up capital")
    
    print()
    print("=" * 60)
    print("POSITION SIZING FOR NEW TRADE")
    print("=" * 60)
    
    for conviction in [3, 5, 7, 9]:
        sizing = calc.calculate_position(conviction)
        print(f"Conviction {conviction}/10: ${sizing['suggested_position']:.0f} "
              f"({sizing['position_pct_of_portfolio']:.1f}%), "
              f"Risk: ${sizing['risk_amount']:.0f}")

if __name__ == "__main__":
    main()
