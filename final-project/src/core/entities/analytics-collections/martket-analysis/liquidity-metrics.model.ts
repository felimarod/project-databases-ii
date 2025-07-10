export interface LiquidityMetric {
  bid_ask_spread: number; // Average bid-ask spread in pips
  market_depth: number; // Market depth in terms of volume
  trading_volume: number; // Average trading volume over a period
}
