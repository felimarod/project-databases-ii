import { Router } from 'express';
import liquidityMetricsRoutes from './liquidity-metrics.routes';
import marketAnalysisRoutes from './market-analysis.routes';
import predictionsRoutes from './predictions.routes';
import technicalSignalsRoutes from './technical-signals.routes';
import volatilityAnalysisRoutes from './volatility-analysis.routes';
import strategyPerformanceRoutes from './strategy-performance.routes';

const router = Router();

router.use('/liquidity-metrics', liquidityMetricsRoutes);
router.use('/market-analysis', marketAnalysisRoutes);
router.use('/predictions', predictionsRoutes);
router.use('/technical-signals', technicalSignalsRoutes);
router.use('/volatility-analysis', volatilityAnalysisRoutes);
router.use('/strategy-performance', strategyPerformanceRoutes);

export default router;
