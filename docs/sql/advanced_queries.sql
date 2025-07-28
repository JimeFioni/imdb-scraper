-- ===============================================
-- CONSULTAS SQL AVANZADAS - ANÁLISIS IMDB SCRAPER
-- PostgreSQL - Análisis completo del Top 250
-- ===============================================

-- ===============================================
-- 1. TOP 5 DÉCADAS CON MAYOR PROMEDIO DE DURACIÓN
-- ===============================================

WITH peliculas_por_decada AS (
    SELECT 
        p.*,
        (p.anio / 10 * 10) AS decada,
        d.nombre AS nombre_decada
    FROM peliculas p
    LEFT JOIN decadas d ON (p.anio / 10 * 10) = d.decada
    WHERE p.duracion_minutos IS NOT NULL
),
estadisticas_decada AS (
    SELECT 
        decada,
        nombre_decada,
        AVG(duracion_minutos) AS promedio_duracion,
        COUNT(*) AS total_peliculas,
        STDDEV(duracion_minutos) AS desviacion_duracion,
        MIN(duracion_minutos) AS duracion_minima,
        MAX(duracion_minutos) AS duracion_maxima,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY duracion_minutos) AS mediana_duracion
    FROM peliculas_por_decada
    GROUP BY decada, nombre_decada
    HAVING COUNT(*) >= 2  -- Al menos 2 películas por década
),
ranking_decadas AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (ORDER BY promedio_duracion DESC) AS ranking
    FROM estadisticas_decada
)
SELECT 
    ranking,
    COALESCE(nombre_decada, decada::text || 's') AS periodo,
    ROUND(promedio_duracion, 1) AS promedio_duracion_minutos,
    ROUND(promedio_duracion / 60.0, 1) AS promedio_duracion_horas,
    total_peliculas,
    ROUND(desviacion_duracion, 1) AS desviacion_std,
    duracion_minima || ' min' AS pelicula_mas_corta,
    duracion_maxima || ' min' AS pelicula_mas_larga,
    ROUND(mediana_duracion, 0) || ' min' AS mediana
FROM ranking_decadas
WHERE ranking <= 5
ORDER BY promedio_duracion DESC;

-- ===============================================
-- 2. DESVIACIÓN ESTÁNDAR DE CALIFICACIONES POR AÑO
-- ===============================================

WITH stats_por_anio AS (
    SELECT 
        anio,
        COUNT(*) AS total_peliculas,
        AVG(calificacion) AS promedio_calificacion,
        STDDEV(calificacion) AS desviacion_std,
        MIN(calificacion) AS calificacion_minima,
        MAX(calificacion) AS calificacion_maxima,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY calificacion) AS mediana
    FROM peliculas
    WHERE calificacion IS NOT NULL AND anio IS NOT NULL
    GROUP BY anio
    HAVING COUNT(*) >= 1
)
SELECT 
    anio,
    total_peliculas,
    ROUND(promedio_calificacion, 2) AS promedio,
    ROUND(desviacion_std, 3) AS desviacion_estandar,
    ROUND(mediana, 1) AS mediana,
    calificacion_minima AS min_calif,
    calificacion_maxima AS max_calif,
    -- Clasificación de variabilidad
    CASE 
        WHEN desviacion_std < 0.2 THEN 'Baja variabilidad'
        WHEN desviacion_std < 0.5 THEN 'Variabilidad media'
        ELSE 'Alta variabilidad'
    END AS clasificacion_variabilidad
FROM stats_por_anio
ORDER BY anio DESC;

-- ===============================================
-- 3. ANÁLISIS COMPARATIVO IMDB VS METASCORE
-- ===============================================

