import express, { Application } from 'express';
import cors from 'cors';
import swaggerUi from 'swagger-ui-express';
import { swaggerSpec } from './swagger';

// Importar todas las rutas
import routes from './routes';

export default class Api {
  private app: Application;
  private port: number;

  constructor(port: number = 3000) {
    this.app = express();
    this.port = port;
    this.configureMiddlewares();
    this.setupRoutes();
  }

  private configureMiddlewares(): void {
    this.app.use(cors());
    this.app.use(express.json());
    this.app.use(express.urlencoded({ extended: false }));
  }

  private setupRoutes(): void {
    // Configurar Swagger UI
    this.app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec));
    
    // Configurar rutas de la API
    this.app.use('/api', routes);

    // Ruta de verificación de salud
    this.app.get('/health', (req, res) => {
      res.json({ status: 'UP', timestamp: new Date() });
    });
  }

  public start(): void {
    this.app.listen(this.port, () => {
      console.log(`Servidor API ejecutándose en http://localhost:${this.port}`);
      console.log(`Documentación Swagger disponible en http://localhost:${this.port}/api-docs`);
    });
  }
}
