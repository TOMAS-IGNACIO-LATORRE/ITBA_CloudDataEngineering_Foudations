-- Eliminar la tabla si existe
DROP TABLE IF EXISTS world_cups;

-- Crear la tabla
CREATE TABLE world_cups (
    id SERIAL PRIMARY KEY,
    year INTEGER,
    country TEXT,
    winner TEXT,
    runners_up TEXT,
    third TEXT,
    fourth TEXT,
    goals_scored INTEGER,
    qualified_teams INTEGER,
    matches_played INTEGER,
    attendance INTEGER
);
