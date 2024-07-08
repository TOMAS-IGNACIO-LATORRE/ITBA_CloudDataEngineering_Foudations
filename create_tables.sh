#!/bin/bash

# Verificar si el contenedor de PostgreSQL está en ejecución y obtener su ID
container_id=$(docker ps -qf "name=postgres_db")

if [ -z "$container_id" ]; then
    echo "Error: No se encontró el contenedor postgres_db."
    exit 1
fi

# Esperar a que PostgreSQL esté listo
until docker exec "$container_id" pg_isready -U admin -d world_cup_data
do
  echo "Esperando a que PostgreSQL esté listo..."
  sleep 2
done

# Ejecutar los scripts SQL para crear las tablas
docker exec -i "$container_id" psql -U admin -d world_cup_data << EOF
$(cat create_world_cup_tables.sql)
EOF

echo "Tablas creadas exitosamente."
