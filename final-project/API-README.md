# API de Trading y Analítica

Este proyecto proporciona una API RESTful para acceder a datos de trading, análisis de mercado y sistema de soporte.

## Requisitos

- Node.js (v14 o superior)
- MongoDB

## Instalación

```bash
# Clonar el repositorio
git clone <url-del-repositorio>

# Navegar al directorio del proyecto
cd final-project

# Instalar dependencias
npm install
```

## Configuración

Cree un archivo `.env` en la raíz del proyecto con la siguiente configuración:

```
MONGODB_URI=mongodb://localhost:27017/trading_analytics_db
PORT=3000
```

## Ejecución

```bash
# Compilar el proyecto TypeScript
npm run build

# Iniciar la aplicación
npm start
```

## Documentación de la API

La documentación de la API está disponible a través de Swagger UI en:

```
http://localhost:3000/api-docs
```

## Endpoints disponibles

### Precios

- `GET /api/prices`: Obtener todos los precios
- `GET /api/prices/:id`: Obtener un precio por su índice
- `POST /api/prices`: Crear un nuevo registro de precio

## Desarrollo

```bash
# Ejecutar en modo desarrollo con recarga automática
npm run dev
```

## Pruebas

```bash
# Ejecutar pruebas
npm test
```

## Estructura del proyecto

- `src/api`: Configuración de la API y rutas
- `src/core/entities`: Modelos de datos
- `src/core/services`: Servicios de la aplicación
