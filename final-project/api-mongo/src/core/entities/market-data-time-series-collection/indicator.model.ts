export interface Indicator {
    sma_20: number; // Simple Moving Average for 20 periods
    ema_12: number; // Exponential Moving Average for 12 periods
    ema_26: number; // Exponential Moving Average for 26 periods
    rsi: number; // Relative Strength Index
    macd: number; // Moving Average Convergence Divergence
    bollinger_upper: number; // Upper Bollinger Band
    bollinger_lower: number; // Lower Bollinger Band
    atr: number; // Average True Range
}