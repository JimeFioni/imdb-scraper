#!/bin/bash

# ===============================================
# DEMOSTRACIÓN COMPLETA - IMDB SCRAPER CON POSTGRESQL
# Script para mostrar todas las funcionalidades
# ===============================================

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

print_header() {
    echo -e "${PURPLE}===============================================${NC}"
    echo -e "${PURPLE}$1${NC}"
    echo -e "${PURPLE}===============================================${NC}"
}

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar dependencias
check_dependencies() {
    print_header "🔍 VERIFICANDO DEPENDENCIAS"
    
    # Python y módulos
    if python -c "import scrapy, psycopg2, pandas" 2>/dev/null; then
        print_success "✅ Módulos Python disponibles"
    else
        print_error "❌ Módulos Python faltantes"
        print_status "Instalando dependencias..."
        pip install -r requirements.txt
    fi
    
    # Docker
    if command -v docker &> /dev/null && docker info &> /dev/null; then
        print_success "✅ Docker disponible y ejecutándose"
    else
        print_warning "⚠️  Docker no disponible - PostgreSQL no funcionará"
    fi
}

# Mostrar información del proyecto
show_project_info() {
    print_header "📊 INFORMACIÓN DEL PROYECTO"
    
    echo -e "${CYAN}🎬 IMDb Top Movies Scraper${NC}"
    echo -e "${CYAN}📅 Películas objetivo: 50 del Top 250 IMDb${NC}"
    echo -e "${CYAN}🗄️  Formatos de salida: CSV, SQLite, PostgreSQL${NC}"
    echo -e "${CYAN}🔍 Consultas SQL: 20+ consultas avanzadas${NC}"
    echo ""
    
    print_status "📁 Estructura del proyecto:"
    tree -L 2 -I '__pycache__|*.pyc|venv' . || ls -la
}

# Configurar PostgreSQL si está disponible
setup_postgresql_demo() {
    print_header "🐘 CONFIGURACIÓN POSTGRESQL"
    
    if command -v docker &> /dev/null && docker info &> /dev/null; then
        print_status "Configurando PostgreSQL con Docker..."
        cd database/
        
        # Detener contenedores existentes
        docker-compose down -v 2>/dev/null || true
        
        # Iniciar PostgreSQL
        print_status "Iniciando PostgreSQL y pgAdmin..."
        docker-compose up -d
        
        # Esperar a que esté listo
        print_status "Esperando PostgreSQL..."
        for i in {1..15}; do
            if docker-compose exec -T postgres pg_isready -U imdb_user -d imdb_scraper_db &>/dev/null; then
                print_success "✅ PostgreSQL listo!"
                break
            fi
            echo -n "."
            sleep 2
        done
        
        cd ..
        
        # Mostrar información de acceso
        echo ""
        print_success "🌐 Acceso a pgAdmin: http://localhost:8080"
        print_success "📧 Email: admin@imdb-scraper.local"
        print_success "🔑 Password: admin123"
        echo ""
        
        return 0
    else
        print_warning "Docker no disponible - Saltando PostgreSQL"
        return 1
    fi
}

# Ejecutar scraper completo
run_scraper_demo() {
    print_header "🚀 EJECUTANDO SCRAPER COMPLETO"
    
    print_status "Limpiando archivos de salida anteriores..."
    rm -f output/peliculas.csv output/peliculas.db
    mkdir -p output/
    
    print_status "Iniciando scraper de IMDb..."
    print_warning "⏰ Esto puede tardar 2-3 minutos..."
    
    # Ejecutar scraper con logs informativos
    if scrapy crawl top_movies -L INFO; then
        print_success "✅ Scraper completado exitosamente"
        
        # Verificar archivos generados
        if [[ -f "output/peliculas.csv" ]]; then
            local csv_lines=$(wc -l < output/peliculas.csv)
            print_success "📄 CSV: $csv_lines líneas generadas"
        fi
        
        if [[ -f "output/peliculas.db" ]]; then
            local db_size=$(du -h output/peliculas.db | cut -f1)
            print_success "🗃️  SQLite: $db_size base de datos"
        fi
        
        return 0
    else
        print_error "❌ Error ejecutando scraper"
        return 1
    fi
}

