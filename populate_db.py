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

# Cargar datos en la base de datos
def load_data(engine, data_url, table_name='world_cups'):
    df = pd.read_csv(data_url)
    
    # Deshabilitar restricciones antes de la carga
    with engine.connect() as conn:
        set_constraints(conn, enable=False)
        
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

    wait_for_postgres(user, password, db, host, port)

    try:
        engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
        
        # Cargar datos en la tabla 'world_cups'
        print("Cargando datos en la tabla 'world_cups'...")
        load_data(engine, data_url)
        
    except OperationalError as e:
        print(f"Error de conexión: {e}")

if __name__ == "__main__":
    main()
