# Proyecto de Análisis de Trading con MongoDB y TypeScript

Este proyecto conecta una base de datos MongoDB con entidades TypeScript para almacenar y analizar datos relacionados con trading, análisis de mercado y soporte técnico.

## Estructura del Proyecto

El proyecto está organizado en los siguientes módulos:

- **Market Data Time Series Collections**: Almacena datos históricos de precios, indicadores técnicos y datos de mercado.
- **Analytics Collections**: 
  - **Market Analysis**: Métricas de liquidez, análisis de mercado, predicciones, señales técnicas y análisis de volatilidad.
  - **Strategy Performance**: Calidad de ejecución, métricas de riesgo y rendimiento de estrategias.
- **Support System Collections**: 
  - **Agents**: Información sobre agentes de soporte y sus métricas de rendimiento.
  - **Support Requests**: Solicitudes de soporte, respuestas, métricas SLA y archivos adjuntos.
  - **Trading Alerts**: Alertas de trading, instantáneas de datos de mercado y condiciones de activación.

## Requisitos previos

- Node.js (v14 o superior)
- MongoDB (local o remoto)
- TypeScript

## Instalación

1. Clona este repositorio
2. Instala las dependencias:

```bash
npm install
```

3. Crea un archivo `.env` en la raíz del proyecto con la URL de conexión a MongoDB:

```
MONGO_URL=mongodb://localhost:27017/trading_analytics_db
```

## Uso

### Iniciar MongoDB local (si es necesario)

Si no tienes una instancia de MongoDB ejecutándose, puedes usar el script incluido para iniciar una con Docker:

```bash
./start-mongodb.sh
```

### Ejecutar la aplicación

Para desarrollo (con ts-node):

```bash
npm run dev
```

Para producción:

```bash
npm run build
npm start
```

## Entidades

El proyecto utiliza varias entidades organizadas en colecciones para representar los diferentes aspectos de los datos de trading y análisis financiero.

## Conexión a MongoDB

La clase `Database` en `entities/db.ts` proporciona una conexión Singleton a MongoDB, asegurando que solo exista una instancia de conexión en toda la aplicación.
