#!/bin/bash

# Script para iniciar PostgreSQL en Docker
# Creado el 10 de julio de 2025

# Nombre del contenedor
CONTAINER_NAME="trading_platform_postgres"

# Verificar si el contenedor ya existe
if [ "$(docker ps -a -q -f name=$CONTAINER_NAME)" ]; then
    echo "El contenedor $CONTAINER_NAME ya existe."
    
    # Verificar si el contenedor está corriendo
    if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
        echo "El contenedor ya está en ejecución."
    else
        echo "Iniciando el contenedor existente..."
        docker start $CONTAINER_NAME
    fi
else
    echo "Creando y ejecutando un nuevo contenedor PostgreSQL..."
    
    # Crear un volumen para persistencia de datos
    docker volume create postgres_data
    
    # Ejecutar PostgreSQL en Docker
    docker run --name $CONTAINER_NAME \
        -e POSTGRES_PASSWORD=postgres \
        -e POSTGRES_USER=postgres \
        -e POSTGRES_DB=trading_platform \
        -p 5432:5432 \
        -v postgres_data:/var/lib/postgresql/data \
        -d postgres:15
        
    echo "Esperando a que PostgreSQL inicie completamente..."
    sleep 5
fi

# Mostrar información de conexión
echo ""
echo "PostgreSQL está corriendo en Docker"
echo "-------------------------------------"
echo "Host: localhost"
echo "Puerto: 5432"
echo "Base de datos: trading_platform"
echo "Usuario: postgres"
echo "Contraseña: postgres"
echo ""
echo "Para conectarse usando psql:"
echo "psql -h localhost -p 5432 -U postgres -d trading_platform"
echo ""
echo "Para detener el contenedor:"
echo "docker stop $CONTAINER_NAME"
echo ""
