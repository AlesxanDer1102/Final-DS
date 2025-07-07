#!/usr/bin/env bash

echo "Iniciando despliegue de microservicios..."

echo "Construyendo y levantando servicios..."
docker compose -f pregunta-3/docker-compose.yaml up --build -d

# Verificar estado
echo "Estado de los servicios:"
docker compose ps

echo ""
echo "Despliegue completado!"
echo "• User Service:    http://localhost:8000"
echo "• Product Service: http://localhost:8001"
echo ""