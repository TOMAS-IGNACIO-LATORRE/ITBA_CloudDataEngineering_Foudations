import warnings
import psycopg2
import pandas as pd
from psycopg2 import OperationalError
warnings.filterwarnings("ignore")


# Función para ejecutar una consulta y devolver el resultado como un DataFrame
def run_query(conn, query):
    return pd.read_sql_query(query, conn)

def main():
    user = "admin"
    password = "admin_password"
    db = "world_cup_data"
    host = "db"
    port = "5432"

    queries = {
        "Top 5 de los países con mayores copas del mundo ganadas": 
            'SELECT Winner AS Country, COUNT(*) AS Total_Wins FROM world_cups GROUP BY Winner ORDER BY Total_Wins DESC LIMIT 5',
        
        "Sedes con mayor cantidad de espectadores en el siglo 1900 y en el siglo 2000": 
            '''
            SELECT '1990s' as Siglo, Country AS Host_Country, Year, Attendance
            FROM world_cups
            WHERE CAST(Year AS TEXT) LIKE '1%'
            
            UNION ALL
            
            SELECT '2000s' as Siglo, Country AS Host_Country, Year, Attendance
            FROM world_cups
            WHERE CAST(Year AS TEXT) LIKE '2%'
            
            ORDER BY Attendance DESC
            LIMIT 2
            ''',
        
        "Países con mayor cantidad de subcampeonatos": 
            '''
            SELECT Runners_Up AS Country, COUNT(*) AS most_runner_up_finished
            FROM world_cups 
            GROUP BY Runners_Up 
            ORDER BY most_runner_up_finished DESC 
            LIMIT 5
            ''',
        
        "Cantidad de equipos que hubo en los diferentes torneos, las veces que se repitió, y el último año que ocurrió esa cantidad": 
            '''
            SELECT QualifiedTeams AS QualifiedTeams, COUNT(*) AS Repetitions, MAX(Year) AS Ultimo_año
            FROM world_cups
            GROUP BY QualifiedTeams 
            ORDER BY QualifiedTeams DESC
            ''',
        
        "Años en que no se disputó la copa del mundo": 
            '''
            WITH RECURSIVE Years (Year) AS (
                SELECT MIN(Year) AS Year
                FROM world_cups
                UNION ALL
                SELECT Year + 4
                FROM Years
                WHERE Year + 4 <= 2024
            )
            SELECT Year
            FROM Years
            WHERE NOT EXISTS (
                SELECT 1
                FROM world_cups c
                WHERE c.Year = Years.Year
            )
            ORDER BY Year
            '''
    }

    try:
        conn = psycopg2.connect(dbname=db, user=user, password=password, host=host, port=port)
        
        for title, query in queries.items():
            print(f"\n{title}:")
            df = run_query(conn, query)
            print(df.to_string(index=False))
        
    except OperationalError as e:
        print(f"Error de conexión: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            print("Conexión cerrada.")

if __name__ == "__main__":
    main()
