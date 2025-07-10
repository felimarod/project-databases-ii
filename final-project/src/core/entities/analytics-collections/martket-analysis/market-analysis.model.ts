import { LiquidityMetric } from "./liquidity-metrics.model";
import { Prediction } from "./predictions.model";
import { TechnicalSignal } from "./technical-signals.model";
import { VolatilityAnalysis } from "./volatility-analysis.model";

export interface MartketAnalysis {
  _id: string; // Unique identifier for the market analysis
  instrument: string; // Financial instrument (e.g., stock, forex)
  analysis_date: Date; // Date of the market analysis
  timeframe: string; // Timeframe of the analysis (e.g., "1D", "1H", "15M")
  technical_signals: TechnicalSignal[]; // Array of technical signals
  volatility_analysis: VolatilityAnalysis; // Volatility analysis data
  liquidity_metrics: LiquidityMetric; // Liquidity metrics data
  predictions: Prediction[]; // Array of predictions based on the analysis
}
