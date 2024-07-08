#!/bin/bash

# Función para esperar a que PostgreSQL esté listo
wait_for_postgres() {
    local user="admin"
    local password="admin_password"
    local db="world_cup_data"
    local host="postgres_db"  # Nombre del servicio del contenedor Docker de PostgreSQL
    local port="5432"
    
    while ! docker exec postgres_db pg_isready -U "$user" -d "$db" -h "$host" -p "$port" > /dev/null 2>&1; do
        echo "Esperando a que PostgreSQL esté listo..."
        sleep 2
    done
    
    echo "PostgreSQL está listo."
}

# Chequear si el contenedor de PostgreSQL está en ejecución y obtener su ID
check_postgres_container() {
    local container_id=$(docker ps -qf "name=postgres_db")
    
    if [ -z "$container_id" ]; then
        echo "Error: No se encontró el contenedor postgres_db en ejecución."
        exit 1
    fi
    
    echo "Contenedor de PostgreSQL encontrado: $container_id"
}

# Construir la imagen Docker
build_docker_image() {
    echo "Construyendo la imagen Docker..."
    docker build -t populate-db .
}

# Ejecutar el contenedor Docker
run_docker_container() {
    echo "Ejecutando el contenedor Docker..."
    docker run --rm populate-db
}

# Función principal
main() {
    check_postgres_container
    wait_for_postgres
    build_docker_image
    run_docker_container
}

main
