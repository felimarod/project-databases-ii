import { Router } from 'express';
import Database from '../../../core/services/db';
import { StrategyPerformance } from '../../../core/entities/analytics-collections/strategy-performance/strategy-performance.model';

const router = Router();

/**
 * @swagger
 * components:
 *   schemas:
 *     StrategyPerformance:
 *       type: object
 *       required:
 *         - strategy_id
 *         - date
 *         - daily_pnl
 *         - trades_count
 *         - win_rate
 *       properties:
 *         _id:
 *           type: string
 *           description: Identificador único para el registro de rendimiento
 *         strategy_id:
 *           type: string
 *           description: Identificador único para la estrategia
 *         date:
 *           type: string
 *           format: date-time
 *           description: Fecha del registro de rendimiento
 *         daily_pnl:
 *           type: number
 *           description: Ganancias y pérdidas diarias en la moneda de la cuenta
 *         trades_count:
 *           type: number
 *           description: Número total de operaciones ejecutadas ese día
 *         win_rate:
 *           type: number
 *           description: Porcentaje de operaciones ganadoras
 *         avg_trade_duration:
 *           type: number
 *           description: Duración media de las operaciones en segundos
 *         max_drawdown:
 *           type: number
 *           description: Máxima reducción en porcentaje
 *         sharpe_ratio:
 *           type: number
 *           description: Ratio de Sharpe para la estrategia
 *         volatility:
 *           type: number
 *           description: Volatilidad diaria de los retornos de la estrategia
 *         market_conditions:
 *           type: array
 *           items:
 *             type: string
 *           description: Array de condiciones de mercado durante el período
 */

/**
 * @swagger
 * /api/analytics/strategy-performance:
 *   get:
 *     summary: Obtiene todos los registros de rendimiento de estrategia
 *     tags: [Analytics - Strategy Performance]
 *     responses:
 *       200:
 *         description: Lista de todos los registros de rendimiento
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 $ref: '#/components/schemas/StrategyPerformance'
 */
router.get('/', async (req, res) => {
  try {
    const db = await Database.getInstance().connect();
    const strategyPerformanceCollection = db.collection<StrategyPerformance>('strategy_performance');
    const performances = await strategyPerformanceCollection.find({}).toArray();
    
    res.json(performances);
  } catch (error) {
    console.error('Error al obtener rendimientos de estrategia:', error);
    res.status(500).json({ error: 'Error al obtener los rendimientos de estrategia' });
  }
});

/**
 * @swagger
 * /api/analytics/strategy-performance/{id}:
 *   get:
 *     summary: Obtiene un registro de rendimiento de estrategia por su ID
 *     tags: [Analytics - Strategy Performance]
 *     parameters:
 *       - in: path
 *         name: id
 *         schema:
 *           type: string
 *         required: true
 *         description: ID del registro de rendimiento
 *     responses:
 *       200:
 *         description: Detalles del registro de rendimiento
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/StrategyPerformance'
 *       404:
 *         description: Registro de rendimiento no encontrado
 */
router.get('/:id', async (req, res) => {
  try {
    const db = await Database.getInstance().connect();
    const strategyPerformanceCollection = db.collection<StrategyPerformance>('strategy_performance');
    const performance = await strategyPerformanceCollection.findOne({ _id: req.params.id });
    
    if (!performance) {
      return res.status(404).json({ error: 'Registro de rendimiento no encontrado' });
    }
    
    res.json(performance);
  } catch (error) {
    console.error('Error al obtener rendimiento de estrategia:', error);
    res.status(500).json({ error: 'Error al obtener el rendimiento de estrategia' });
  }
});

/**
 * @swagger
 * /api/analytics/strategy-performance:
 *   post:
 *     summary: Crea un nuevo registro de rendimiento de estrategia
 *     tags: [Analytics - Strategy Performance]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/StrategyPerformance'
 *     responses:
 *       201:
 *         description: Registro de rendimiento creado exitosamente
 *       500:
 *         description: Error al crear el registro de rendimiento
 */
router.post('/', async (req, res) => {
  try {
    const { 
      strategy_id,
      date,
      daily_pnl,
      trades_count,
      win_rate,
      avg_trade_duration,
      max_drawdown,
      sharpe_ratio,
      volatility,
      market_conditions
    } = req.body;
    
    const strategyPerformanceData: Partial<StrategyPerformance> = {
      strategy_id,
      date: new Date(date),
      daily_pnl,
      trades_count,
      win_rate,
      avg_trade_duration,
      max_drawdown,
      sharpe_ratio,
      volatility,
      market_conditions
    };
    
    const db = await Database.getInstance().connect();
    const strategyPerformanceCollection = db.collection<StrategyPerformance>('strategy_performance');
    const result = await strategyPerformanceCollection.insertOne(strategyPerformanceData as any);
    
    res.status(201).json({
      message: 'Registro de rendimiento creado exitosamente',
      id: result.insertedId
    });
  } catch (error) {
    console.error('Error al crear rendimiento de estrategia:', error);
    res.status(500).json({ error: 'Error al crear el rendimiento de estrategia' });
  }
});

export default router;
