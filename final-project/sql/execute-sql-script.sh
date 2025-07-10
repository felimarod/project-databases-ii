#!/bin/bash

# Script para ejecutar el archivo SQL en PostgreSQL Docker
# Creado el 10 de julio de 2025

# Nombre del contenedor
CONTAINER_NAME="trading_platform_postgres"

# Ruta al archivo SQL (relativa a este script)
SQL_FILE="create_tables.sql"
ABSOLUTE_SQL_PATH=$(realpath $SQL_FILE)

# Verificar si el archivo SQL existe
if [ ! -f "$SQL_FILE" ]; then
    echo "Error: El archivo SQL '$SQL_FILE' no existe en la ubicación actual."
    exit 1
fi

# Verificar si el contenedor está corriendo
if [ ! "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
    echo "El contenedor PostgreSQL no está en ejecución."
    echo "Por favor, ejecuta primero el script start-postgres-docker.sh"
    exit 1
fi

echo "Ejecutando el archivo SQL en PostgreSQL..."
echo "Archivo: $ABSOLUTE_SQL_PATH"

# Copiar el archivo SQL al contenedor
echo "Copiando el archivo SQL al contenedor..."
docker cp "$ABSOLUTE_SQL_PATH" "$CONTAINER_NAME:/tmp/create_tables.sql"

# Ejecutar el archivo SQL en PostgreSQL
echo "Ejecutando el script SQL..."
docker exec -it $CONTAINER_NAME psql -U postgres -d trading_platform -f /tmp/create_tables.sql

# Verificar resultado
if [ $? -eq 0 ]; then
    echo ""
    echo "¡Script SQL ejecutado con éxito!"
    echo "La base de datos trading_platform ha sido configurada."
    echo ""
    echo "Para verificar las tablas creadas, puedes ejecutar:"
    echo "docker exec -it $CONTAINER_NAME psql -U postgres -d trading_platform -c '\\dt'"
else
    echo ""
    echo "Ocurrió un error al ejecutar el script SQL."
    echo "Revisa los mensajes de error para más información."
fi