WITH comparacion_ratings AS (
    SELECT 
        titulo,
        anio,
        calificacion AS imdb_rating,
        metascore,
        ROUND(metascore::NUMERIC / 10.0, 1) AS metascore_normalizado, -- Escala 0-10
        ROUND(calificacion - (metascore::NUMERIC / 10.0), 1) AS diferencia,
        ABS(calificacion - (metascore::NUMERIC / 10.0)) AS diferencia_absoluta,
        ranking,
        (anio / 10 * 10) AS decada
    FROM peliculas 
    WHERE calificacion IS NOT NULL 
      AND metascore IS NOT NULL 
      AND metascore > 0
),
clasificacion_diferencias AS (
    SELECT 
        *,
        CASE 
            WHEN diferencia_absoluta <= 0.5 THEN 'Muy Coherente'
            WHEN diferencia_absoluta <= 1.0 THEN 'Coherente'
            WHEN diferencia_absoluta <= 1.5 THEN 'Poco Coherente'
            ELSE 'Muy Divergente'
        END AS coherencia,
        CASE 
            WHEN diferencia > 1.0 THEN 'IMDb Favorece'
            WHEN diferencia < -1.0 THEN 'Metascore Favorece'
            ELSE 'Equilibrado'
        END AS tendencia
    FROM comparacion_ratings
),
estadisticas_generales AS (
    SELECT 
        COUNT(*) AS total_peliculas,
        ROUND(AVG(imdb_rating), 2) AS promedio_imdb,
        ROUND(AVG(metascore_normalizado), 2) AS promedio_metascore,
        ROUND(AVG(diferencia), 2) AS diferencia_promedio,
        ROUND(STDDEV(diferencia), 3) AS desviacion_diferencia,
        ROUND(
            (COUNT(*) FILTER (WHERE coherencia IN ('Muy Coherente', 'Coherente'))::NUMERIC / COUNT(*)) * 100, 
            1
        ) AS porcentaje_coherencia
    FROM clasificacion_diferencias
)
-- Resultados principales
SELECT 
    'ESTADÍSTICAS GENERALES' AS seccion,
    'Total: ' || total_peliculas || ' películas' AS detalle,
    'Promedio IMDb: ' || promedio_imdb AS imdb_info,
    'Promedio Metascore: ' || promedio_metascore AS metascore_info,
    'Diferencia promedio: ' || diferencia_promedio AS diferencia_info,
    'Coherencia: ' || porcentaje_coherencia || '%' AS coherencia_info
FROM estadisticas_generales

UNION ALL

-- Top 5 películas más divergentes (IMDb >> Metascore)
SELECT 
    'TOP 5 - IMDB FAVORECE',
    titulo || ' (' || anio || ')',
    'IMDb: ' || imdb_rating,
    'Meta: ' || metascore_normalizado,
    'Dif: +' || diferencia,
    'Ranking: #' || ranking
FROM clasificacion_diferencias
WHERE diferencia > 0
ORDER BY diferencia DESC
LIMIT 5;

-- ===============================================
-- 4. VISTA: PELÍCULAS Y ACTORES CON FILTRO POR ACTOR PRINCIPAL
-- ===============================================

CREATE OR REPLACE VIEW vista_peliculas_actores AS
WITH actores_principales AS (
    SELECT 
        pelicula_id,
        STRING_AGG(nombre, ', ' ORDER BY posicion) AS todos_actores,
        MAX(CASE WHEN posicion = 1 THEN nombre END) AS actor_principal,
        MAX(CASE WHEN posicion = 2 THEN nombre END) AS segundo_actor,
        MAX(CASE WHEN posicion = 3 THEN nombre END) AS tercer_actor
    FROM actores
    GROUP BY pelicula_id
)
SELECT 
    p.id,
    p.titulo,
    p.anio,
    p.calificacion,
    p.duracion_texto,
    p.metascore,
    p.ranking,
    ap.actor_principal,
    ap.segundo_actor,
    ap.tercer_actor,
    ap.todos_actores,
    -- Análisis adicional
    (p.anio / 10 * 10) AS decada,
    CASE 
        WHEN p.calificacion >= 9.0 THEN 'Excelente'
        WHEN p.calificacion >= 8.5 THEN 'Muy buena'
        WHEN p.calificacion >= 8.0 THEN 'Buena'
        ELSE 'Regular'
    END AS categoria_calificacion
FROM peliculas p
LEFT JOIN actores_principales ap ON p.id = ap.pelicula_id
ORDER BY p.ranking;

