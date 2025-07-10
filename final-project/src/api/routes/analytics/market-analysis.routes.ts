import { Router } from 'express';
import Database from '../../../core/services/db';
import { MarketAnalysis } from '../../../core/entities/analytics-collections/martket-analysis/market-analysis.model';

const router = Router();

/**
 * @swagger
 * components:
 *   schemas:
 *     MarketAnalysis:
 *       type: object
 *       required:
 *         - instrument
 *         - analysis_date
 *         - timeframe
 *       properties:
 *         _id:
 *           type: string
 *           description: Identificador único para el análisis de mercado
 *         instrument:
 *           type: string
 *           description: Instrumento financiero (ej. acción, forex)
 *         analysis_date:
 *           type: string
 *           format: date-time
 *           description: Fecha del análisis de mercado
 *         timeframe:
 *           type: string
 *           description: Marco temporal del análisis (ej. "1D", "1H", "15M")
 *         technical_signals:
 *           type: array
 *           items:
 *             $ref: '#/components/schemas/TechnicalSignal'
 *           description: Array de señales técnicas
 *         volatility_analysis:
 *           $ref: '#/components/schemas/VolatilityAnalysis'
 *           description: Datos de análisis de volatilidad
 *         liquidity_metrics:
 *           $ref: '#/components/schemas/LiquidityMetric'
 *           description: Datos de métricas de liquidez
 *         predictions:
 *           type: array
 *           items:
 *             $ref: '#/components/schemas/Prediction'
 *           description: Array de predicciones basadas en el análisis
 */

/**
 * @swagger
 * /api/analytics/market-analysis:
 *   get:
 *     summary: Obtiene todos los análisis de mercado
 *     tags: [Analytics - Market Analysis]
 *     responses:
 *       200:
 *         description: Lista de todos los análisis de mercado
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 $ref: '#/components/schemas/MarketAnalysis'
 */
router.get('/', async (req, res) => {
  try {
    const db = await Database.getInstance().connect();
    const marketAnalysisCollection = db.collection<MarketAnalysis>('market_analysis');
    const analyses = await marketAnalysisCollection.find({}).toArray();
    
    res.json(analyses);
  } catch (error) {
    console.error('Error al obtener análisis de mercado:', error);
    res.status(500).json({ error: 'Error al obtener los análisis de mercado' });
  }
});

/**
 * @swagger
 * /api/analytics/market-analysis/{id}:
 *   get:
 *     summary: Obtiene un análisis de mercado por su ID
 *     tags: [Analytics - Market Analysis]
 *     parameters:
 *       - in: path
 *         name: id
 *         schema:
 *           type: string
 *         required: true
 *         description: ID del análisis de mercado
 *     responses:
 *       200:
 *         description: Detalles del análisis de mercado
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/MarketAnalysis'
 *       404:
 *         description: Análisis de mercado no encontrado
 */
router.get('/:id', async (req, res) => {
  try {
    const db = await Database.getInstance().connect();
    const marketAnalysisCollection = db.collection<MarketAnalysis>('market_analysis');
    const analysis = await marketAnalysisCollection.findOne({ _id: req.params.id });
    
    if (!analysis) {
      return res.status(404).json({ error: 'Análisis de mercado no encontrado' });
    }
    
    res.json(analysis);
  } catch (error) {
    console.error('Error al obtener análisis de mercado:', error);
    res.status(500).json({ error: 'Error al obtener el análisis de mercado' });
  }
});

/**
 * @swagger
 * /api/analytics/market-analysis:
 *   post:
 *     summary: Crea un nuevo análisis de mercado
 *     tags: [Analytics - Market Analysis]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/MarketAnalysis'
 *     responses:
 *       201:
 *         description: Análisis de mercado creado exitosamente
 *       500:
 *         description: Error al crear el análisis de mercado
 */
router.post('/', async (req, res) => {
  try {
    const { 
      instrument,
      analysis_date,
      timeframe,
      technical_signals,
      volatility_analysis,
      liquidity_metrics,
      predictions
    } = req.body;
    
    const marketAnalysisData: Partial<MarketAnalysis> = {
      instrument,
      analysis_date: new Date(analysis_date),
      timeframe,
      technical_signals,
      volatility_analysis,
      liquidity_metrics,
      predictions
    };
    
    const db = await Database.getInstance().connect();
    const marketAnalysisCollection = db.collection<MarketAnalysis>('market_analysis');
    const result = await marketAnalysisCollection.insertOne(marketAnalysisData as any);
    
    res.status(201).json({
      message: 'Análisis de mercado creado exitosamente',
      id: result.insertedId
    });
  } catch (error) {
    console.error('Error al crear análisis de mercado:', error);
    res.status(500).json({ error: 'Error al crear el análisis de mercado' });
  }
});

export default router;
