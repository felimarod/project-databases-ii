export interface Prediction {
  price_direction: "up" | "down" | "neutral"; // Predicted price direction
  confidence_level: number; // Confidence level of the prediction (0 to 1)
  time_horizon: string; // Time horizon for the prediction (e.g., "short-term", "medium-term", "long-term")
}
