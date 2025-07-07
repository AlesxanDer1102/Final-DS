#!/usr/bin/env bash
echo "Desplegando servicios"
minikube start --driver=docker
eval $(minikube docker-env)

echo "Building Docker imagesÑ"
docker build -t postgres-custom:latest pregunta-4/postgres/
docker build -t user-service:latest pregunta-4/user-service/
docker build -t product-service:latest pregunta-4/product-service/

echo "Aplicamanto manifiestos Kubernetes:"
kubectl apply -f pregunta-4/k8s/postgres-deployment.yaml
kubectl apply -f pregunta-4/k8s/user-deployment.yaml
kubectl apply -f pregunta-4/k8s/product-deployment.yaml

echo "Esperando los deployments..."
kubectl wait --for=condition=available --timeout=300s deployment/postgres-deployment
kubectl wait --for=condition=available --timeout=300s deployment/user-service-deployment
kubectl wait --for=condition=available --timeout=300s deployment/product-service-deployment

echo "Verificando estado de los pods:"
kubectl get pods

echo "Verificando logs de servicios:"
echo "User Service Logs"
kubectl logs -l app=user-service --tail=10

echo "Product Service Logs"
kubectl logs -l app=product-service --tail=10

echo "Configurando port-forward para acceso a servicios"
echo "Iniciando port-forward"
# Eliminar procesos de port-forward previos
pkill -f "kubectl port-forward" 2>/dev/null || true
# Configurar port-forwards
kubectl port-forward service/user-service 8000:8000 > /dev/null 2>&1 &
USER_ID=$!
kubectl port-forward service/product-service 8001:8001 > /dev/null 2>&1 &
PRODUCT_ID=$!

echo "Esperando a que port-forward esté listo..."
sleep 5

echo "Acceso a servicios via port-forward:"
echo "User Service: http://localhost:8000"
echo "Product Service: http://localhost:8001"

echo "Comandos para probar manualmente:"
echo "curl http://localhost:8000/users/"
echo "curl http://localhost:8001/products/"

echo "Para parar port-forward:"
echo "kill $USER_ID $PRODUCT_ID"


echo "Deployment Terminado"