import { MarketDataSnapshot } from "./market-data-snapshot.model";
import { TriggerCondition } from "./trigger-conditions.model";

export interface TradingAlert {
    _id: string; // Unique identifier for the trading alert
    user_id: string; // ID of the user who created the alert
    strategy_id: string; // ID of the trading strategy associated with the alert
    instrument: string; // Financial instrument the alert is related to (e.g., stock, forex)
    alert_type: string; // Type of alert (e.g., price alert, volume alert)
    message: string; // Message or description of the alert
    confidence_score: number; // Confidence score of the alert (0-100)
    generated_at: Date; // Timestamp when the alert was generated
    sent_at: Date | null; // Timestamp when the alert was sent to the user (null if not sent yet)
    is_read: boolean; // Indicates if the user has read the alert
    market_data_snapshot: MarketDataSnapshot; // Snapshot of market data at the time of alert generation
    trigger_conditions: TriggerCondition[]; // Conditions that triggered the alert
}