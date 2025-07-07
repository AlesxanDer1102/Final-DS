#!/usr/bin/env bash

echo "Deteniendo microservicios..."

# Parar y remover contenedores
echo "Parando contenedores..."
docker compose -f pregunta-3/docker-compose.yaml down

# Remover volúmenes también 
echo "Removiendo volúmenes..."
docker compose -f pregunta-3/docker-compose.yaml down --volumes

# Limpiar imágenes no utilizadas 
echo "Limpiando imágenes no utilizadas..."
docker image prune -f

echo ""
echo "Todos los servicios han sido detenidos!"
echo "Volúmenes removidos"
echo "Imágenes no utilizadas limpiadas"
echo ""
echo "Para volver a desplegar: .pregunta-3/deploy.sh"
