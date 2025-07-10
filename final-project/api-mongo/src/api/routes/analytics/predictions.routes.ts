import { Router } from 'express';
import Database from '../../../core/services/db';
import { Prediction } from '../../../core/entities/analytics-collections/martket-analysis/predictions.model';

const router = Router();

/**
 * @swagger
 * components:
 *   schemas:
 *     Prediction:
 *       type: object
 *       required:
 *         - price_direction
 *         - confidence_level
 *         - time_horizon
 *       properties:
 *         price_direction:
 *           type: string
 *           enum: [up, down, neutral]
 *           description: Dirección predicha del precio
 *         confidence_level:
 *           type: number
 *           description: Nivel de confianza de la predicción (0 a 1)
 *         time_horizon:
 *           type: string
 *           description: Horizonte temporal para la predicción (ej. corto plazo, medio plazo, largo plazo)
 */

/**
 * @swagger
 * /api/analytics/predictions:
 *   get:
 *     summary: Obtiene todas las predicciones
 *     tags: [Analytics - Predictions]
 *     responses:
 *       200:
 *         description: Lista de todas las predicciones
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 $ref: '#/components/schemas/Prediction'
 */
router.get('/', async (req, res) => {
  try {
    const db = await Database.getInstance().connect();
    const predictionsCollection = db.collection<Prediction>('predictions');
    const predictions = await predictionsCollection.find({}).toArray();
    
    res.json(predictions);
  } catch (error) {
    console.error('Error al obtener predicciones:', error);
    res.status(500).json({ error: 'Error al obtener las predicciones' });
  }
});

/**
 * @swagger
 * /api/analytics/predictions/{id}:
 *   get:
 *     summary: Obtiene una predicción por su ID
 *     tags: [Analytics - Predictions]
 *     parameters:
 *       - in: path
 *         name: id
 *         schema:
 *           type: string
 *         required: true
 *         description: ID de la predicción
 *     responses:
 *       200:
 *         description: Detalles de la predicción
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Prediction'
 *       404:
 *         description: Predicción no encontrada
 */
router.get('/:id', async (req, res) => {
  try {
    const db = await Database.getInstance().connect();
    const predictionsCollection = db.collection<Prediction>('predictions');
    
    // Buscar por cualquier campo disponible o índice
    const prediction = await predictionsCollection.findOne({}, { skip: parseInt(req.params.id) });
    
    if (!prediction) {
      return res.status(404).json({ error: 'Predicción no encontrada' });
    }
    
    res.json(prediction);
  } catch (error) {
    console.error('Error al obtener predicción:', error);
    res.status(500).json({ error: 'Error al obtener la predicción' });
  }
});

/**
 * @swagger
 * /api/analytics/predictions:
 *   post:
 *     summary: Crea una nueva predicción
 *     tags: [Analytics - Predictions]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/Prediction'
 *     responses:
 *       201:
 *         description: Predicción creada exitosamente
 *       500:
 *         description: Error al crear la predicción
 */
router.post('/', async (req, res) => {
  try {
    const { 
      price_direction,
      confidence_level,
      time_horizon
    } = req.body;
    
    const predictionData: Prediction = {
      price_direction,
      confidence_level,
      time_horizon
    };
    
    const db = await Database.getInstance().connect();
    const predictionsCollection = db.collection<Prediction>('predictions');
    const result = await predictionsCollection.insertOne(predictionData);
    
    res.status(201).json({
      message: 'Predicción creada exitosamente',
      id: result.insertedId
    });
  } catch (error) {
    console.error('Error al crear predicción:', error);
    res.status(500).json({ error: 'Error al crear la predicción' });
  }
});

export default router;
