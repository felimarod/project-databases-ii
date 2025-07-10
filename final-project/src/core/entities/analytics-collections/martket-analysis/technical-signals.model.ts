export interface TechnicalSignal {
  trend_direction: "up" | "down" | "neutral"; // Direction of the trend
  momentum: "strong" | "weak" | "neutral"; // Momentum strength
  support_levels: number[]; // Array of support levels
  resistance_levels: number[]; // Array of resistance levels
}
