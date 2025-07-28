-- ===============================================
-- MODELO RELACIONAL IMDB SCRAPER
-- PostgreSQL Schema para análisis avanzado
-- ===============================================

-- Crear base de datos
-- CREATE DATABASE imdb_scraper_db;
-- \c imdb_scraper_db;

-- Extensiones útiles para análisis
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ===============================================
-- TABLAS PRINCIPALES
-- ===============================================

-- Tabla de películas
CREATE TABLE IF NOT EXISTS peliculas (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE,
    titulo VARCHAR(255) NOT NULL,
    anio INTEGER CHECK (anio >= 1900 AND anio <= 2030),
    calificacion DECIMAL(3,1) CHECK (calificacion >= 0.0 AND calificacion <= 10.0),
    duracion_minutos INTEGER CHECK (duracion_minutos > 0),
    duracion_texto VARCHAR(50), -- Formato original "2h 22m"
    metascore INTEGER CHECK (metascore >= 0 AND metascore <= 100),
    ranking INTEGER UNIQUE CHECK (ranking > 0),
    fecha_scraping TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Índices para optimización
    CONSTRAINT unique_titulo_anio UNIQUE(titulo, anio)
);

-- Tabla de actores
CREATE TABLE IF NOT EXISTS actores (
    id SERIAL PRIMARY KEY,
    pelicula_id INTEGER NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    posicion INTEGER CHECK (posicion >= 1 AND posicion <= 3), -- 1=principal, 2=segundo, 3=tercero
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Relación con películas
    FOREIGN KEY (pelicula_id) REFERENCES peliculas(id) ON DELETE CASCADE,
    
    -- Evitar duplicados
    CONSTRAINT unique_actor_pelicula_posicion UNIQUE(pelicula_id, posicion),
    CONSTRAINT unique_actor_pelicula_nombre UNIQUE(pelicula_id, nombre)
);

-- ===============================================
-- TABLAS AUXILIARES PARA ANÁLISIS
-- ===============================================

-- Tabla de décadas para análisis temporal
CREATE TABLE IF NOT EXISTS decadas (
    id SERIAL PRIMARY KEY,
    decada INTEGER UNIQUE NOT NULL, -- 1990, 2000, 2010, etc.
    nombre VARCHAR(20) NOT NULL,    -- "1990s", "2000s", etc.
    descripcion TEXT
);

-- Tabla de géneros (expandible)
CREATE TABLE IF NOT EXISTS generos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT
);

-- Tabla relacional película-género (many-to-many)
CREATE TABLE IF NOT EXISTS pelicula_generos (
    pelicula_id INTEGER NOT NULL,
    genero_id INTEGER NOT NULL,
    PRIMARY KEY (pelicula_id, genero_id),
    FOREIGN KEY (pelicula_id) REFERENCES peliculas(id) ON DELETE CASCADE,
    FOREIGN KEY (genero_id) REFERENCES generos(id) ON DELETE CASCADE
);

-- ===============================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- ===============================================

-- Índices principales
CREATE INDEX IF NOT EXISTS idx_peliculas_anio ON peliculas(anio);
CREATE INDEX IF NOT EXISTS idx_peliculas_calificacion ON peliculas(calificacion DESC);
CREATE INDEX IF NOT EXISTS idx_peliculas_metascore ON peliculas(metascore DESC);
CREATE INDEX IF NOT EXISTS idx_peliculas_duracion ON peliculas(duracion_minutos);
CREATE INDEX IF NOT EXISTS idx_peliculas_ranking ON peliculas(ranking);

-- Índices compuestos para consultas frecuentes
CREATE INDEX IF NOT EXISTS idx_peliculas_anio_calificacion ON peliculas(anio, calificacion DESC);
CREATE INDEX IF NOT EXISTS idx_peliculas_decada ON peliculas((anio / 10 * 10)); -- Índice funcional para décadas

-- Índices para actores
CREATE INDEX IF NOT EXISTS idx_actores_pelicula ON actores(pelicula_id);
CREATE INDEX IF NOT EXISTS idx_actores_nombre ON actores(nombre);
CREATE INDEX IF NOT EXISTS idx_actores_posicion ON actores(posicion);

-- Índice para búsquedas de texto
CREATE INDEX IF NOT EXISTS idx_peliculas_titulo_gin ON peliculas USING gin(to_tsvector('spanish', titulo));
CREATE INDEX IF NOT EXISTS idx_actores_nombre_gin ON actores USING gin(to_tsvector('spanish', nombre));

-- ===============================================
-- TRIGGERS PARA AUTOMATIZACIÓN
-- ===============================================

-- Función para actualizar timestamp
CREATE OR REPLACE FUNCTION update_fecha_actualizacion()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para películas
CREATE TRIGGER trigger_peliculas_fecha_actualizacion
    BEFORE UPDATE ON peliculas
    FOR EACH ROW
    EXECUTE FUNCTION update_fecha_actualizacion();

-- ===============================================
-- INSERTAR DATOS DE DÉCADAS
-- ===============================================

INSERT INTO decadas (decada, nombre, descripcion) VALUES
(1920, '1920s', 'Era del cine mudo y primeros talkies'),
(1930, '1930s', 'Edad dorada de Hollywood'),
(1940, '1940s', 'Era de la Segunda Guerra Mundial'),
(1950, '1950s', 'Época clásica del cine'),
(1960, '1960s', 'Nueva ola y revolución cinematográfica'),
(1970, '1970s', 'Nuevo Hollywood'),
(1980, '1980s', 'Era de los blockbusters'),
(1990, '1990s', 'Cine digital emergente'),
(2000, '2000s', 'Era digital'),
(2010, '2010s', 'Cine moderno'),
(2020, '2020s', 'Cine contemporáneo')
ON CONFLICT (decada) DO NOTHING;

-- ===============================================
-- COMENTARIOS EN TABLAS
-- ===============================================

COMMENT ON TABLE peliculas IS 'Tabla principal con información de películas del Top 250 de IMDb';
COMMENT ON TABLE actores IS 'Tabla de actores principales por película (máximo 3 por película)';
COMMENT ON TABLE decadas IS 'Tabla auxiliar para análisis temporal por décadas';

COMMENT ON COLUMN peliculas.duracion_minutos IS 'Duración en minutos extraída del texto original';
COMMENT ON COLUMN peliculas.duracion_texto IS 'Formato original de duración (ej: "2h 22m")';
COMMENT ON COLUMN peliculas.metascore IS 'Puntuación de Metacritic (0-100)';
COMMENT ON COLUMN actores.posicion IS 'Orden de importancia: 1=principal, 2=segundo, 3=tercero';
