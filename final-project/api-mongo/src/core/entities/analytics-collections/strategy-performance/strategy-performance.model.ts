export interface StrategyPerformance {
  _id: string; // Unique identifier for the performance record
  strategy_id: string; // Unique identifier for the strategy
  date: Date; // Date of the performance record
  daily_pnl: number; // Daily profit and loss in the account currency
  trades_count: number; // Total number of trades executed on that day
  win_rate: number; // Percentage of winning trades
  avg_trade_duration: number; // Average duration of trades in seconds
  max_drawdown: number; // Maximum drawdown in percentage
  sharpe_ratio: number; // Sharpe ratio for the strategy
  volatility: number; // Daily volatility of the strategy returns
  market_conditions: string[]; // Array of market conditions during the period (e.g., "bullish", "bearish", "sideways")
}
