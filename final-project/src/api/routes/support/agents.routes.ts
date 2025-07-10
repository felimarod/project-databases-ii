import { Router } from 'express';
import Database from '../../../core/services/db';
import { Agent } from '../../../core/entities/support-system-collections/agents/agent.model';

const router = Router();

/**
 * @swagger
 * components:
 *   schemas:
 *     PerformanceMetrics:
 *       type: object
 *       properties:
 *         response_time_avg:
 *           type: number
 *           description: Tiempo promedio de respuesta en minutos
 *         resolution_time_avg:
 *           type: number
 *           description: Tiempo promedio de resolución en minutos
 *         customer_satisfaction_score:
 *           type: number
 *           description: Puntuación de satisfacción del cliente (1-10)
 *     Agent:
 *       type: object
 *       required:
 *         - agent_id
 *         - name
 *         - email
 *         - department
 *         - status
 *         - specializations
 *       properties:
 *         _id:
 *           type: string
 *           description: Identificador único para el agente
 *         agent_id:
 *           type: string
 *           description: Identificador único del agente, usado para seguimiento interno
 *         name:
 *           type: string
 *           description: Nombre del agente
 *         email:
 *           type: string
 *           description: Dirección de correo electrónico del agente
 *         department:
 *           type: string
 *           description: Departamento al que pertenece el agente
 *         status:
 *           type: string
 *           description: Estado actual del agente (activo, inactivo)
 *         specializations:
 *           type: array
 *           items:
 *             type: string
 *           description: Áreas de especialización
 *         created_at:
 *           type: string
 *           format: date-time
 *           description: Fecha de creación del agente
 *         performance_metrics:
 *           $ref: '#/components/schemas/PerformanceMetrics'
 */

/**
 * @swagger
 * /api/support/agents:
 *   get:
 *     summary: Obtiene todos los agentes
 *     tags: [Support - Agents]
 *     responses:
 *       200:
 *         description: Lista de todos los agentes
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 $ref: '#/components/schemas/Agent'
 */
router.get('/', async (req, res) => {
  try {
    const db = await Database.getInstance().connect();
    const agentsCollection = db.collection<Agent>('agents');
    const agents = await agentsCollection.find({}).toArray();
    
    res.json(agents);
  } catch (error) {
    console.error('Error al obtener agentes:', error);
    res.status(500).json({ error: 'Error al obtener los datos de agentes' });
  }
});

/**
 * @swagger
 * /api/support/agents/{id}:
 *   get:
 *     summary: Obtiene un agente por su ID
 *     tags: [Support - Agents]
 *     parameters:
 *       - in: path
 *         name: id
 *         schema:
 *           type: string
 *         required: true
 *         description: ID del agente
 *     responses:
 *       200:
 *         description: Detalles del agente
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Agent'
 *       404:
 *         description: Agente no encontrado
 */
router.get('/:id', async (req, res) => {
  try {
    const db = await Database.getInstance().connect();
    const agentsCollection = db.collection<Agent>('agents');
    const agent = await agentsCollection.findOne({ _id: req.params.id });
    
    if (!agent) {
      return res.status(404).json({ error: 'Agente no encontrado' });
    }
    
    res.json(agent);
  } catch (error) {
    console.error('Error al obtener agente:', error);
    res.status(500).json({ error: 'Error al obtener los datos del agente' });
  }
});

/**
 * @swagger
 * /api/support/agents:
 *   post:
 *     summary: Crea un nuevo agente
 *     tags: [Support - Agents]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/Agent'
 *     responses:
 *       201:
 *         description: Agente creado exitosamente
 *       500:
 *         description: Error al crear el agente
 */
router.post('/', async (req, res) => {
  try {
    const { 
      agent_id,
      name,
      email,
      department,
      status,
      specializations,
      performance_metrics
    } = req.body;
    
    const agentData: Partial<Agent> = {
      agent_id,
      name,
      email,
      department,
      status,
      specializations,
      created_at: new Date(),
      performance_metrics
    };
    
    const db = await Database.getInstance().connect();
    const agentsCollection = db.collection<Agent>('agents');
    const result = await agentsCollection.insertOne(agentData as any);
    
    res.status(201).json({
      message: 'Agente creado exitosamente',
      id: result.insertedId
    });
  } catch (error) {
    console.error('Error al crear agente:', error);
    res.status(500).json({ error: 'Error al crear el agente' });
  }
});

export default router;
