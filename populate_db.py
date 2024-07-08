import time
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from psycopg2 import OperationalError

# Esperar a que PostgreSQL esté listo
def wait_for_postgres(user, password, db, host, port):
    while True:
        try:
            conn = psycopg2.connect(
                dbname=db, user=user, password=password, host=host, port=port
            )
            conn.close()
            print("PostgreSQL está listo.")
            break
        except OperationalError as e:
            print(f"Error de conexión: {e}")
            print("Esperando a que PostgreSQL esté listo...")
            time.sleep(2)

# Deshabilitar constraints
def set_constraints(conn, enable=False):
    action = 'ENABLE' if enable else 'DISABLE'
    with conn.cursor() as cursor:
        cursor.execute(f"ALTER TABLE world_cups {action} TRIGGER ALL;")
    conn.commit()

# Verificar si la tabla existe
def table_exists(conn, table_name):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1
                FROM   information_schema.tables 
                WHERE  table_name = %s
            );
        """, (table_name,))
        return cursor.fetchone()[0]

# Eliminar tabla si existe
def drop_table_if_exists(conn, table_name):
    if table_exists(conn, table_name):
        with conn.cursor() as cursor:
            cursor.execute(f"DROP TABLE {table_name};")
        conn.commit()
        print(f"Tabla '{table_name}' eliminada.")

# Cargar datos en la base de datos
def load_data(engine, data_url, table_name):
    df = pd.read_csv(data_url)
    
    # Deshabilitar restricciones antes de la carga
    with engine.connect() as conn:
        set_constraints(conn, enable=False)
        
        # Verificar y eliminar tabla si existe
        drop_table_if_exists(conn, table_name)
        
        # Cargar datos
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"Datos cargados en la tabla '{table_name}' exitosamente.")
        
        # Habilitar restricciones después de la carga
        set_constraints(conn, enable=True)

def main():
    user = "admin"
    password = "admin_password"
    db = "world_cup_data"
    host = "db"
    port = "5432"
    data_url = "WorldCups.csv"
    table_name = "world_cups"

    wait_for_postgres(user, password, db, host, port)

    try:
        engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
        
        # Cargar datos en la tabla especificada
        print(f"Cargando datos en la tabla '{table_name}'...")
        load_data(engine, data_url, table_name)
        
    except OperationalError as e:
        print(f"Error de conexión: {e}")

if __name__ == "__main__":
    main()
