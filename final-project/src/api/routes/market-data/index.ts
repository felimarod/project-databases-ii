import { Router } from 'express';
import marketDataRoutes from './market-data.routes';
import indicatorsRoutes from './indicators.routes';
import pricesRoutes from './prices.routes';

const router = Router();

router.use('/market-data', marketDataRoutes);
router.use('/indicators', indicatorsRoutes);
router.use('/prices', pricesRoutes);


export default router;
