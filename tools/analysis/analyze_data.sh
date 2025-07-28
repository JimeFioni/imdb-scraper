#!/bin/bash

# ===============================================
# EJECUTAR CONSULTAS SQL AVANZADAS
# Script para análisis completo de datos
# ===============================================

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar que PostgreSQL esté ejecutándose
check_postgresql() {
    if ! docker-compose -f ../database/docker-compose.yml ps postgres | grep -q "Up"; then
        print_error "PostgreSQL no está ejecutándose"
        print_status "Ejecuta: cd ../database && docker-compose up -d"
        exit 1
    fi
    print_success "PostgreSQL está activo"
}

# Ejecutar consulta específica
run_query() {
    local query_name="$1"
    local query="$2"
    
    print_status "Ejecutando: $query_name"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    docker-compose -f ../database/docker-compose.yml exec -T postgres psql -U imdb_user -d imdb_scraper_db -c "$query" || {
        print_error "Error ejecutando consulta: $query_name"
        return 1
    }
    
    echo ""
}

# Ejecutar archivo SQL completo
run_sql_file() {
    local file_path="$1"
    local description="$2"
    
    if [[ ! -f "$file_path" ]]; then
        print_error "Archivo no encontrado: $file_path"
        return 1
    fi
    
    print_status "Ejecutando: $description"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    docker-compose -f ../database/docker-compose.yml exec -T postgres psql -U imdb_user -d imdb_scraper_db -f - < "$file_path" || {
        print_error "Error ejecutando archivo: $file_path"
        return 1
    }
    
    echo ""
}

# Mostrar estadísticas básicas
show_basic_stats() {
    print_status "📊 ESTADÍSTICAS BÁSICAS"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Contar registros
    run_query "Total de películas" "SELECT COUNT(*) as total_peliculas FROM peliculas;"
    run_query "Total de actores" "SELECT COUNT(*) as total_actores FROM actores;"
    run_query "Rango de años" "SELECT MIN(anio) as año_inicial, MAX(anio) as año_final FROM peliculas WHERE anio IS NOT NULL;"
    run_query "Calificación promedio" "SELECT ROUND(AVG(calificacion), 2) as calificacion_promedio FROM peliculas WHERE calificacion IS NOT NULL;"
}

# Análisis de correlación IMDb vs Metascore
analyze_correlation() {
    print_status "🔍 ANÁLISIS DE CORRELACIÓN IMDb vs METASCORE"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    run_query "Correlación IMDb-Metascore" "SELECT * FROM analyze_rating_correlation();"
}

# Top películas por década
analyze_decades() {
    print_status "📅 ANÁLISIS POR DÉCADAS"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    run_query "Películas por década" "
    SELECT 
        (anio / 10 * 10) as decada,
        COUNT(*) as total_peliculas,
        ROUND(AVG(calificacion), 2) as calificacion_promedio,
        ROUND(AVG(duracion_minutos), 0) as duracion_promedio_min
    FROM peliculas 
    WHERE anio IS NOT NULL AND calificacion IS NOT NULL
    GROUP BY (anio / 10 * 10)
    ORDER BY decada DESC;
    "
}

# Actores más frecuentes
analyze_actors() {
    print_status "🎭 ACTORES MÁS FRECUENTES"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    run_query "Top 10 actores más frecuentes" "
    SELECT 
        a.nombre,
        COUNT(*) as apariciones,
        ROUND(AVG(p.calificacion), 2) as calificacion_promedio,
        STRING_AGG(p.titulo, ', ' ORDER BY p.calificacion DESC) as peliculas
    FROM actores a
    JOIN peliculas p ON a.pelicula_id = p.id
    WHERE p.calificacion IS NOT NULL
    GROUP BY a.nombre
    HAVING COUNT(*) >= 2
    ORDER BY apariciones DESC, calificacion_promedio DESC
    LIMIT 10;
    "
}

# Estadísticas de películas
analyze_movies() {
    print_status "🎬 ANÁLISIS DE PELÍCULAS"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    run_query "Top 10 películas mejor calificadas" "
    SELECT 
        ranking,
        titulo,
        anio,
        calificacion,
        COALESCE(metascore, 0) as metascore,
        duracion_minutos || ' min' as duracion
    FROM peliculas 
    WHERE calificacion IS NOT NULL
    ORDER BY calificacion DESC, ranking ASC
    LIMIT 10;
    "
    
    run_query "Películas más largas" "
    SELECT 
        titulo,
        anio,
        duracion_minutos || ' min' as duracion,
        ROUND(duracion_minutos / 60.0, 1) || ' hrs' as duracion_horas,
        calificacion
    FROM peliculas 
    WHERE duracion_minutos IS NOT NULL
    ORDER BY duracion_minutos DESC
    LIMIT 10;
    "
}

# Ejecutar análisis completo
run_full_analysis() {
    print_status "🚀 EJECUTANDO ANÁLISIS COMPLETO"
    echo "==============================================="
    
    show_basic_stats
    analyze_correlation
    analyze_decades
    analyze_actors
    analyze_movies
    
    print_success "✅ Análisis completo terminado"
}

# Ejecutar consultas avanzadas del archivo
run_advanced_queries() {
    print_status "🔬 EJECUTANDO CONSULTAS SQL AVANZADAS"
    echo "==============================================="
    
    if [[ -f "../database/advanced_queries.sql" ]]; then
        run_sql_file "../database/advanced_queries.sql" "Consultas SQL Avanzadas"
        print_success "✅ Consultas avanzadas ejecutadas"
    else
        print_error "Archivo advanced_queries.sql no encontrado"
    fi
}

# Mostrar menú de opciones
show_menu() {
    echo ""
    echo "==============================================="
    echo "🔍 ANÁLISIS SQL - IMDB SCRAPER"
    echo "==============================================="
    echo "1. Estadísticas básicas"
    echo "2. Análisis de correlación IMDb vs Metascore"
    echo "3. Análisis por décadas"
    echo "4. Actores más frecuentes"
    echo "5. Análisis de películas"
    echo "6. Análisis completo (todas las opciones)"
    echo "7. Ejecutar consultas SQL avanzadas (archivo completo)"
    echo "8. Salir"
    echo ""
    read -p "Selecciona una opción (1-8): " choice
}

# Función principal
main() {
    check_postgresql
    
    while true; do
        show_menu
        
        case $choice in
            1) show_basic_stats ;;
            2) analyze_correlation ;;
            3) analyze_decades ;;
            4) analyze_actors ;;
            5) analyze_movies ;;
            6) run_full_analysis ;;
            7) run_advanced_queries ;;
            8) 
                print_success "¡Hasta luego! 👋"
                exit 0
                ;;
            *)
                print_error "Opción inválida. Selecciona 1-8."
                ;;
        esac
        
        echo ""
        read -p "Presiona Enter para continuar..."
    done
}

# Ejecutar función principal
main "$@"
