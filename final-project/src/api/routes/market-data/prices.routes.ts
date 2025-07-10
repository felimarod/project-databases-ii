import { Router } from 'express';
import Database from '../../../core/services/db';
import { Price } from '../../../core/entities';

const router = Router();

/**
 * @swagger
 * components:
 *   schemas:
 *     Price:
 *       type: object
 *       required:
 *         - open
 *         - close
 *         - high
 *         - low
 *         - ask
 *         - bid
 *       properties:
 *         open:
 *           type: number
 *           description: Precio de apertura
 *         close:
 *           type: number
 *           description: Precio de cierre
 *         high:
 *           type: number
 *           description: Precio máximo
 *         low:
 *           type: number
 *           description: Precio mínimo
 *         ask:
 *           type: number
 *           description: Precio de venta
 *         bid:
 *           type: number
 *           description: Precio de compra
 *       example:
 *         open: 100.50
 *         close: 101.25
 *         high: 102.00
 *         low: 100.00
 *         ask: 101.30
 *         bid: 101.20
 */

/**
 * @swagger
 * /api/market-data/prices:
 *   get:
 *     summary: Obtiene todos los precios
 *     tags: [Prices]
 *     responses:
 *       200:
 *         description: Lista de todos los precios
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 $ref: '#/components/schemas/Price'
 */
router.get('/', async (req, res) => {
  try {
    const db = await Database.getInstance().connect();
    const pricesCollection = db.collection<Price>('prices');
    const prices = await pricesCollection.find({}).toArray();
    
    res.json(prices);
  } catch (error) {
    console.error('Error al obtener precios:', error);
    res.status(500).json({ error: 'Error al obtener los datos de precios' });
  }
});

/**
 * @swagger
 * /api/market-data/prices/{id}:
 *   get:
 *     summary: Obtiene un precio por su ID
 *     tags: [Prices]
 *     parameters:
 *       - in: path
 *         name: id
 *         schema:
 *           type: string
 *         required: true
 *         description: ID del precio
 *     responses:
 *       200:
 *         description: Detalles del precio
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Price'
 *       404:
 *         description: Precio no encontrado
 */
router.get('/:id', async (req, res) => {
  try {
    const db = await Database.getInstance().connect();
    const pricesCollection = db.collection<Price>('prices');
    
    // Buscar por cualquier campo disponible
    const price = await pricesCollection.findOne({}, { skip: parseInt(req.params.id) });
    
    if (!price) {
      return res.status(404).json({ error: 'Precio no encontrado' });
    }
    
    res.json(price);
  } catch (error) {
    console.error('Error al obtener precio:', error);
    res.status(500).json({ error: 'Error al obtener los datos del precio' });
  }
});

/**
 * @swagger
 * /api/market-data/prices:
 *   post:
 *     summary: Crea un nuevo registro de precio
 *     tags: [Prices]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/Price'
 *     responses:
 *       201:
 *         description: Precio creado exitosamente
 *       500:
 *         description: Error al crear el precio
 */
router.post('/', async (req, res) => {
  try {
    const { open, close, high, low, ask, bid } = req.body;
    
    const priceData: Price = {
      open,
      close,
      high,
      low,
      ask,
      bid
    };
    
    const db = await Database.getInstance().connect();
    const pricesCollection = db.collection<Price>('prices');
    const result = await pricesCollection.insertOne(priceData);
    
    res.status(201).json({
      message: 'Precio creado exitosamente',
      id: result.insertedId
    });
  } catch (error) {
    console.error('Error al crear precio:', error);
    res.status(500).json({ error: 'Error al crear el registro de precio' });
  }
});

export default router;
