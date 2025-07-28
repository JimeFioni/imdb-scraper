# 📊 Análisis SQL Avanzado - IMDb Scraper

Este documento detalla las **consultas SQL avanzadas** implementadas para el análisis de datos del scraper de IMDb.

## 🗄️ Modelo Relacional

### Diagrama de Entidad-Relación
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    PELICULAS    │    │     ACTORES     │    │    DECADAS      │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ id (PK)         │◄──┐│ id (PK)         │    │ id (PK)         │
│ titulo          │   └│ pelicula_id(FK) │    │ decada          │
│ anio            │    │ nombre          │    │ nombre          │
│ calificacion    │    │ posicion        │    │ descripcion     │
│ duracion_minutos│    └─────────────────┘    └─────────────────┘
│ metascore       │
│ ranking         │    ┌─────────────────┐
│ fecha_scraping  │    │ PELICULA_GENEROS│
└─────────────────┘    ├─────────────────┤
                       │ pelicula_id(FK) │
┌─────────────────┐    │ genero_id(FK)   │
│    GENEROS      │    └─────────────────┘
├─────────────────┤           │
│ id (PK)         │◄──────────┘
│ nombre          │
│ descripcion     │
└─────────────────┘
```

## 🔍 Consultas SQL Avanzadas Implementadas

### 1. 📅 Análisis Temporal por Décadas

**Objetivo**: Obtener las 5 décadas con mayor promedio de duración de películas.

```sql
WITH peliculas_por_decada AS (
    SELECT 
        (anio / 10 * 10) AS decada,
        AVG(duracion_minutos) AS promedio_duracion,
        COUNT(*) AS total_peliculas,
        STDDEV(duracion_minutos) AS desviacion_duracion
    FROM peliculas 
    WHERE duracion_minutos IS NOT NULL
    GROUP BY (anio / 10 * 10)
    HAVING COUNT(*) >= 2
)
SELECT 
    ranking,
    decada || 's' AS periodo,
    ROUND(promedio_duracion, 1) AS promedio_duracion_minutos,
    total_peliculas,
    ROUND(desviacion_duracion, 1) AS desviacion_std
FROM (
    SELECT *, ROW_NUMBER() OVER (ORDER BY promedio_duracion DESC) AS ranking
    FROM peliculas_por_decada
) ranking_decadas
WHERE ranking <= 5;
```

**Técnicas utilizadas:**
- ✅ **CTE (Common Table Expressions)** para estructurar la consulta
- ✅ **Window Functions** con `ROW_NUMBER()`
- ✅ **Funciones Agregadas** (`AVG`, `COUNT`, `STDDEV`)
- ✅ **Cálculo de décadas** con aritmética de enteros

### 2. 📈 Desviación Estándar de Calificaciones

**Objetivo**: Calcular variabilidad de calificaciones por año.

```sql
WITH stats_por_anio AS (
    SELECT 
        anio,
        COUNT(*) AS total_peliculas,
        AVG(calificacion) AS promedio_calificacion,
        STDDEV(calificacion) AS desviacion_std,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY calificacion) AS mediana
    FROM peliculas
    WHERE calificacion IS NOT NULL AND anio IS NOT NULL
    GROUP BY anio
)
SELECT 
    anio,
    ROUND(promedio_calificacion, 2) AS promedio,
    ROUND(desviacion_std, 3) AS desviacion_estandar,
    CASE 
        WHEN desviacion_std < 0.2 THEN 'Baja variabilidad'
        WHEN desviacion_std < 0.5 THEN 'Variabilidad media'
        ELSE 'Alta variabilidad'
    END AS clasificacion_variabilidad
