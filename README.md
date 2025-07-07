# Infraestructura como codigo y orquestacion de microservicios

## Curso : Desarrollo de Software
## Autor : Diego Alesxander Orrego Torrejon
## Codigo : 20204161G



# Pregunta 3 Contenerizacion de Docker y Docker-compose

Para esta practica califica se creo en la carpe `pregunta-3` y tiene la siguiente estructura

```
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

Despues de haber definido todo esto para los servicion lo que hacemos a continuacion es la orquestacion mediante `Docker-compose`  el cual conectara ambos servicios en una sola red interna y les permitira compartir el volumen simulado.

Para poder tener una sola red interna lo que hacemos es definir una red la cual compartiran mediante la siguiente declaracion:
```
networks:
  app-network:
    driver: bridge
```

Y para el volumen compartido la siguiente declaracion en la cual servira para la data compartidad y tambien los logs:

```
volumes:
  shared-data:
    driver: local
  logs-data:
    driver: local
```

Para poder ejecutar el proyecto lo que se tiene que hacer el utilizar el siguiente script

```
# Darle permisos de ejecucion
chmod +x ./pregunta-3/deploy.sh

# Ejecutar el script desde la raiz del proyecto
./pregunta-3/deploy.sh
```

Si se quiere detener los microservicios y realizar una limpiza de los volumenes e imagenes solo se tiene que ejecutar el siguiente script

```
# Darle permisos de ejecucion
chmod +x ./pregunta-3/stop.sh

# Ejecutar el script desde la raiz del proyecto
./pregunta-3/stop.sh
```