-- Consulta de ejemplo usando la vista para filtrar por actor principal
/*
SELECT * FROM vista_peliculas_actores 
WHERE actor_principal ILIKE '%Tom Hanks%' 
OR actor_principal ILIKE '%Morgan Freeman%'
ORDER BY calificacion DESC;
*/

-- ===============================================
-- 5. ÍNDICES Y PARTICIONES PARA CONSULTAS FRECUENTES
-- ===============================================

-- Índice compuesto para búsquedas por década y calificación
CREATE INDEX IF NOT EXISTS idx_peliculas_decada_calificacion 
ON peliculas ((anio / 10 * 10), calificacion DESC);

-- Índice parcial para películas con alta calificación (>= 8.5)
CREATE INDEX IF NOT EXISTS idx_peliculas_alta_calificacion 
ON peliculas (ranking, calificacion) 
WHERE calificacion >= 8.5;

-- Índice funcional para búsquedas de diferencia IMDb vs Metascore
CREATE INDEX IF NOT EXISTS idx_diferencia_imdb_metascore 
ON peliculas (ABS((calificacion * 10) - metascore)) 
WHERE calificacion IS NOT NULL AND metascore IS NOT NULL;

-- ===============================================
-- FUNCIONES DE VENTANA (OVER/PARTITION BY)
-- ===============================================

-- Análisis con funciones de ventana
CREATE OR REPLACE VIEW analisis_ventanas AS
SELECT 
    p.titulo,
    p.anio,
    p.calificacion,
    p.metascore,
    p.duracion_minutos,
    
    -- Ranking dentro de cada década
    ROW_NUMBER() OVER (
        PARTITION BY (p.anio / 10 * 10) 
        ORDER BY p.calificacion DESC
    ) AS ranking_en_decada,
    
    -- Percentil de calificación por década
    PERCENT_RANK() OVER (
        PARTITION BY (p.anio / 10 * 10) 
        ORDER BY p.calificacion
    ) AS percentil_calificacion_decada,
    
    -- Media móvil de calificaciones por año (ventana de 3 años)
    AVG(p.calificacion) OVER (
        ORDER BY p.anio 
        ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
    ) AS media_movil_3_anios,
    
    -- Diferencia con la película anterior en ranking
    LAG(p.calificacion) OVER (ORDER BY p.ranking) AS calificacion_anterior,
    p.calificacion - LAG(p.calificacion) OVER (ORDER BY p.ranking) AS diferencia_con_anterior,
    
    -- Posición relativa en el top general
    NTILE(10) OVER (ORDER BY p.calificacion DESC) AS decil_calificacion
    
FROM peliculas p
WHERE p.calificacion IS NOT NULL
ORDER BY p.ranking;

-- ===============================================
-- PROCEDIMIENTOS ALMACENADOS PARA CARGA INCREMENTAL
-- ===============================================

