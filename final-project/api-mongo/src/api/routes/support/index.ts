import { Router } from 'express';
import agentsRoutes from './agents.routes';
import supportRequestsRoutes from './support-requests.routes';
import tradingAlertsRoutes from './trading-alerts.routes';

const router = Router();

router.use('/agents', agentsRoutes);
router.use('/support-requests', supportRequestsRoutes);
router.use('/trading-alerts', tradingAlertsRoutes);

export default router;
