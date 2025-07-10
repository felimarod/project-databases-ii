export interface TriggerCondition {
    rsi_threshold: number; // RSI threshold for triggering the alert
    price_change: number; // Percentage change in price to trigger the alert
    volume_spike: number; // Minimum volume spike to trigger the alert
}