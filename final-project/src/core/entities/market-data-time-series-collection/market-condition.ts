export interface MarketCondition {
  volatility_regime: string; // e.g., "low", "medium", "high"
  trend_direction: string; // e.g., "uptrend", "downtrend", "sideways"
  liquidity_level: string; // e.g., "high", "medium", "low"
}
