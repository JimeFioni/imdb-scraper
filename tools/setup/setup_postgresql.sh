#!/bin/bash

# ===============================================
# SCRIPT DE CONFIGURACIÓN POSTGRESQL
# Automatiza la configuración completa de PostgreSQL
# ===============================================

set -e  # Salir en caso de error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir con colores
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

# Verificar si Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker no está instalado. Instalalo desde: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        print_error "Docker no está ejecutándose. Inicia Docker Desktop o el servicio Docker."
        exit 1
    fi
    
    print_success "Docker está disponible y ejecutándose"
}

# Verificar si Docker Compose está disponible
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_error "Docker Compose no está disponible"
        exit 1
    fi
    print_success "Docker Compose está disponible"
}

# Configurar PostgreSQL con Docker
setup_postgresql() {
    print_status "Configurando PostgreSQL con Docker..."
    
    cd database/
    
    # Detener contenedores existentes
    print_status "Deteniendo contenedores existentes..."
    docker-compose down -v 2>/dev/null || true
    
    # Construir y levantar contenedores
    print_status "Iniciando PostgreSQL y pgAdmin..."
    docker-compose up -d
    
    # Esperar a que PostgreSQL esté listo
    print_status "Esperando a que PostgreSQL esté listo..."
    for i in {1..30}; do
        if docker-compose exec -T postgres pg_isready -U imdb_user -d imdb_scraper_db &>/dev/null; then
            print_success "PostgreSQL está listo!"
            break
        fi
        echo -n "."
        sleep 2
    done
    
    cd ..
}

# Verificar la conexión a PostgreSQL
verify_connection() {
    print_status "Verificando conexión a PostgreSQL..."
    
    # Instalar psycopg2 si no está disponible
    if ! python -c "import psycopg2" 2>/dev/null; then
        print_warning "Instalando psycopg2-binary..."
        pip install psycopg2-binary
    fi
    
    # Test de conexión con Python
    python -c "
import psycopg2
try:
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        database='imdb_scraper_db',
        user='imdb_user',
        password='imdb_secure_2024'
    )
    cursor = conn.cursor()
    cursor.execute('SELECT version();')
    version = cursor.fetchone()[0]
    print(f'✅ Conexión exitosa: {version}')
    
    cursor.execute('SELECT COUNT(*) FROM peliculas;')
    count = cursor.fetchone()[0]
    print(f'📊 Películas en BD: {count}')
    
    conn.close()
except Exception as e:
    print(f'❌ Error de conexión: {e}')
    exit(1)
"
}

# Ejecutar scraper con PostgreSQL
run_scraper_with_postgresql() {
    print_status "Ejecutando scraper con PostgreSQL activado..."
    
    cd ..
    scrapy crawl top_movies
    cd scripts/
}

# Mostrar información de acceso
show_access_info() {
    print_success "🎉 PostgreSQL configurado exitosamente!"
    echo ""
    echo "📊 INFORMACIÓN DE ACCESO:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🐘 PostgreSQL:"
    echo "   Host: localhost"
    echo "   Puerto: 5432"
    echo "   Base de datos: imdb_scraper_db"
    echo "   Usuario: imdb_user"
    echo "   Contraseña: imdb_secure_2024"
    echo ""
    echo "🌐 pgAdmin (Interfaz Web):"
    echo "   URL: http://localhost:8080"
    echo "   Email: admin@imdb-scraper.local"
    echo "   Contraseña: admin123"
    echo ""
    echo "🛠️  COMANDOS ÚTILES:"
    echo "   Ver logs: docker-compose logs postgres"
    echo "   Reiniciar: docker-compose restart"
    echo "   Detener: docker-compose down"
    echo "   Consola SQL: docker-compose exec postgres psql -U imdb_user -d imdb_scraper_db"
    echo ""
    echo "📝 Para ejecutar consultas SQL avanzadas:"
    echo "   cat ../database/advanced_queries.sql | docker-compose exec -T postgres psql -U imdb_user -d imdb_scraper_db"
}

# Función principal
main() {
    echo "==============================================="
    echo "🐘 CONFIGURACIÓN POSTGRESQL - IMDB SCRAPER"
    echo "==============================================="
    echo ""
    
    check_docker
    check_docker_compose
    setup_postgresql
    verify_connection
    show_access_info
    
    echo ""
    read -p "¿Deseas ejecutar el scraper ahora? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        run_scraper_with_postgresql
    fi
    
    print_success "¡Configuración completa! 🎉"
}

# Ejecutar función principal
main "$@"
