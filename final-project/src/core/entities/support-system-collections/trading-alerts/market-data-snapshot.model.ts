export interface MarketDataSnapshot {
    price: number; // Current price of the asset
    volume: number; // Trading volume of the asset
    indicators: {
        moving_average: number; // Moving average value
        rsi: number; // Relative Strength Index value
        macd: number; // Moving Average Convergence Divergence value
    };
}