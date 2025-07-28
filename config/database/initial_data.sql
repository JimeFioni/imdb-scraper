-- ===============================================
-- DATOS INICIALES PARA EL MODELO RELACIONAL
-- ===============================================

-- Insertar géneros comunes del cine
INSERT INTO generos (nombre, descripcion) VALUES
('Action', 'Películas de acción con secuencias dinámicas'),
('Adventure', 'Películas de aventuras y exploración'),
('Animation', 'Películas animadas y de dibujos'),
('Biography', 'Películas biográficas de personajes reales'),
('Comedy', 'Películas de comedia y humor'),
('Crime', 'Películas de crímenes y thriller policial'),
('Documentary', 'Documentales y no ficción'),
('Drama', 'Películas dramáticas'),
('Family', 'Películas familiares para todas las edades'),
('Fantasy', 'Películas de fantasía y mundos imaginarios'),
('Horror', 'Películas de terror y suspense'),
('Musical', 'Películas musicales'),
('Mystery', 'Películas de misterio e intriga'),
('Romance', 'Películas románticas'),
('Sci-Fi', 'Ciencia ficción y futurismo'),
('Sport', 'Películas deportivas'),
('Thriller', 'Películas de suspense y tensión'),
('War', 'Películas bélicas y de guerra'),
('Western', 'Películas del oeste americano'),
('History', 'Películas históricas')
ON CONFLICT (nombre) DO NOTHING;

-- ===============================================
-- PROCEDIMIENTOS ALMACENADOS PARA ANÁLISIS
-- ===============================================

-- Función para obtener estadísticas de una película
CREATE OR REPLACE FUNCTION get_pelicula_stats(p_pelicula_id INTEGER)
RETURNS TABLE(
    titulo VARCHAR,
    anio INTEGER,
    calificacion DECIMAL,
    ranking_general INTEGER,
    ranking_en_decada BIGINT,
    total_peliculas_decada BIGINT,
    actores_principales TEXT
) AS $$
BEGIN
    RETURN QUERY
    WITH pelicula_info AS (
        SELECT p.*, (p.anio / 10 * 10) AS decada
        FROM peliculas p
        WHERE p.id = p_pelicula_id
    ),
    ranking_decada AS (
        SELECT 
            pi.id,
            ROW_NUMBER() OVER (
                PARTITION BY (pi.anio / 10 * 10) 
                ORDER BY pi.calificacion DESC, pi.ranking ASC
            ) AS rank_decada,
            COUNT(*) OVER (PARTITION BY (pi.anio / 10 * 10)) AS total_decada
        FROM peliculas pi
        JOIN pelicula_info pinfo ON (pi.anio / 10 * 10) = pinfo.decada
    ),
    actores_concat AS (
        SELECT 
            a.pelicula_id,
            STRING_AGG(a.nombre, ', ' ORDER BY a.posicion) AS actores_lista
        FROM actores a
        WHERE a.pelicula_id = p_pelicula_id
        GROUP BY a.pelicula_id
    )
    SELECT 
        pi.titulo,
        pi.anio,
        pi.calificacion,
        pi.ranking,
        rd.rank_decada,
        rd.total_decada,
        COALESCE(ac.actores_lista, 'Sin actores registrados')
    FROM pelicula_info pi
    LEFT JOIN ranking_decada rd ON pi.id = rd.id
    LEFT JOIN actores_concat ac ON pi.id = ac.pelicula_id;
END;
$$ LANGUAGE plpgsql;

-- Función para análisis comparativo entre IMDb y Metascore
CREATE OR REPLACE FUNCTION analyze_rating_correlation()
RETURNS TABLE(
    total_peliculas BIGINT,
    promedio_imdb NUMERIC,
    promedio_metascore NUMERIC,
    correlacion_estimada TEXT,
    diferencia_promedio NUMERIC
) AS $$
DECLARE
    total_count BIGINT;
    avg_imdb NUMERIC;
    avg_meta NUMERIC;
    diff_avg NUMERIC;
BEGIN
    SELECT 
        COUNT(*),
        AVG(calificacion),
        AVG(metascore::NUMERIC / 10.0)  -- Convertir metascore a escala 0-10
    INTO total_count, avg_imdb, avg_meta
    FROM peliculas 
    WHERE calificacion IS NOT NULL AND metascore IS NOT NULL;
    
    diff_avg := avg_imdb - avg_meta;
    
    RETURN QUERY
    SELECT 
        total_count,
        ROUND(avg_imdb, 2),
        ROUND(avg_meta, 2),
        CASE 
            WHEN ABS(diff_avg) < 0.5 THEN 'Correlación Alta'
            WHEN ABS(diff_avg) < 1.0 THEN 'Correlación Media'
            ELSE 'Correlación Baja'
        END,
        ROUND(diff_avg, 2);
END;
$$ LANGUAGE plpgsql;

-- ===============================================
-- VISTAS MATERIALIZADAS PARA CONSULTAS RÁPIDAS
-- ===============================================

-- Vista materializada: Películas con actores principales
CREATE MATERIALIZED VIEW IF NOT EXISTS view_peliculas_actores AS
SELECT 
    p.id,
    p.titulo,
    p.anio,
    p.calificacion,
    p.metascore,
    p.duracion_minutos,
    p.ranking,
    (p.anio / 10 * 10) AS decada,
    d.nombre AS nombre_decada,
    STRING_AGG(a.nombre, ', ' ORDER BY a.posicion) AS actores_principales,
    COUNT(a.id) AS total_actores
FROM peliculas p
LEFT JOIN decadas d ON (p.anio / 10 * 10) = d.decada
LEFT JOIN actores a ON p.id = a.pelicula_id
GROUP BY p.id, p.titulo, p.anio, p.calificacion, p.metascore, 
         p.duracion_minutos, p.ranking, d.nombre
ORDER BY p.ranking;

-- Índices para la vista materializada
CREATE INDEX IF NOT EXISTS idx_view_peliculas_actores_decada ON view_peliculas_actores(decada);
CREATE INDEX IF NOT EXISTS idx_view_peliculas_actores_calificacion ON view_peliculas_actores(calificacion DESC);

-- ===============================================
-- FUNCIÓN PARA REFRESCAR VISTAS MATERIALIZADAS
-- ===============================================

CREATE OR REPLACE FUNCTION refresh_materialized_views()
RETURNS TEXT AS $$
BEGIN
    REFRESH MATERIALIZED VIEW view_peliculas_actores;
    RETURN 'Vistas materializadas actualizadas correctamente';
END;
$$ LANGUAGE plpgsql;
