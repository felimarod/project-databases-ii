# Sistema de Base de Datos PostgreSQL para Plataforma de Trading

Este directorio contiene los scripts necesarios para configurar y ejecutar la base de datos PostgreSQL en Docker, así como para inicializar el esquema de la base de datos para la plataforma de trading.

## Archivos Disponibles

- `create_tables.sql` - Script SQL completo que define todos los tipos ENUM, tablas, restricciones, índices, triggers y particionamiento para la base de datos.
- `start-postgres-docker.sh` - Script para montar PostgreSQL en Docker.
- `execute-sql-script.sh` - Script para ejecutar el archivo SQL en la instancia de PostgreSQL.

## Instrucciones de Uso

### 1. Iniciar PostgreSQL en Docker

Primero, inicia el contenedor PostgreSQL:

```bash
cd /path/to/sql/directory
./start-postgres-docker.sh
```

Este script:
- Verifica si ya existe un contenedor con el nombre `trading_platform_postgres`
- Si existe pero no está en ejecución, lo inicia
- Si no existe, crea un nuevo contenedor con:
  - PostgreSQL 15
  - Base de datos `trading_platform`
  - Usuario `postgres` con contraseña `postgres`
  - Puerto 5432 mapeado al host
  - Un volumen de Docker para persistencia de datos

### 2. Ejecutar el Script SQL

Después de iniciar el contenedor PostgreSQL, puedes ejecutar el script SQL para crear todas las tablas:

```bash
./execute-sql-script.sh
```

Este script:
- Verifica si el archivo SQL existe
- Comprueba si el contenedor de PostgreSQL está en ejecución
- Copia el archivo SQL al contenedor
- Ejecuta el script SQL en la base de datos
- Muestra mensajes de confirmación o error según corresponda

### Estructura de la Base de Datos

El esquema de la base de datos incluye:

- 15 tipos ENUM para diferentes categorías y estados
- 24 tablas con relaciones completas
- Claves foráneas para mantener la integridad referencial
- Índices optimizados para consultas comunes
- Triggers para automatización
- Particionamiento por rango de fechas para la tabla de auditoría
- Documentación completa mediante comentarios en cada tabla

### Información de Conexión

Después de ejecutar el script `start-postgres-docker.sh`, la base de datos estará disponible con los siguientes parámetros:

- Host: localhost
- Puerto: 5432
- Base de datos: trading_platform
- Usuario: postgres
- Contraseña: postgres

Para conectarse usando psql:

```bash
psql -h localhost -p 5432 -U postgres -d trading_platform
```

## Operaciones adicionales

### Detener el contenedor

```bash
docker stop trading_platform_postgres
```

### Reiniciar el contenedor

```bash
docker start trading_platform_postgres
```

### Ver los logs del contenedor

```bash
docker logs trading_platform_postgres
```

---

Creado el 10 de julio de 2025
