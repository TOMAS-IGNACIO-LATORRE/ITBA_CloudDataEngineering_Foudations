#!/bin/bash

# Esperar a que PostgreSQL esté listo
until docker exec postgres_db pg_isready -U admin -d world_cup_data
do
  echo "Esperando a que PostgreSQL esté listo..."
  sleep 2
done

# Ejecutar los scripts SQL para crear las tablas
docker exec -i postgres_db psql -U admin -d world_cup_data << EOF
$(cat create_world_cup_tables.sql)
EOF

echo "Tablas creadas exitosamente."