FROM stats_por_anio
ORDER BY anio DESC;
```

**Técnicas utilizadas:**
- ✅ **Función PERCENTILE_CONT** para calcular mediana
- ✅ **CASE WHEN** para clasificación automática
- ✅ **Funciones estadísticas** avanzadas

### 3. 🔍 Análisis Comparativo IMDb vs Metascore

**Objetivo**: Detectar películas con más del 20% de diferencia entre calificaciones.

```sql
WITH comparacion_ratings AS (
    SELECT 
        titulo,
        anio,
        calificacion AS imdb_rating,
        ROUND(metascore::NUMERIC / 10.0, 1) AS metascore_normalizado,
        ROUND(calificacion - (metascore::NUMERIC / 10.0), 1) AS diferencia,
        ABS(calificacion - (metascore::NUMERIC / 10.0)) AS diferencia_absoluta
    FROM peliculas 
    WHERE calificacion IS NOT NULL AND metascore IS NOT NULL AND metascore > 0
),
clasificacion_diferencias AS (
    SELECT 
        *,
        CASE 
            WHEN diferencia_absoluta > 2.0 THEN 'Muy Divergente (20%+)'
            WHEN diferencia_absoluta > 1.0 THEN 'Divergente'
            ELSE 'Coherente'
        END AS nivel_coherencia,
        CASE 
            WHEN diferencia > 1.0 THEN 'IMDb Favorece'
            WHEN diferencia < -1.0 THEN 'Metascore Favorece'
            ELSE 'Equilibrado'
        END AS tendencia
    FROM comparacion_ratings
)
SELECT * FROM clasificacion_diferencias
WHERE nivel_coherencia LIKE '%Divergente%'
ORDER BY diferencia_absoluta DESC;
```

**Técnicas utilizadas:**
- ✅ **Normalización de escalas** (Metascore 0-100 → 0-10)
- ✅ **Cálculo de diferencias absolutas**
- ✅ **Clasificación automática** de coherencia
- ✅ **Filtrado por umbrales** de diferencia

### 4. 🎭 Vista Películas-Actores con Filtros

**Objetivo**: Crear vista optimizada para búsquedas por actor principal.

```sql
-- Vista materializada para optimización
CREATE MATERIALIZED VIEW view_peliculas_actores AS
SELECT 
    p.id,
    p.titulo,
    p.anio,
    p.calificacion,
    p.ranking,
    STRING_AGG(a.nombre, ', ' ORDER BY a.posicion) AS actores_principales,
    (SELECT a2.nombre FROM actores a2 WHERE a2.pelicula_id = p.id AND a2.posicion = 1) AS actor_principal
FROM peliculas p
LEFT JOIN actores a ON p.id = a.pelicula_id
GROUP BY p.id, p.titulo, p.anio, p.calificacion, p.ranking
ORDER BY p.ranking;

-- Consulta con filtro por actor principal
SELECT * FROM view_peliculas_actores 
WHERE actor_principal ILIKE '%morgan freeman%'
ORDER BY calificacion DESC;
```

**Técnicas utilizadas:**
- ✅ **Vistas Materializadas** para optimización
- ✅ **STRING_AGG** para concatenar actores
- ✅ **Subconsultas correlacionadas** para actor principal
- ✅ **Búsqueda insensible a mayúsculas** con `ILIKE`

### 5. 🚀 Window Functions Avanzadas

**Objetivo**: Análisis de tendencias y rankings dinámicos.

```sql
WITH ventanas_analisis AS (
    SELECT 
        titulo,
        anio,
        calificacion,
        ranking,
        
        -- Ranking por década
        ROW_NUMBER() OVER (
            PARTITION BY (anio / 10 * 10) 
            ORDER BY calificacion DESC
        ) AS ranking_decada,
        
        -- Promedio móvil de 5 películas
        AVG(calificacion) OVER (
            ORDER BY anio 
            ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING
        ) AS promedio_movil_5,
        
        -- Percentiles dinámicos
        PERCENT_RANK() OVER (ORDER BY calificacion) AS percentil_calificacion,
        NTILE(4) OVER (ORDER BY calificacion DESC) AS cuartil_calificacion,
        
        -- Comparación con película anterior/siguiente
        LAG(calificacion, 1) OVER (ORDER BY anio, ranking) AS calificacion_anterior,
        LEAD(calificacion, 1) OVER (ORDER BY anio, ranking) AS calificacion_siguiente
    FROM peliculas
    WHERE calificacion IS NOT NULL
)
SELECT 
    titulo,
    anio,
    calificacion,
    ranking_decada,
    ROUND(promedio_movil_5, 2) AS promedio_movil,
    CASE 
        WHEN percentil_calificacion >= 0.9 THEN 'Elite (Top 10%)'
        WHEN percentil_calificacion >= 0.75 THEN 'Excelente (Top 25%)'
        ELSE 'Buena'
    END AS categoria_calidad
