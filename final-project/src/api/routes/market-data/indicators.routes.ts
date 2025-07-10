import { Router } from 'express';
import Database from '../../../core/services/db';
import { Indicator } from '../../../core/entities/market-data-time-series-collection/indicator.model';

const router = Router();

/**
 * @swagger
 * components:
 *   schemas:
 *     Indicator:
 *       type: object
 *       required:
 *         - sma_20
 *         - ema_12
 *         - ema_26
 *         - rsi
 *         - macd
 *         - bollinger_upper
 *         - bollinger_lower
 *         - atr
 *       properties:
 *         sma_20:
 *           type: number
 *           description: Simple Moving Average para 20 períodos
 *         ema_12:
 *           type: number
 *           description: Exponential Moving Average para 12 períodos
 *         ema_26:
 *           type: number
 *           description: Exponential Moving Average para 26 períodos
 *         rsi:
 *           type: number
 *           description: Relative Strength Index
 *         macd:
 *           type: number
 *           description: Moving Average Convergence Divergence
 *         bollinger_upper:
 *           type: number
 *           description: Banda superior de Bollinger
 *         bollinger_lower:
 *           type: number
 *           description: Banda inferior de Bollinger
 *         atr:
 *           type: number
 *           description: Average True Range
 */

/**
 * @swagger
 * /api/market-data/indicators:
 *   get:
 *     summary: Obtiene todos los indicadores
 *     tags: [Indicators]
 *     responses:
 *       200:
 *         description: Lista de todos los indicadores
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 $ref: '#/components/schemas/Indicator'
 */
router.get('/', async (req, res) => {
  try {
    const db = await Database.getInstance().connect();
    const indicatorsCollection = db.collection<Indicator>('indicators');
    const indicators = await indicatorsCollection.find({}).toArray();
    
    res.json(indicators);
  } catch (error) {
    console.error('Error al obtener indicadores:', error);
    res.status(500).json({ error: 'Error al obtener los datos de indicadores' });
  }
});

/**
 * @swagger
 * /api/market-data/indicators/{id}:
 *   get:
 *     summary: Obtiene un indicador por su ID
 *     tags: [Indicators]
 *     parameters:
 *       - in: path
 *         name: id
 *         schema:
 *           type: string
 *         required: true
 *         description: ID del indicador
 *     responses:
 *       200:
 *         description: Detalles del indicador
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Indicator'
 *       404:
 *         description: Indicador no encontrado
 */
router.get('/:id', async (req, res) => {
  try {
    const db = await Database.getInstance().connect();
    const indicatorsCollection = db.collection<Indicator>('indicators');
    
    // Buscar por cualquier campo disponible o índice
    const indicator = await indicatorsCollection.findOne({}, { skip: parseInt(req.params.id) });
    
    if (!indicator) {
      return res.status(404).json({ error: 'Indicador no encontrado' });
    }
    
    res.json(indicator);
  } catch (error) {
    console.error('Error al obtener indicador:', error);
    res.status(500).json({ error: 'Error al obtener los datos del indicador' });
  }
});

/**
 * @swagger
 * /api/market-data/indicators:
 *   post:
 *     summary: Crea un nuevo indicador
 *     tags: [Indicators]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/Indicator'
 *     responses:
 *       201:
 *         description: Indicador creado exitosamente
 *       500:
 *         description: Error al crear el indicador
 */
router.post('/', async (req, res) => {
  try {
    const { 
      sma_20,
      ema_12,
      ema_26,
      rsi,
      macd,
      bollinger_upper,
      bollinger_lower,
      atr
    } = req.body;
    
    const indicatorData: Indicator = {
      sma_20,
      ema_12,
      ema_26,
      rsi,
      macd,
      bollinger_upper,
      bollinger_lower,
      atr
    };
    
    const db = await Database.getInstance().connect();
    const indicatorsCollection = db.collection<Indicator>('indicators');
    const result = await indicatorsCollection.insertOne(indicatorData);
    
    res.status(201).json({
      message: 'Indicador creado exitosamente',
      id: result.insertedId
    });
  } catch (error) {
    console.error('Error al crear indicador:', error);
    res.status(500).json({ error: 'Error al crear el indicador' });
  }
});

export default router;
