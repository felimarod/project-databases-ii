import { Router } from 'express';
import Database from '../../../core/services/db';
import { VolatilityAnalysis } from '../../../core/entities/analytics-collections/martket-analysis/volatility-analysis.model';

const router = Router();

/**
 * @swagger
 * components:
 *   schemas:
 *     VolatilityAnalysis:
 *       type: object
 *       required:
 *         - current_volatility
 *         - volatility_percentile
 *         - volatility_regime
 *       properties:
 *         current_volatility:
 *           type: number
 *           description: Nivel actual de volatilidad
 *         volatility_percentile:
 *           type: number
 *           description: Percentil de volatilidad actual comparado con datos históricos
 *         volatility_regime:
 *           type: string
 *           enum: [low, medium, high]
 *           description: Régimen de volatilidad actual
 */

/**
 * @swagger
 * /api/analytics/volatility-analysis:
 *   get:
 *     summary: Obtiene todos los análisis de volatilidad
 *     tags: [Analytics - Volatility Analysis]
 *     responses:
 *       200:
 *         description: Lista de todos los análisis de volatilidad
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 $ref: '#/components/schemas/VolatilityAnalysis'
 */
router.get('/', async (req, res) => {
  try {
    const db = await Database.getInstance().connect();
    const volatilityAnalysisCollection = db.collection<VolatilityAnalysis>('volatility_analysis');
    const analyses = await volatilityAnalysisCollection.find({}).toArray();
    
    res.json(analyses);
  } catch (error) {
    console.error('Error al obtener análisis de volatilidad:', error);
    res.status(500).json({ error: 'Error al obtener los análisis de volatilidad' });
  }
});

/**
 * @swagger
 * /api/analytics/volatility-analysis/{id}:
 *   get:
 *     summary: Obtiene un análisis de volatilidad por su ID
 *     tags: [Analytics - Volatility Analysis]
 *     parameters:
 *       - in: path
 *         name: id
 *         schema:
 *           type: string
 *         required: true
 *         description: ID del análisis de volatilidad
 *     responses:
 *       200:
 *         description: Detalles del análisis de volatilidad
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/VolatilityAnalysis'
 *       404:
 *         description: Análisis de volatilidad no encontrado
 */
router.get('/:id', async (req, res) => {
  try {
    const db = await Database.getInstance().connect();
    const volatilityAnalysisCollection = db.collection<VolatilityAnalysis>('volatility_analysis');
    
    // Buscar por cualquier campo disponible o índice
    const analysis = await volatilityAnalysisCollection.findOne({}, { skip: parseInt(req.params.id) });
    
    if (!analysis) {
      return res.status(404).json({ error: 'Análisis de volatilidad no encontrado' });
    }
    
    res.json(analysis);
  } catch (error) {
    console.error('Error al obtener análisis de volatilidad:', error);
    res.status(500).json({ error: 'Error al obtener el análisis de volatilidad' });
  }
});

/**
 * @swagger
 * /api/analytics/volatility-analysis:
 *   post:
 *     summary: Crea un nuevo análisis de volatilidad
 *     tags: [Analytics - Volatility Analysis]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/VolatilityAnalysis'
 *     responses:
 *       201:
 *         description: Análisis de volatilidad creado exitosamente
 *       500:
 *         description: Error al crear el análisis de volatilidad
 */
router.post('/', async (req, res) => {
  try {
    const { 
      current_volatility,
      volatility_percentile,
      volatility_regime
    } = req.body;
    
    const volatilityAnalysisData: VolatilityAnalysis = {
      current_volatility,
      volatility_percentile,
      volatility_regime
    };
    
    const db = await Database.getInstance().connect();
    const volatilityAnalysisCollection = db.collection<VolatilityAnalysis>('volatility_analysis');
    const result = await volatilityAnalysisCollection.insertOne(volatilityAnalysisData);
    
    res.status(201).json({
      message: 'Análisis de volatilidad creado exitosamente',
      id: result.insertedId
    });
  } catch (error) {
    console.error('Error al crear análisis de volatilidad:', error);
    res.status(500).json({ error: 'Error al crear el análisis de volatilidad' });
  }
});

export default router;
