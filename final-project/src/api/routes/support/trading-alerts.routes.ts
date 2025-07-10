import { Router } from 'express';
import Database from '../../../core/services/db';
import { TradingAlert } from '../../../core/entities/support-system-collections/trading-alerts/trading-alerts.model';

const router = Router();

/**
 * @swagger
 * components:
 *   schemas:
 *     MarketDataSnapshot:
 *       type: object
 *       properties:
 *         price:
 *           type: number
 *           description: Precio actual del instrumento
 *         volume:
 *           type: number
 *           description: Volumen de negociación actual
 *         bid:
 *           type: number
 *           description: Precio de compra actual
 *         ask:
 *           type: number
 *           description: Precio de venta actual
 *         timestamp:
 *           type: string
 *           format: date-time
 *           description: Marca de tiempo de la captura de datos
 *     TriggerCondition:
 *       type: object
 *       properties:
 *         condition_type:
 *           type: string
 *           description: Tipo de condición (precio, volumen, indicador técnico)
 *         field:
 *           type: string
 *           description: Campo al que se aplica la condición
 *         operator:
 *           type: string
 *           description: Operador de la condición (mayor que, menor que, igual a)
 *         threshold:
 *           type: number
 *           description: Valor umbral para activar la condición
 *         is_triggered:
 *           type: boolean
 *           description: Indica si la condición se ha activado
 *     TradingAlert:
 *       type: object
 *       required:
 *         - user_id
 *         - instrument
 *         - alert_type
 *         - message
 *       properties:
 *         _id:
 *           type: string
 *           description: Identificador único para la alerta de trading
 *         user_id:
 *           type: string
 *           description: ID del usuario que creó la alerta
 *         strategy_id:
 *           type: string
 *           description: ID de la estrategia de trading asociada con la alerta
 *         instrument:
 *           type: string
 *           description: Instrumento financiero relacionado con la alerta (ej., acción, forex)
 *         alert_type:
 *           type: string
 *           description: Tipo de alerta (ej., alerta de precio, alerta de volumen)
 *         message:
 *           type: string
 *           description: Mensaje o descripción de la alerta
 *         confidence_score:
 *           type: number
 *           description: Puntuación de confianza de la alerta (0-100)
 *         generated_at:
 *           type: string
 *           format: date-time
 *           description: Marca de tiempo cuando se generó la alerta
 *         sent_at:
 *           type: string
 *           format: date-time
 *           description: Marca de tiempo cuando se envió la alerta al usuario
 *         is_read:
 *           type: boolean
 *           description: Indica si el usuario ha leído la alerta
 *         market_data_snapshot:
 *           $ref: '#/components/schemas/MarketDataSnapshot'
 *           description: Instantánea de datos de mercado en el momento de la generación de la alerta
 *         trigger_conditions:
 *           type: array
 *           items:
 *             $ref: '#/components/schemas/TriggerCondition'
 *           description: Condiciones que activaron la alerta
 */

/**
 * @swagger
 * /api/support/trading-alerts:
 *   get:
 *     summary: Obtiene todas las alertas de trading
 *     tags: [Support - Trading Alerts]
 *     responses:
 *       200:
 *         description: Lista de todas las alertas de trading
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 $ref: '#/components/schemas/TradingAlert'
 */
router.get('/', async (req, res) => {
  try {
    const db = await Database.getInstance().connect();
    const tradingAlertsCollection = db.collection<TradingAlert>('trading_alerts');
    const alerts = await tradingAlertsCollection.find({}).toArray();
    
    res.json(alerts);
  } catch (error) {
    console.error('Error al obtener alertas de trading:', error);
    res.status(500).json({ error: 'Error al obtener las alertas de trading' });
  }
});

/**
 * @swagger
 * /api/support/trading-alerts/{id}:
 *   get:
 *     summary: Obtiene una alerta de trading por su ID
 *     tags: [Support - Trading Alerts]
 *     parameters:
 *       - in: path
 *         name: id
 *         schema:
 *           type: string
 *         required: true
 *         description: ID de la alerta de trading
 *     responses:
 *       200:
 *         description: Detalles de la alerta de trading
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/TradingAlert'
 *       404:
 *         description: Alerta de trading no encontrada
 */
router.get('/:id', async (req, res) => {
  try {
    const db = await Database.getInstance().connect();
    const tradingAlertsCollection = db.collection<TradingAlert>('trading_alerts');
    const alert = await tradingAlertsCollection.findOne({ _id: req.params.id });
    
    if (!alert) {
      return res.status(404).json({ error: 'Alerta de trading no encontrada' });
    }
    
    res.json(alert);
  } catch (error) {
    console.error('Error al obtener alerta de trading:', error);
    res.status(500).json({ error: 'Error al obtener la alerta de trading' });
  }
});

/**
 * @swagger
 * /api/support/trading-alerts:
 *   post:
 *     summary: Crea una nueva alerta de trading
 *     tags: [Support - Trading Alerts]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/TradingAlert'
 *     responses:
 *       201:
 *         description: Alerta de trading creada exitosamente
 *       500:
 *         description: Error al crear la alerta de trading
 */
router.post('/', async (req, res) => {
  try {
    const { 
      user_id,
      strategy_id,
      instrument,
      alert_type,
      message,
      confidence_score,
      market_data_snapshot,
      trigger_conditions
    } = req.body;
    
    const now = new Date();
    
    const tradingAlertData: Partial<TradingAlert> = {
      user_id,
      strategy_id,
      instrument,
      alert_type,
      message,
      confidence_score,
      generated_at: now,
      is_read: false,
      market_data_snapshot,
      trigger_conditions
    };
    
    const db = await Database.getInstance().connect();
    const tradingAlertsCollection = db.collection<TradingAlert>('trading_alerts');
    const result = await tradingAlertsCollection.insertOne(tradingAlertData as any);
    
    res.status(201).json({
      message: 'Alerta de trading creada exitosamente',
      id: result.insertedId
    });
  } catch (error) {
    console.error('Error al crear alerta de trading:', error);
    res.status(500).json({ error: 'Error al crear la alerta de trading' });
  }
});

export default router;