-- Función para análisis estadístico completo
CREATE OR REPLACE FUNCTION analisis_estadistico_completo()
RETURNS TABLE (
    metrica VARCHAR,
    valor NUMERIC,
    descripcion TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        'total_peliculas'::VARCHAR,
        COUNT(*)::NUMERIC,
        'Número total de películas en la base de datos'::TEXT
    FROM peliculas
    
    UNION ALL
    
    SELECT 
        'promedio_calificacion'::VARCHAR,
        ROUND(AVG(calificacion), 2)::NUMERIC,
        'Calificación promedio de todas las películas'::TEXT
    FROM peliculas WHERE calificacion IS NOT NULL
    
    UNION ALL
    
    SELECT 
        'peliculas_con_metascore'::VARCHAR,
        COUNT(*)::NUMERIC,
        'Películas que tienen metascore disponible'::TEXT
    FROM peliculas WHERE metascore IS NOT NULL
    
    UNION ALL
    
    SELECT 
        'decada_mas_representada'::VARCHAR,
        (anio / 10 * 10)::NUMERIC,
        'Década con más películas en el top'::TEXT
    FROM peliculas
    WHERE anio IS NOT NULL
    GROUP BY (anio / 10 * 10)
    ORDER BY COUNT(*) DESC
    LIMIT 1;
END;
$$ LANGUAGE plpgsql;

-- Función para carga incremental de películas
CREATE OR REPLACE FUNCTION cargar_pelicula_incremental(
    p_titulo VARCHAR,
    p_anio INTEGER,
    p_calificacion DECIMAL,
    p_duracion_minutos INTEGER,
    p_metascore INTEGER,
    p_ranking INTEGER
) RETURNS INTEGER AS $$
DECLARE
    pelicula_id INTEGER;
BEGIN
    -- Insertar o actualizar película
    INSERT INTO peliculas (titulo, anio, calificacion, duracion_minutos, metascore, ranking)
    VALUES (p_titulo, p_anio, p_calificacion, p_duracion_minutos, p_metascore, p_ranking)
    ON CONFLICT (titulo, anio)
    DO UPDATE SET 
        calificacion = EXCLUDED.calificacion,
        duracion_minutos = EXCLUDED.duracion_minutos,
        metascore = EXCLUDED.metascore,
        ranking = EXCLUDED.ranking,
        fecha_actualizacion = CURRENT_TIMESTAMP
    RETURNING id INTO pelicula_id;
    
    RETURN pelicula_id;
END;
$$ LANGUAGE plpgsql;

-- ===============================================
-- COMENTARIOS SOBRE OPTIMIZACIÓN
-- ===============================================

/*
JUSTIFICACIÓN DE ÍNDICES Y PARTICIONES:

1. idx_peliculas_decada_calificacion: 
   - Para consultas frecuentes por década y ordenamiento por calificación
   - Optimiza la consulta #1 de promedios por década

2. idx_peliculas_alta_calificacion:
   - Índice parcial para el subset de películas más relevantes
   - Mejora consultas de top películas

3. idx_diferencia_imdb_metascore:
   - Optimiza la consulta #3 de diferencias entre ratings
   - Índice funcional para cálculos complejos

4. Funciones de ventana:
   - Proporcionan análisis estadístico avanzado
   - Rankings, percentiles, medias móviles sin subconsultas

5. Procedimientos almacenados:
   - Encapsulan lógica de negocio
   - Facilitan mantenimiento y carga incremental
*/

-- ===============================================
-- 4. ANÁLISIS DE VENTANAS DESLIZANTES (WINDOW FUNCTIONS)
-- ===============================================

WITH ventanas_analisis AS (
    SELECT 
        titulo,
        anio,
        calificacion,
        ranking,
        duracion_minutos,
        
        -- Ventanas de tiempo
        LAG(calificacion, 1) OVER (ORDER BY anio, ranking) AS calificacion_anterior,
        LEAD(calificacion, 1) OVER (ORDER BY anio, ranking) AS calificacion_siguiente,
        
        -- Promedios móviles
        AVG(calificacion) OVER (
            ORDER BY anio 
            ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING
        ) AS promedio_movil_5,
        
        -- Rankings por década
        ROW_NUMBER() OVER (
            PARTITION BY (anio / 10 * 10) 
            ORDER BY calificacion DESC, ranking ASC
        ) AS ranking_decada,
        
        -- Percentiles
        PERCENT_RANK() OVER (ORDER BY calificacion) AS percentil_calificacion,
        NTILE(4) OVER (ORDER BY calificacion DESC) AS cuartil_calificacion,
        
        -- Densidad temporal
        COUNT(*) OVER (
            PARTITION BY (anio / 10 * 10)
        ) AS peliculas_por_decada
    FROM peliculas
    WHERE calificacion IS NOT NULL
),
tendencias AS (
    SELECT 
        *,
        CASE 
            WHEN calificacion > promedio_movil_5 THEN 'Sobre Promedio'
            WHEN calificacion < promedio_movil_5 THEN 'Bajo Promedio'
            ELSE 'En Promedio'
        END AS tendencia_temporal,
        
        CASE 
            WHEN percentil_calificacion >= 0.9 THEN 'Elite (Top 10%)'
            WHEN percentil_calificacion >= 0.75 THEN 'Excelente (Top 25%)'
            WHEN percentil_calificacion >= 0.5 THEN 'Buena (Top 50%)'
            ELSE 'Regular'
        END AS categoria_calidad
    FROM ventanas_analisis
)
SELECT 
    titulo,
    anio,
    calificacion,
    ROUND(promedio_movil_5, 2) AS promedio_movil,
    ranking_decada || '/' || peliculas_por_decada AS posicion_decada,
    categoria_calidad,
    tendencia_temporal
FROM tendencias
ORDER BY anio DESC, calificacion DESC
LIMIT 20;

-- ===============================================
-- 5. ANÁLISIS DE ACTORES PRINCIPALES MÁS FRECUENTES
-- ===============================================

WITH actores_frecuencia AS (
    SELECT 
        a.nombre,
        COUNT(*) AS apariciones,
        STRING_AGG(p.titulo, ', ' ORDER BY p.calificacion DESC) AS peliculas,
        AVG(p.calificacion) AS promedio_calificacion,
        MIN(p.anio) AS primera_aparicion,
        MAX(p.anio) AS ultima_aparicion,
        STRING_AGG(DISTINCT (p.anio / 10 * 10)::text, ', ') AS decadas_activas
    FROM actores a
    JOIN peliculas p ON a.pelicula_id = p.id
    WHERE p.calificacion IS NOT NULL
    GROUP BY a.nombre
    HAVING COUNT(*) >= 2  -- Al menos 2 apariciones
),
ranking_actores AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (ORDER BY apariciones DESC, promedio_calificacion DESC) AS ranking,
        ultima_aparicion - primera_aparicion AS anos_carrera
    FROM actores_frecuencia
)
SELECT 
    ranking,
    nombre,
    apariciones || ' películas' AS total_apariciones,
    ROUND(promedio_calificacion, 1) AS calificacion_promedio,
    primera_aparicion || '-' || ultima_aparicion AS periodo_activo,
    anos_carrera || ' años de carrera' AS duracion_carrera,
    decadas_activas AS decadas,
    CASE 
        WHEN LENGTH(peliculas) > 100 THEN LEFT(peliculas, 97) || '...'
        ELSE peliculas
    END AS principales_peliculas
