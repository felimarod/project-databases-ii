#!/bin/bash

# Script para iniciar MongoDB localmente con Docker

echo "Iniciando MongoDB con Docker..."

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "Docker no está instalado. Por favor instala Docker primero."
    exit 1
fi

# Comprobar si ya existe un contenedor de MongoDB
if docker ps -a | grep -q mongodb-trading; then
    echo "El contenedor MongoDB ya existe, iniciándolo..."
    docker start mongodb-trading
else
    echo "Creando y ejecutando nuevo contenedor MongoDB..."
    docker run -d \
        --name mongodb-trading \
        -p 27017:27017 \
        -v mongodb_trading_data:/data/db \
        -e MONGO_INITDB_DATABASE=trading_analytics_db \
        mongo:latest
fi

echo "MongoDB está ejecutándose en mongodb://localhost:27017/trading_analytics_db"
echo "Para detener MongoDB usa: docker stop mongodb-trading"
