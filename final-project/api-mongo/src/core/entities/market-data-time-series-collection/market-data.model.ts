import { Indicator } from "./indicator.model";
import { MarketCondition } from "./market-condition";
import { Price } from "./prices.model";

export interface MarketData {
  _id: string; // Unique identifier for the market data entry
  instrument: string; // Financial instrument (e.g., stock, forex)
  timestamp: Date; // Timestamp of the market data entry
  source: string; // Source of the market data (e.g., exchange, data provider)
  volume: number; // Trading volume for the instrument at the given timestamp
  spread: number; // Bid-ask spread at the given timestamp
  tick_count: number; // Number of ticks (price changes) during the period
  prices: Price[]; // Array of price data points for the instrument
  indicators: Indicator[]; // Array of technical indicators applied to the price data
  market_condition: MarketCondition; // Market condition data (e.g., volatility, trend)
}
