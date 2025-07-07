#!/usr/bin/env bash

echo "Limpiando recursos los servicios"

pkill -f "kubectl port-forward" 2>/dev/null || true

kubectl delete -f pregunta-4/k8s/product-deployment.yaml --ignore-not-found=true
kubectl delete -f pregunta-4/k8s/user-deployment.yaml --ignore-not-found=true
kubectl delete -f pregunta-4/k8s/postgres-deployment.yaml --ignore-not-found=true

kubectl delete pods --all --force --grace-period=0 2>/dev/null || true

eval $(minikube docker-env) 2>/dev/null || true
docker rmi postgres-custom:latest user-service:latest product-service:latest 2>/dev/null || true

minikube stop
minikube delete

echo "Limpieza completada"