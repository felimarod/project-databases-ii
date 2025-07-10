import { Router } from 'express';
import Database from '../../../core/services/db';
import { SupportRequest } from '../../../core/entities/support-system-collections/support-requests/support-request.model';

const router = Router();

/**
 * @swagger
 * components:
 *   schemas:
 *     UserAttachment:
 *       type: object
 *       properties:
 *         file_name:
 *           type: string
 *           description: Nombre del archivo adjunto
 *         file_type:
 *           type: string
 *           description: Tipo de archivo (imagen, pdf, etc.)
 *         file_size:
 *           type: number
 *           description: Tamaño del archivo en bytes
 *         upload_date:
 *           type: string
 *           format: date-time
 *           description: Fecha en que se subió el archivo
 *         content_url:
 *           type: string
 *           description: URL para acceder al contenido del archivo
 *     Response:
 *       type: object
 *       properties:
 *         response_id:
 *           type: string
 *           description: ID único de la respuesta
 *         agent_id:
 *           type: string
 *           description: ID del agente que proporcionó la respuesta
 *         content:
 *           type: string
 *           description: Contenido de la respuesta
 *         created_at:
 *           type: string
 *           format: date-time
 *           description: Fecha de creación de la respuesta
 *         is_internal:
 *           type: boolean
 *           description: Indica si la respuesta es interna (solo visible para agentes)
 *     SupportRequest:
 *       type: object
 *       required:
 *         - ticket_id
 *         - user_id
 *         - type
 *         - category
 *         - priority
 *         - status
 *         - subject
 *         - description
 *       properties:
 *         _id:
 *           type: string
 *           description: ID único de la solicitud de soporte
 *         ticket_id:
 *           type: string
 *           description: ID del ticket de soporte
 *         user_id:
 *           type: string
 *           description: ID del usuario que creó la solicitud
 *         type:
 *           type: string
 *           description: Tipo de solicitud de soporte
 *         category:
 *           type: string
 *           description: Categoría de la solicitud
 *         priority:
 *           type: string
 *           description: Prioridad de la solicitud (baja, media, alta, crítica)
 *         status:
 *           type: string
 *           description: Estado de la solicitud (abierta, en progreso, cerrada)
 *         subject:
 *           type: string
 *           description: Asunto de la solicitud
 *         description:
 *           type: string
 *           description: Descripción detallada de la solicitud
 *         created_at:
 *           type: string
 *           format: date-time
 *           description: Fecha de creación de la solicitud
 *         updated_at:
 *           type: string
 *           format: date-time
 *           description: Fecha de última actualización de la solicitud
 *         resolved_at:
 *           type: string
 *           format: date-time
 *           description: Fecha de resolución de la solicitud
 *         tags:
 *           type: array
 *           items:
 *             type: string
 *           description: Etiquetas relacionadas con la solicitud
 *         escalation_level:
 *           type: number
 *           description: Nivel de escalamiento de la solicitud
 *         user_attachments:
 *           type: array
 *           items:
 *             $ref: '#/components/schemas/UserAttachment'
 *           description: Archivos adjuntos por el usuario
 *         responses:
 *           type: array
 *           items:
 *             $ref: '#/components/schemas/Response'
 *           description: Respuestas a la solicitud
 */

/**
 * @swagger
 * /api/support/support-requests:
 *   get:
 *     summary: Obtiene todas las solicitudes de soporte
 *     tags: [Support - Support Requests]
 *     responses:
 *       200:
 *         description: Lista de todas las solicitudes de soporte
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 $ref: '#/components/schemas/SupportRequest'
 */
router.get('/', async (req, res) => {
  try {
    const db = await Database.getInstance().connect();
    const supportRequestsCollection = db.collection<SupportRequest>('support_requests');
    const requests = await supportRequestsCollection.find({}).toArray();
    
    res.json(requests);
  } catch (error) {
    console.error('Error al obtener solicitudes de soporte:', error);
    res.status(500).json({ error: 'Error al obtener las solicitudes de soporte' });
  }
});

/**
 * @swagger
 * /api/support/support-requests/{id}:
 *   get:
 *     summary: Obtiene una solicitud de soporte por su ID
 *     tags: [Support - Support Requests]
 *     parameters:
 *       - in: path
 *         name: id
 *         schema:
 *           type: string
 *         required: true
 *         description: ID de la solicitud de soporte
 *     responses:
 *       200:
 *         description: Detalles de la solicitud de soporte
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/SupportRequest'
 *       404:
 *         description: Solicitud de soporte no encontrada
 */
router.get('/:id', async (req, res) => {
  try {
    const db = await Database.getInstance().connect();
    const supportRequestsCollection = db.collection<SupportRequest>('support_requests');
    const request = await supportRequestsCollection.findOne({ _id: req.params.id });
    
    if (!request) {
      return res.status(404).json({ error: 'Solicitud de soporte no encontrada' });
    }
    
    res.json(request);
  } catch (error) {
    console.error('Error al obtener solicitud de soporte:', error);
    res.status(500).json({ error: 'Error al obtener la solicitud de soporte' });
  }
});

/**
 * @swagger
 * /api/support/support-requests:
 *   post:
 *     summary: Crea una nueva solicitud de soporte
 *     tags: [Support - Support Requests]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/SupportRequest'
 *     responses:
 *       201:
 *         description: Solicitud de soporte creada exitosamente
 *       500:
 *         description: Error al crear la solicitud de soporte
 */
router.post('/', async (req, res) => {
  try {
    const { 
      ticket_id,
      user_id,
      type,
      category,
      priority,
      status,
      subject,
      description,
      tags,
      escalation_level,
      user_attachments,
      responses
    } = req.body;
    
    const now = new Date();
    
    const supportRequestData: Partial<SupportRequest> = {
      ticket_id,
      user_id,
      type,
      category,
      priority,
      status,
      subject,
      description,
      created_at: now,
      updated_at: now,
      tags,
      escalation_level,
      user_attachments,
      responses
    };
    
    const db = await Database.getInstance().connect();
    const supportRequestsCollection = db.collection<SupportRequest>('support_requests');
    const result = await supportRequestsCollection.insertOne(supportRequestData as any);
    
    res.status(201).json({
      message: 'Solicitud de soporte creada exitosamente',
      id: result.insertedId
    });
  } catch (error) {
    console.error('Error al crear solicitud de soporte:', error);
    res.status(500).json({ error: 'Error al crear la solicitud de soporte' });
  }
});

export default router;
