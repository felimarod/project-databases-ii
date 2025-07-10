export interface VolatilityAnalysis {
  current_volatility: number; // Current volatility level
  volatility_percentile: number; // Percentile of current volatility compared to historical data
  volatility_regime: "low" | "medium" | "high"; // Current volatility regime
}