FROM ranking_actores
WHERE ranking <= 15
ORDER BY apariciones DESC, promedio_calificacion DESC;

-- ===============================================
-- 6. DISTRIBUCIÓN TEMPORAL Y ANÁLISIS DE EVOLUCIÓN
-- ===============================================

WITH evolucion_temporal AS (
    SELECT 
        anio,
        COUNT(*) AS peliculas_por_ano,
        AVG(calificacion) AS promedio_calificacion,
        AVG(duracion_minutos) AS promedio_duracion,
        AVG(CASE WHEN metascore > 0 THEN metascore END) AS promedio_metascore,
        
        -- Acumulados
        SUM(COUNT(*)) OVER (ORDER BY anio) AS peliculas_acumuladas,
        
        -- Comparación con año anterior
        LAG(AVG(calificacion), 1) OVER (ORDER BY anio) AS calificacion_ano_anterior
    FROM peliculas 
    WHERE calificacion IS NOT NULL AND anio IS NOT NULL
    GROUP BY anio
),
tendencias_anuales AS (
    SELECT 
        *,
        ROUND(promedio_calificacion - calificacion_ano_anterior, 2) AS cambio_calificacion,
        CASE 
            WHEN promedio_calificacion > calificacion_ano_anterior THEN '↗ Mejora'
            WHEN promedio_calificacion < calificacion_ano_anterior THEN '↘ Declive'
            ELSE '→ Estable'
        END AS tendencia_calidad
    FROM evolucion_temporal
)
SELECT 
    anio,
    peliculas_por_ano,
    ROUND(promedio_calificacion, 2) AS calificacion_avg,
    ROUND(promedio_duracion, 0) || ' min' AS duracion_avg,
    COALESCE(ROUND(promedio_metascore, 0), 0) AS metascore_avg,
    COALESCE(cambio_calificacion, 0) AS cambio_vs_anterior,
    COALESCE(tendencia_calidad, '→ Inicial') AS tendencia
FROM tendencias_anuales
WHERE anio >= 1990  -- Últimas 3 décadas
ORDER BY anio DESC;
