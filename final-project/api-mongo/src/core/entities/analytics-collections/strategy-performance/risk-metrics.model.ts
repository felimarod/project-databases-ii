export interface RiskMetrics {
  var_95: number; // Value at Risk at 95% confidence level
  expected_shortfall: number; // Expected Shortfall
  beta: number; // Beta coefficient
}
