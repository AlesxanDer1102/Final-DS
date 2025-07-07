# Infraestructura como codigo y orquestacion de microservicios

## Curso : Desarrollo de Software

## Autor : Diego Alesxander Orrego Torrejon

## Codigo : 20204161G

! Se avanzo hasta la pregunta 3 para avanzar lo que podia acabar mas facilmente

# Pregunta 3 Contenerizacion de Docker y Docker-compose

Para esta practica califica se creo en la carpe `pregunta-3` y tiene la siguiente estructura

```bash
|-pregunta-3
    |-product-service
    |   |-app.py
    |   |-Dockerfile
    |   |-requirements.txt
    |
    |-user-service
        |-app.py
    |   |-Dockerfile
    |   |-requirements.txt
```

Donde en `product-service` se creo un microservicio de gestion de productos que tiene la funciond e crear, buscar y actualizar productos y en `user-service` un microservicio de manejo de usuarios que tiene la funcionalidad de crear, listar y eliminar.

Estos a su ves presentan un `Dockerfile` con `multi-stage build` en el que primero se inicializa las dependencias necesarias y despues se copia solo los archivos necesarios en el segundo stage para correr el programa, esto puede evidenciarse mejor en otros lenguajes en los que se necesita compilar los archivos asi simplemente tendriamos que copiar los binarios compilados y dejar mas libre el runtime image

Despues de haber definido todo esto para los servicion lo que hacemos a continuacion es la orquestacion mediante `Docker-compose` el cual conectara ambos servicios en una sola red interna y les permitira compartir el volumen simulado.

Para poder tener una sola red interna lo que hacemos es definir una red la cual compartiran mediante la siguiente declaracion:

```bash
networks:
  app-network:
    driver: bridge
```

Y para el volumen compartido la siguiente declaracion en la cual servira para la data compartidad y tambien los logs:

```bash
volumes:
  shared-data:
    driver: local
  logs-data:
    driver: local
```

Para poder ejecutar el proyecto lo que se tiene que hacer el utilizar el siguiente script

```bash
# Darle permisos de ejecucion
chmod +x ./pregunta-3/deploy.sh

# Ejecutar el script desde la raiz del proyecto
./pregunta-3/deploy.sh
```

Si se quiere detener los microservicios y realizar una limpiza de los volumenes e imagenes solo se tiene que ejecutar el siguiente script

```bash
# Darle permisos de ejecucion
chmod +x ./pregunta-3/stop.sh

# Ejecutar el script desde la raiz del proyecto
./pregunta-3/stop.sh
```

# Pregunta 4 Kubernetes y Orquestacion

Estructura del proyecto

```bash
|-pregunta-4
|   |-k8s
|   | |-postgres-deployment.yaml
|   | |-product-deployment.yaml
|   | |-user-deployment.yaml
|   |
|   |-postgres
|   | |-Dockerfile
|   | |-init.sql
|   |
|   |-product-service
|   |   |-app.py
|   |   |-Dockerfile
|   |   |-requirements.txt
|   |
|   |-user-service
|   |   |-app.py
|   |   |-Dockerfile
|   |   |-requirements.txt
|
|-deploy.sh
|-cleanup.sh
```

En este proyecto lo que se hizo fue moficicar los servicios antes usados de `user-service` y `product-service` modificados para que puedan interactuar con una base de datos `postgreSql` definida en la carpeta `postgres` donde se crea e inicializa con el archivo `init.sql` al crea la imagen del contenedor del archivo `Dockerfile` dentro de la carpeta, despues estas imagenes de los servicios y la base de datos son orquestados mediante manifiestos de kubernetes llamados `postgres-deployment.yaml`,`porduct-deployment.yam` y `user-deployment.yaml` donde para `postgres-deployment.yaml` creamos usando los objetos Deployment, Service, ConfigMap y Secret, para `porduct-deployment.yam` usamos un Secret, Service,ConfigMap y un Deployment y de la misma manera para `user-deployment.yaml`, este proyecto se inicializa utilizando minikube, kubernetes, esta automatizado para usarse mediante en siguiente script

```bash
chmod +x pregunta-4\deploy.sh
pregunta-4\deploy.sh
```

Lo que hace este script es lo siguiente

Inicia minicube configura como entorno docker despues buildea las imagenes de los servicios y la base de datos luego aplica los manifiestos sobre el cluster de minikube y espera a que los deployments esten terminados para seguir, despues lo que hace es recuperar los pods para verificar los estados y revisa los logs de `prodcut-service` y `user-service` despues configura un `port-forward` en los puestos `8000` para `user-service` y `8001` para `product-service` para poder hacer la llamada haciendola desde el localhost.

```
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
```

Para poder probar que los servicios esten funcionando lo que podemos hacer es una llamada con curl despues de haber ejecutado el script de la siguiente manera:

```bash
curl http://localhost:8000/users/
curl http://localhost:8001/products/
```

Esto listara los usuarios y los productos

Y si queremos limpiar y detener minicube lo que podemos hacer es simplemente

```bash
chmod +x pregunta-4\cleanup.sh
pregunta-4\cleanup.sh
```

El log que nos da al ejecutar se guardara en `preagunta-4/logs.txt` para verificar como es que se realiza la ejecucion y deployment asi como al final nos mostrara en que puertos podemos probar para hacer uso de los servicios

# GitHub Actions para CI/CD

Se han creado GitHub Actions minimalistas para automatizar las pruebas de ambas preguntas:

## Pregunta 3 - Docker Compose CI

- **Archivo**: `.github/workflows/pregunta3-docker-deploy.yml`
- **Trigger**: Push/PR a archivos en `pregunta-3/`
- **Funcionalidad**:
  - Ejecuta el script `deploy.sh`
  - Prueba conectividad usando endpoints `/health`
  - Limpia recursos automáticamente

## Pregunta 4 - Kubernetes CI

- **Archivo**: `.github/workflows/pregunta4-k8s-deploy.yml`
- **Trigger**: Push/PR a archivos en `pregunta-4/`
- **Funcionalidad**:
  - Configura Minikube automáticamente
  - Ejecuta el script `deploy.sh`
  - Verifica conectividad de servicios
  - Limpia recursos y clusters

Ambos workflows son minimalistas y usan los scripts existentes para mantener consistencia entre el desarrollo local y CI/CD. servicios
