import { Router } from 'express';
import Database from '../../../core/services/db';
import { LiquidityMetric } from '../../../core/entities/analytics-collections/martket-analysis/liquidity-metrics.model';

const router = Router();

/**
 * @swagger
 * components:
 *   schemas:
 *     LiquidityMetric:
 *       type: object
 *       required:
 *         - bid_ask_spread
 *         - market_depth
 *         - trading_volume
 *       properties:
 *         bid_ask_spread:
 *           type: number
 *           description: Promedio de spread bid-ask en pips
 *         market_depth:
 *           type: number
 *           description: Profundidad del mercado en términos de volumen
 *         trading_volume:
 *           type: number
 *           description: Volumen promedio de trading en un período
 */

/**
 * @swagger
 * /api/analytics/liquidity-metrics:
 *   get:
 *     summary: Obtiene todas las métricas de liquidez
 *     tags: [Analytics - Liquidity Metrics]
 *     responses:
 *       200:
 *         description: Lista de todas las métricas de liquidez
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 $ref: '#/components/schemas/LiquidityMetric'
 */
router.get('/', async (req, res) => {
  try {
    const db = await Database.getInstance().connect();
    const liquidityMetricsCollection = db.collection<LiquidityMetric>('liquidity_metrics');
    const metrics = await liquidityMetricsCollection.find({}).toArray();
    
    res.json(metrics);
  } catch (error) {
    console.error('Error al obtener métricas de liquidez:', error);
    res.status(500).json({ error: 'Error al obtener las métricas de liquidez' });
  }
});

/**
 * @swagger
 * /api/analytics/liquidity-metrics/{id}:
 *   get:
 *     summary: Obtiene una métrica de liquidez por su ID
 *     tags: [Analytics - Liquidity Metrics]
 *     parameters:
 *       - in: path
 *         name: id
 *         schema:
 *           type: string
 *         required: true
 *         description: ID de la métrica de liquidez
 *     responses:
 *       200:
 *         description: Detalles de la métrica de liquidez
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/LiquidityMetric'
 *       404:
 *         description: Métrica de liquidez no encontrada
 */
router.get('/:id', async (req, res) => {
  try {
    const db = await Database.getInstance().connect();
    const liquidityMetricsCollection = db.collection<LiquidityMetric>('liquidity_metrics');
    
    // Buscar por cualquier campo disponible o índice
    const metric = await liquidityMetricsCollection.findOne({}, { skip: parseInt(req.params.id) });
    
    if (!metric) {
      return res.status(404).json({ error: 'Métrica de liquidez no encontrada' });
    }
    
    res.json(metric);
  } catch (error) {
    console.error('Error al obtener métrica de liquidez:', error);
    res.status(500).json({ error: 'Error al obtener la métrica de liquidez' });
  }
});

/**
 * @swagger
 * /api/analytics/liquidity-metrics:
 *   post:
 *     summary: Crea una nueva métrica de liquidez
 *     tags: [Analytics - Liquidity Metrics]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/LiquidityMetric'
 *     responses:
 *       201:
 *         description: Métrica de liquidez creada exitosamente
 *       500:
 *         description: Error al crear la métrica de liquidez
 */
router.post('/', async (req, res) => {
  try {
    const { 
      bid_ask_spread,
      market_depth,
      trading_volume
    } = req.body;
    
    const liquidityMetricData: LiquidityMetric = {
      bid_ask_spread,
      market_depth,
      trading_volume
    };
    
    const db = await Database.getInstance().connect();
    const liquidityMetricsCollection = db.collection<LiquidityMetric>('liquidity_metrics');
    const result = await liquidityMetricsCollection.insertOne(liquidityMetricData);
    
    res.status(201).json({
      message: 'Métrica de liquidez creada exitosamente',
      id: result.insertedId
    });
  } catch (error) {
    console.error('Error al crear métrica de liquidez:', error);
    res.status(500).json({ error: 'Error al crear la métrica de liquidez' });
  }
});

export default router;
