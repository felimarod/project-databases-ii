import { Router } from 'express';
import Database from '../../../core/services/db';
import { TechnicalSignal } from '../../../core/entities/analytics-collections/martket-analysis/technical-signals.model';

const router = Router();

/**
 * @swagger
 * components:
 *   schemas:
 *     TechnicalSignal:
 *       type: object
 *       required:
 *         - trend_direction
 *         - momentum
 *         - support_levels
 *         - resistance_levels
 *       properties:
 *         trend_direction:
 *           type: string
 *           enum: [up, down, neutral]
 *           description: Dirección de la tendencia
 *         momentum:
 *           type: string
 *           enum: [strong, weak, neutral]
 *           description: Fuerza del momentum
 *         support_levels:
 *           type: array
 *           items:
 *             type: number
 *           description: Array de niveles de soporte
 *         resistance_levels:
 *           type: array
 *           items:
 *             type: number
 *           description: Array de niveles de resistencia
 */

/**
 * @swagger
 * /api/analytics/technical-signals:
 *   get:
 *     summary: Obtiene todas las señales técnicas
 *     tags: [Analytics - Technical Signals]
 *     responses:
 *       200:
 *         description: Lista de todas las señales técnicas
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 $ref: '#/components/schemas/TechnicalSignal'
 */
router.get('/', async (req, res) => {
  try {
    const db = await Database.getInstance().connect();
    const technicalSignalsCollection = db.collection<TechnicalSignal>('technical_signals');
    const signals = await technicalSignalsCollection.find({}).toArray();
    
    res.json(signals);
  } catch (error) {
    console.error('Error al obtener señales técnicas:', error);
    res.status(500).json({ error: 'Error al obtener las señales técnicas' });
  }
});

/**
 * @swagger
 * /api/analytics/technical-signals/{id}:
 *   get:
 *     summary: Obtiene una señal técnica por su ID
 *     tags: [Analytics - Technical Signals]
 *     parameters:
 *       - in: path
 *         name: id
 *         schema:
 *           type: string
 *         required: true
 *         description: ID de la señal técnica
 *     responses:
 *       200:
 *         description: Detalles de la señal técnica
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/TechnicalSignal'
 *       404:
 *         description: Señal técnica no encontrada
 */
router.get('/:id', async (req, res) => {
  try {
    const db = await Database.getInstance().connect();
    const technicalSignalsCollection = db.collection<TechnicalSignal>('technical_signals');
    
    // Buscar por cualquier campo disponible o índice
    const signal = await technicalSignalsCollection.findOne({}, { skip: parseInt(req.params.id) });
    
    if (!signal) {
      return res.status(404).json({ error: 'Señal técnica no encontrada' });
    }
    
    res.json(signal);
  } catch (error) {
    console.error('Error al obtener señal técnica:', error);
    res.status(500).json({ error: 'Error al obtener la señal técnica' });
  }
});

/**
 * @swagger
 * /api/analytics/technical-signals:
 *   post:
 *     summary: Crea una nueva señal técnica
 *     tags: [Analytics - Technical Signals]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/TechnicalSignal'
 *     responses:
 *       201:
 *         description: Señal técnica creada exitosamente
 *       500:
 *         description: Error al crear la señal técnica
 */
router.post('/', async (req, res) => {
  try {
    const { 
      trend_direction,
      momentum,
      support_levels,
      resistance_levels
    } = req.body;
    
    const technicalSignalData: TechnicalSignal = {
      trend_direction,
      momentum,
      support_levels,
      resistance_levels
    };
    
    const db = await Database.getInstance().connect();
    const technicalSignalsCollection = db.collection<TechnicalSignal>('technical_signals');
    const result = await technicalSignalsCollection.insertOne(technicalSignalData);
    
    res.status(201).json({
      message: 'Señal técnica creada exitosamente',
      id: result.insertedId
    });
  } catch (error) {
    console.error('Error al crear señal técnica:', error);
    res.status(500).json({ error: 'Error al crear la señal técnica' });
  }
});

export default router;
