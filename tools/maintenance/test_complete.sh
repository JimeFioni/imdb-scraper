#!/bin/bash

# ===============================================
# SCRIPT DE PRUEBA COMPLETA - IMDB SCRAPER
# Verifica funcionalidad completa con PostgreSQL
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

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Variables de control
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Función para ejecutar test
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    print_status "Test $TOTAL_TESTS: $test_name"
    
    if eval "$test_command" &>/dev/null; then
        print_success "✅ $test_name - PASSED"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        return 0
    else
        print_error "❌ $test_name - FAILED"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        return 1
    fi
}

# Test de dependencias Python
test_python_dependencies() {
    run_test "Importar Scrapy" "python -c 'import scrapy'"
    run_test "Importar pandas" "python -c 'import pandas'"
    run_test "Importar psycopg2" "python -c 'import psycopg2'"
    run_test "Importar BeautifulSoup" "python -c 'from bs4 import BeautifulSoup'"
}

# Test de Docker
test_docker() {
    run_test "Docker disponible" "docker --version"
    run_test "Docker Compose disponible" "docker compose version || docker-compose --version"
}

# Test de archivos del proyecto
test_project_files() {
    run_test "Spider principal" "test -f imdb_scraper/spiders/top_movies.py"
    run_test "Pipeline PostgreSQL" "test -f imdb_scraper/postgresql_pipeline.py"
    run_test "Factory Pattern" "test -f imdb_scraper/selector_factory.py"
    run_test "Schema SQL" "test -f database/schema.sql"
    run_test "Consultas avanzadas" "test -f database/advanced_queries.sql"
    run_test "Docker Compose" "test -f database/docker-compose.yml"
}

# Test de PostgreSQL (si está ejecutándose)
test_postgresql() {
    if docker-compose -f database/docker-compose.yml ps postgres | grep -q "Up"; then
        print_status "PostgreSQL detectado, ejecutando tests de BD..."
        
        run_test "Conexión PostgreSQL" "docker-compose -f database/docker-compose.yml exec -T postgres pg_isready -U imdb_user -d imdb_scraper_db"
        run_test "Tabla películas existe" "docker-compose -f database/docker-compose.yml exec -T postgres psql -U imdb_user -d imdb_scraper_db -c 'SELECT 1 FROM peliculas LIMIT 1;'"
        run_test "Función de análisis existe" "docker-compose -f database/docker-compose.yml exec -T postgres psql -U imdb_user -d imdb_scraper_db -c 'SELECT analyze_rating_correlation();'"
    else
        print_warning "PostgreSQL no está ejecutándose - Saltando tests de BD"
        print_warning "Para activar: cd database && docker-compose up -d"
    fi
}

# Test de scraper (versión corta)
test_scraper_functionality() {
    print_status "Ejecutando test del scraper (5 películas)..."
    
    # Crear configuración temporal para test rápido
    cp imdb_scraper/spiders/top_movies.py imdb_scraper/spiders/top_movies_backup.py
    
    # Modificar temporalmente para solo 5 películas
    sed -i.bak 's/TOP_50_MOVIE_IDS = \[/TOP_5_MOVIE_IDS = [/' imdb_scraper/spiders/top_movies.py
    sed -i.bak 's/self\.TOP_50_MOVIE_IDS/self.TOP_5_MOVIE_IDS[:5]/' imdb_scraper/spiders/top_movies.py
    
    if timeout 60 scrapy crawl top_movies -s LOG_LEVEL=WARNING &>/dev/null; then
        print_success "✅ Scraper funciona correctamente"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        
        # Verificar archivo de salida
        if [[ -f "output/peliculas.csv" ]] && [[ $(wc -l < output/peliculas.csv) -gt 1 ]]; then
            print_success "✅ Archivo CSV generado correctamente"
            PASSED_TESTS=$((PASSED_TESTS + 1))
        else
            print_error "❌ Archivo CSV no generado o vacío"
            FAILED_TESTS=$((FAILED_TESTS + 1))
        fi
    else
        print_error "❌ Error ejecutando scraper"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
    
    TOTAL_TESTS=$((TOTAL_TESTS + 2))
    
    # Restaurar archivo original
    mv imdb_scraper/spiders/top_movies_backup.py imdb_scraper/spiders/top_movies.py
    rm -f imdb_scraper/spiders/top_movies.py.bak
}

# Test de scripts ejecutables
test_scripts() {
    run_test "Script de configuración PostgreSQL" "test -x scripts/setup_postgresql.sh"
    run_test "Script de análisis" "test -x scripts/analyze_data.sh"
    run_test "Script principal ejecutable" "test -x run.sh"
}

# Función para mostrar resumen
show_summary() {
    echo ""
    echo "==============================================="
    echo "📊 RESUMEN DE PRUEBAS"
    echo "==============================================="
    echo -e "Total de pruebas: ${BLUE}$TOTAL_TESTS${NC}"
    echo -e "Pruebas exitosas: ${GREEN}$PASSED_TESTS${NC}"
    echo -e "Pruebas fallidas: ${RED}$FAILED_TESTS${NC}"
    
    if [[ $FAILED_TESTS -eq 0 ]]; then
        echo -e "\n${GREEN}🎉 ¡TODAS LAS PRUEBAS PASARON!${NC}"
        echo -e "${GREEN}✅ El proyecto está completamente funcional${NC}"
        return 0
    else
        echo -e "\n${YELLOW}⚠️  Algunas pruebas fallaron${NC}"
        echo -e "${YELLOW}📝 Revisa los errores arriba y corrige los problemas${NC}"
        return 1
    fi
}

# Función principal
main() {
    echo "==============================================="
    echo "🧪 SUITE DE PRUEBAS - IMDB SCRAPER"
    echo "==============================================="
    echo ""
    
    print_status "Iniciando suite de pruebas completa..."
    echo ""
    
    print_status "🐍 Probando dependencias Python..."
    test_python_dependencies
    echo ""
    
    print_status "🐳 Probando Docker..."
    test_docker
    echo ""
    
    print_status "📁 Probando archivos del proyecto..."
    test_project_files
    echo ""
    
    print_status "🐘 Probando PostgreSQL..."
    test_postgresql
    echo ""
    
    print_status "📜 Probando scripts..."
    test_scripts
    echo ""
    
    print_status "🎬 Probando funcionalidad del scraper..."
    test_scraper_functionality
    echo ""
    
    show_summary
}

# Verificar que estamos en el directorio correcto
if [[ ! -f "scrapy.cfg" ]]; then
    print_error "Este script debe ejecutarse desde el directorio raíz del proyecto"
    exit 1
fi

# Ejecutar función principal
main "$@"
