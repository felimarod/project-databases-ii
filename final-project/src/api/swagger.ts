import swaggerJSDoc from 'swagger-jsdoc';

const options: swaggerJSDoc.Options = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'API de Trading y Analítica',
      version: '1.0.0',
      description: 'API para acceder a datos de trading, análisis de mercado y sistema de soporte',
    },
    servers: [
      {
        url: 'http://localhost:3000',
        description: 'Servidor de desarrollo',
      },
    ],
  },
  // Rutas que contienen anotaciones de Swagger
  apis: ['./src/api/routes/*.ts', './src/api/routes/*/*.routes.ts'],
};

export const swaggerSpec = swaggerJSDoc(options);