# Mostrar resultados obtenidos
show_results() {
    print_header "📊 RESULTADOS OBTENIDOS"
    
    if [[ -f "output/peliculas.csv" ]]; then
        print_status "📄 Primeras 5 películas del CSV:"
        echo ""
        head -6 output/peliculas.csv | column -t -s ','
        echo ""
        
        local total_movies=$(tail -n +2 output/peliculas.csv | wc -l)
        print_success "Total de películas extraídas: $total_movies"
    fi
}

# Demostrar análisis PostgreSQL
demo_postgresql_analysis() {
    print_header "🔬 ANÁLISIS POSTGRESQL"
    
    # Verificar si PostgreSQL está disponible
    if docker-compose -f database/docker-compose.yml ps postgres | grep -q "Up"; then
        print_status "Ejecutando consultas de demostración..."
        
        # Estadísticas básicas
        print_status "📊 Estadísticas básicas:"
        docker-compose -f database/docker-compose.yml exec -T postgres psql -U imdb_user -d imdb_scraper_db -c "
        SELECT 
            COUNT(*) as total_peliculas,
            ROUND(AVG(calificacion), 2) as calificacion_promedio,
            MIN(anio) as año_inicio,
            MAX(anio) as año_fin
        FROM peliculas;" 2>/dev/null || echo "Sin datos aún"
        
        # Top 5 películas
        print_status "🏆 Top 5 películas mejor calificadas:"
        docker-compose -f database/docker-compose.yml exec -T postgres psql -U imdb_user -d imdb_scraper_db -c "
        SELECT titulo, anio, calificacion 
        FROM peliculas 
        WHERE calificacion IS NOT NULL 
        ORDER BY calificacion DESC 
        LIMIT 5;" 2>/dev/null || echo "Sin datos aún"
        
        # Información de acceso
        echo ""
        print_success "🌐 Acceso completo a PostgreSQL:"
        echo -e "   ${CYAN}Host:${NC} localhost:5432"
        echo -e "   ${CYAN}Base de datos:${NC} imdb_scraper_db"
        echo -e "   ${CYAN}Usuario:${NC} imdb_user"
        echo -e "   ${CYAN}Contraseña:${NC} imdb_secure_2024"
        
    else
        print_warning "PostgreSQL no está ejecutándose"
        print_status "Para análisis completo, ejecuta: ./scripts/setup_postgresql.sh"
    fi
}

# Mostrar próximos pasos
show_next_steps() {
    print_header "🎯 PRÓXIMOS PASOS"
    
    echo -e "${CYAN}Para análisis SQL avanzado:${NC}"
    echo "   ./scripts/analyze_data.sh"
    echo ""
    echo -e "${CYAN}Para configurar PostgreSQL:${NC}"
    echo "   ./scripts/setup_postgresql.sh"
    echo ""
    echo -e "${CYAN}Para ejecutar pruebas completas:${NC}"
    echo "   ./scripts/test_complete.sh"
    echo ""
    echo -e "${CYAN}Para consultas SQL avanzadas:${NC}"
    echo "   cat database/advanced_queries.sql"
    echo ""
    echo -e "${CYAN}Documentación SQL detallada:${NC}"
    echo "   database/SQL_ANALYSIS_GUIDE.md"
    echo ""
    
    print_success "🎉 ¡Demostración completa!"
}

# Función principal
main() {
    clear
    print_header "🎬 DEMOSTRACIÓN IMDB SCRAPER CON POSTGRESQL"
    echo ""
    
    # Verificar directorio
    if [[ ! -f "scrapy.cfg" ]]; then
        print_error "Ejecuta este script desde el directorio raíz del proyecto"
        exit 1
    fi
    
    # Pasos de la demostración
    check_dependencies
    echo ""
    
    show_project_info
    echo ""
    
    # Preguntar si configurar PostgreSQL
    echo ""
    read -p "¿Configurar PostgreSQL con Docker? (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        setup_postgresql_demo
        POSTGRES_ENABLED=true
    else
        POSTGRES_ENABLED=false
        print_status "Continuando sin PostgreSQL..."
    fi
    echo ""
    
    # Preguntar si ejecutar scraper
    read -p "¿Ejecutar scraper completo de IMDb? (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        run_scraper_demo
        echo ""
        show_results
    else
        print_status "Saltando ejecución del scraper..."
    fi
    echo ""
    
    # Mostrar análisis PostgreSQL si está disponible
    if [[ "$POSTGRES_ENABLED" == "true" ]]; then
        demo_postgresql_analysis
        echo ""
    fi
    
    show_next_steps
}

# Ejecutar demostración
main "$@"
