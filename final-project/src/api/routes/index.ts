import { Router } from 'express';
import analyticsRoutes from './analytics';
import marketDataRoutes from './market-data';
import supportRoutes from './support';

const router = Router();

// Nuevas rutas organizadas
router.use('/market-data', marketDataRoutes);
router.use('/analytics', analyticsRoutes);
router.use('/support', supportRoutes);

export default router;
