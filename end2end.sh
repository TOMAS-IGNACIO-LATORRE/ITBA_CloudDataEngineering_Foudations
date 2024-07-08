#!/bin/bash

# Nombre de las imágenes de Docker
populate_db_image="populate-db"
reporte_image="reporte"

# Construir la imagen para populate_db.py si no existe
if docker image inspect $populate_db_image &> /dev/null; then
    echo "La imagen $populate_db_image ya existe, utilizando la existente."
else
    echo "La imagen $populate_db_image no existe, construyéndola..."
    docker build -t $populate_db_image -f Dockerfile_populate .
fi

# Construir la imagen para reporte.py si no existe
if docker image inspect $reporte_image &> /dev/null; then
    echo "La imagen $reporte_image ya existe, utilizando la existente."
else
    echo "La imagen $reporte_image no existe, construyéndola..."
    docker build -t $reporte_image -f Dockerfile_reporte .
fi

# Levantar los servicios definidos en docker-compose.yml
docker-compose up -d

# Esperar a que PostgreSQL esté listo
echo "Esperando a que PostgreSQL esté listo..."
./wait-for-postgres.sh

# Ejecutar el script para crear las tablas en PostgreSQL
echo "Creando las tablas en PostgreSQL..."
./create_tables.sh

# Cargar datos en la base de datos utilizando el contenedor de populate_db.py
echo "Cargando datos en la base de datos..."
docker run --rm \
    -v $(pwd)/WorldCups.csv:/app/WorldCups.csv \
    --network="itba-cloud-architecting-2024_default" \
    $populate_db_image

# Ejecutar el script de reporte utilizando el contenedor de reporte.py
echo "Ejecutando el script de reporte..."
docker run --rm \
    --network="itba-cloud-architecting-2024_default" \
    -v $(pwd)/reporte.py:/app/reporte.py \
    -e DB_HOST=db \
    -e DB_USER=admin \
    -e DB_PASSWORD=admin_password \
    -e DB_NAME=world_cup_data \
    $reporte_image

# Detener y Eliminar los Contenedores
echo "Deteniendo y eliminando los contenedores..."
docker-compose down
