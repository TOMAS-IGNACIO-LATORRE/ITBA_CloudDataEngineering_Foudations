# Ejercicio 6: Documentación y ejecución end2end

Agregue una sección al README.md comentando como resolvió los ejercicios, linkeando al archivo con la descripción del dataset y explicando como ejecutar un script de BASH para ejecutar todo el proceso end2end desde la creación del container, operaciones de DDL, carga de datos y consultas. Para esto crear el archivo de BASH correspondiente.

- ## Archivos finales

### 1. Dockerfile

El Dockerfile define la configuración para construir una imagen de Docker incluyendo las dependencias necesarias en un archivo requirements.txt que lo ejecuta y los scripts para interactuar con una base de datos PostgreSQL. Este archivo se utiliza para construir las imágenes que ejecutarán los scripts `populate_db.py` y `reporte.py`.

### 2. populate_db.py

Este script se encarga de cargar datos desde un archivo CSV (`WorldCups.csv`) en una tabla llamada `world_cups` dentro de una base de datos PostgreSQL utilizando la imagen de Docker postgres:12.7. Realiza la creación de la tabla si no existe, maneja las restricciones de integridad y asegura la carga de datos de manera segura.

### 3. reporte.py

El script `reporte.py` corre las consultas SQL a la base de datos PostgreSQL para obtener los insights de nuestro dataset. Las consultas responden a todas las preguntas de negocio efectuadas y detalladas en el archivo [Detalle_Dataset.md](https://github.com/TOMAS-IGNACIO-LATORRE/ITBA_CloudDataEngineering_Foudations/blob/ejercicio-5/Detalle_Dataset.md)

### 4. create_world_cup_tables.sql

Este archivo SQL ejecuta las queries de SQL para crear la base de datos y la tabla llamada `world_cups`. Es ejecutado automáticamente por Docker al iniciar el contenedor de PostgreSQL para asegurar que la estructura esté correctamente configurada.

### 5. end2end.sh

El script `end2end.sh` automatiza el proceso de construcción de imágenes Docker, luego su ejecución en formato de Docker Contenedores, creación de tablas, carga de datos, y ejecución de preguntas de negocio. Este script verifica si las imágenes Docker están construidas, levanta el contenedor de PostgreSQL, espera a que esté listo, ejecuta el script SQL para crear la tabla, carga los datos desde el CSV utilizando `populate_db.py`, y finalmente ejecuta las consultas de reporte con `reporte.py`.

## Ejecución
- Ejecutar en bash el archivo `end2end.sh` que se encuentra en el branch ejercicio-6.