FROM ventanas_analisis
ORDER BY anio DESC, calificacion DESC;
```

**Técnicas utilizadas:**
- ✅ **ROW_NUMBER() con PARTITION BY** para rankings por grupo
- ✅ **Promedios móviles** con `ROWS BETWEEN`
- ✅ **PERCENT_RANK()** para percentiles dinámicos
- ✅ **LAG/LEAD** para comparaciones temporales
- ✅ **NTILE()** para cuartiles automáticos

## 🗃️ Procedimientos Almacenados

### Función de Estadísticas de Película

```sql
CREATE OR REPLACE FUNCTION get_pelicula_stats(p_pelicula_id INTEGER)
RETURNS TABLE(
    titulo VARCHAR,
    ranking_general INTEGER,
    ranking_en_decada BIGINT,
    actores_principales TEXT
) AS $$
BEGIN
    RETURN QUERY
    WITH ranking_decada AS (
        SELECT 
            p.id,
            ROW_NUMBER() OVER (
                PARTITION BY (p.anio / 10 * 10) 
                ORDER BY p.calificacion DESC
            ) AS rank_decada
        FROM peliculas p
        WHERE p.id = p_pelicula_id
    )
    SELECT 
        p.titulo,
        p.ranking,
        rd.rank_decada,
        STRING_AGG(a.nombre, ', ' ORDER BY a.posicion) AS actores
    FROM peliculas p
    LEFT JOIN ranking_decada rd ON p.id = rd.id
    LEFT JOIN actores a ON p.id = a.pelicula_id
    WHERE p.id = p_pelicula_id
    GROUP BY p.id, p.titulo, p.ranking, rd.rank_decada;
END;
$$ LANGUAGE plpgsql;
```

### Función de Análisis de Correlación

```sql
CREATE OR REPLACE FUNCTION analyze_rating_correlation()
RETURNS TABLE(
    total_peliculas BIGINT,
    promedio_imdb NUMERIC,
    promedio_metascore NUMERIC,
    correlacion_estimada TEXT
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
        AVG(metascore::NUMERIC / 10.0)
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
        END;
END;
$$ LANGUAGE plpgsql;
```

## 📊 Índices para Optimización

```sql
-- Índices principales
CREATE INDEX idx_peliculas_anio ON peliculas(anio);
CREATE INDEX idx_peliculas_calificacion ON peliculas(calificacion DESC);
CREATE INDEX idx_peliculas_decada ON peliculas((anio / 10 * 10));

-- Índices compuestos
CREATE INDEX idx_peliculas_anio_calificacion ON peliculas(anio, calificacion DESC);

-- Índices de texto completo
CREATE INDEX idx_peliculas_titulo_gin ON peliculas USING gin(to_tsvector('spanish', titulo));
CREATE INDEX idx_actores_nombre_gin ON actores USING gin(to_tsvector('spanish', nombre));
```

## 🎯 Casos de Uso Prácticos

### 1. Encontrar la mejor película de cada década
```sql
SELECT DISTINCT ON (decada)
    decada || 's' AS periodo,
    titulo,
    calificacion
FROM view_peliculas_actores
ORDER BY decada, calificacion DESC;
```

### 2. Actores con más apariciones en el Top
```sql
SELECT 
    nombre,
    COUNT(*) as apariciones,
    ROUND(AVG(calificacion), 2) as calificacion_promedio
FROM actores a
JOIN peliculas p ON a.pelicula_id = p.id
GROUP BY nombre
HAVING COUNT(*) >= 2
ORDER BY apariciones DESC, calificacion_promedio DESC;
```

### 3. Análisis de tendencias por año
```sql
SELECT 
    anio,
    COUNT(*) as peliculas_año,
    AVG(calificacion) as calificacion_promedio,
    AVG(duracion_minutos) as duracion_promedio
FROM peliculas
WHERE anio >= 2000
GROUP BY anio
ORDER BY anio DESC;
```

## 🚀 Ejecución de Consultas

### Automática con Script
```bash
./scripts/analyze_data.sh
```

### Manual en PostgreSQL
```bash
# Conectar a PostgreSQL
docker-compose exec postgres psql -U imdb_user -d imdb_scraper_db

# Ejecutar archivo completo
\i /path/to/advanced_queries.sql

# Ejecutar función específica
SELECT * FROM analyze_rating_correlation();
```

## 💡 Ventajas del Modelo Implementado

1. **🔧 Normalización**: Datos sin redundancia
2. **⚡ Optimización**: Índices estratégicos para consultas frecuentes
3. **📊 Flexibilidad**: Múltiples dimensiones de análisis
4. **🔍 Escalabilidad**: Preparado para grandes volúmenes de datos
5. **🛡️ Integridad**: Constraints y validaciones automáticas
6. **📈 Análisis**: Window functions y estadísticas avanzadas

## 📝 Próximas Mejoras

- [ ] **Particionamiento**: Por décadas para datasets grandes
- [ ] **Índices Parciales**: Para consultas específicas frecuentes  
- [ ] **Triggers**: Para auditoría automática de cambios
- [ ] **Funciones de Machine Learning**: Con extensiones como MADlib
- [ ] **API REST**: Para consumo de datos desde aplicaciones web
