import { Router } from 'express';
import Database from '../../../core/services/db';
import { MarketData } from '../../../core/entities/market-data-time-series-collection/market-data.model';

const router = Router();

/**
 * @swagger
 * components:
 *   schemas:
 *     MarketCondition:
 *       type: object
 *       properties:
 *         volatility_regime:
 *           type: string
 *           description: Régimen de volatilidad (bajo, medio, alto)
 *         trend_direction:
 *           type: string
 *           description: Dirección de la tendencia (alcista, bajista, lateral)
 *         liquidity_level:
 *           type: string
 *           description: Nivel de liquidez (alto, medio, bajo)
 *     Price:
 *       type: object
 *       properties:
 *         open:
 *           type: number
 *           description: Precio de apertura
 *         high:
 *           type: number
 *           description: Precio máximo durante el período
 *         low:
 *           type: number
 *           description: Precio mínimo durante el período
 *         close:
 *           type: number
 *           description: Precio de cierre
 *         bid:
 *           type: number
 *           description: Precio de compra
 *         ask:
 *           type: number
 *           description: Precio de venta
 *     Indicator:
 *       type: object
 *       properties:
 *         sma_20:
 *           type: number
 *           description: Media móvil simple de 20 períodos
 *         ema_12:
 *           type: number
 *           description: Media móvil exponencial de 12 períodos
 *         ema_26:
 *           type: number
 *           description: Media móvil exponencial de 26 períodos
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
 *     MarketData:
 *       type: object
 *       required:
 *         - instrument
 *         - timestamp
 *         - source
 *         - volume
 *         - spread
 *         - tick_count
 *       properties:
 *         _id:
 *           type: string
 *           description: Identificador único para el dato de mercado
 *         instrument:
 *           type: string
 *           description: Instrumento financiero (e.j., acción, forex)
 *         timestamp:
 *           type: string
 *           format: date-time
 *           description: Marca de tiempo del dato de mercado
 *         source:
 *           type: string
 *           description: Fuente del dato de mercado (e.j., exchange, proveedor de datos)
 *         volume:
 *           type: number
 *           description: Volumen de negociación para el instrumento
 *         spread:
 *           type: number
 *           description: Diferencial entre precio de compra y venta
 *         tick_count:
 *           type: number
 *           description: Número de ticks (cambios de precio) durante el período
 *         prices:
 *           type: array
 *           items:
 *             $ref: '#/components/schemas/Price'
 *           description: Array de puntos de datos de precio para el instrumento
 *         indicators:
 *           type: array
 *           items:
 *             $ref: '#/components/schemas/Indicator'
 *           description: Array de indicadores técnicos aplicados a los datos de precio
 *         market_condition:
 *           $ref: '#/components/schemas/MarketCondition'
 *           description: Datos de condición de mercado (volatilidad, tendencia)
 */

/**
 * @swagger
 * /api/market-data/market-data:
 *   get:
 *     summary: Obtiene todos los datos de mercado
 *     tags: [Market Data]
 *     responses:
 *       200:
 *         description: Lista de todos los datos de mercado
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 $ref: '#/components/schemas/MarketData'
 */
router.get('/', async (req, res) => {
  try {
    const db = await Database.getInstance().connect();
    const marketDataCollection = db.collection<MarketData>('market_data');
    const marketData = await marketDataCollection.find({}).toArray();
    
    res.json(marketData);
  } catch (error) {
    console.error('Error al obtener datos de mercado:', error);
    res.status(500).json({ error: 'Error al obtener los datos de mercado' });
  }
});

/**
 * @swagger
 * /api/market-data/market-data/{id}:
 *   get:
 *     summary: Obtiene un dato de mercado por su ID
 *     tags: [Market Data]
 *     parameters:
 *       - in: path
 *         name: id
 *         schema:
 *           type: string
 *         required: true
 *         description: ID del dato de mercado
 *     responses:
 *       200:
 *         description: Detalles del dato de mercado
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/MarketData'
 *       404:
 *         description: Dato de mercado no encontrado
 */
router.get('/:id', async (req, res) => {
  try {
    const db = await Database.getInstance().connect();
    const marketDataCollection = db.collection<MarketData>('market_data');
    const marketData = await marketDataCollection.findOne({ _id: req.params.id });
    
    if (!marketData) {
      return res.status(404).json({ error: 'Dato de mercado no encontrado' });
    }
    
    res.json(marketData);
  } catch (error) {
    console.error('Error al obtener dato de mercado:', error);
    res.status(500).json({ error: 'Error al obtener los datos del mercado' });
  }
});

/**
 * @swagger
 * /api/market-data/market-data:
 *   post:
 *     summary: Crea un nuevo dato de mercado
 *     tags: [Market Data]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/MarketData'
 *     responses:
 *       201:
 *         description: Dato de mercado creado exitosamente
 *       500:
 *         description: Error al crear el dato de mercado
 */
router.post('/', async (req, res) => {
  try {
    const { 
      instrument,
      timestamp,
      source,
      volume,
      spread,
      tick_count,
      prices,
      indicators,
      market_condition
    } = req.body;
    
    const marketDataEntry: Partial<MarketData> = {
      instrument,
      timestamp: new Date(timestamp),
      source,
      volume,
      spread,
      tick_count,
      prices,
      indicators,
      market_condition
    };
    
    const db = await Database.getInstance().connect();
    const marketDataCollection = db.collection<MarketData>('market_data');
    const result = await marketDataCollection.insertOne(marketDataEntry as any);
    
    res.status(201).json({
      message: 'Dato de mercado creado exitosamente',
      id: result.insertedId
    });
  } catch (error) {
    console.error('Error al crear dato de mercado:', error);
    res.status(500).json({ error: 'Error al crear el dato de mercado' });
  }
});

export default router;
