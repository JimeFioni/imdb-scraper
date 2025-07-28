#!/bin/bash
# Script para ejecutar el scraper de IMDb con PostgreSQL

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🎬 Scraper IMDb con PostgreSQL${NC}"
echo "==============================="
echo ""

# Función para activar entorno virtual
activate_venv() {
    if [[ -d "venv" ]]; then
        echo -e "${BLUE}🐍 Activando entorno virtual...${NC}"
        source venv/bin/activate
        if [[ "$VIRTUAL_ENV" != "" ]]; then
            echo -e "${GREEN}✅ Entorno virtual activado: $(basename $VIRTUAL_ENV)${NC}"
            echo -e "${BLUE}📍 Python: $(which python3)${NC}"
            return 0
        else
            echo -e "${RED}❌ Error activando entorno virtual${NC}"
            return 1
        fi
    else
        echo -e "${RED}❌ Entorno virtual no encontrado${NC}"
        echo -e "${BLUE}Creando entorno virtual...${NC}"
        python3 -m venv venv
        source venv/bin/activate
        pip install -r config/requirements.txt
        return 0
    fi
}

# Función para verificar PostgreSQL
check_postgres() {
    echo -e "${BLUE}🐘 Verificando PostgreSQL...${NC}"
    
    # Verificar si PostgreSQL está ejecutándose localmente
    if brew services list | grep postgresql@15 | grep started &> /dev/null; then
        echo -e "${GREEN}✅ PostgreSQL local está ejecutándose${NC}"
        
        # Probar conexión
        export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"
        if psql -U imdb_user -d imdb_scraper_db -c "SELECT 1;" &> /dev/null; then
            echo -e "${GREEN}✅ Conexión a PostgreSQL exitosa${NC}"
            return 0
        else
            echo -e "${YELLOW}⚠️  PostgreSQL ejecutándose pero no se puede conectar${NC}"
            return 1
        fi
    else
        echo -e "${YELLOW}⚠️  PostgreSQL no está ejecutándose${NC}"
        echo -e "${BLUE}Iniciando PostgreSQL...${NC}"
        brew services start postgresql@15
        sleep 3
        return 1
    fi
}

# Función para ejecutar el scraper
run_scraper() {
    echo -e "${BLUE}🚀 Ejecutando scraper con PostgreSQL...${NC}"
    
    # Limpiar archivos anteriores
    echo -e "${BLUE}🗑️ Limpiando archivos anteriores...${NC}"
    rm -f data/exports/peliculas.csv
    rm -f data/exports/peliculas.db
    
    # Ejecutar scraper
    cd imdb_scraper
    scrapy crawl top_movies -s ITEM_PIPELINES='{"imdb_scraper.pipelines.ImdbScraperPipeline": 300, "imdb_scraper.postgresql_pipeline.PostgreSQLPipeline": 400, "imdb_scraper.pipelines.CsvExportPipeline": 500}'
    cd ..
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Scraper ejecutado exitosamente${NC}"
        
        # Verificar archivos generados
        echo -e "${BLUE}📊 Verificando resultados...${NC}"
        
        if [[ -f "data/exports/peliculas.csv" ]]; then
            local movies=$(tail -n +2 data/exports/peliculas.csv | wc -l | tr -d ' ')
            echo -e "${GREEN}✅ CSV generado: $movies películas extraídas${NC}"
            echo -e "${BLUE}📄 Archivo: data/exports/peliculas.csv${NC}"
        fi
        
        if [[ -f "data/exports/peliculas.db" ]]; then
            echo -e "${GREEN}✅ Base de datos SQLite generada${NC}"
            echo -e "${BLUE}🗃️  Archivo: data/exports/peliculas.db${NC}"
        fi
        
        # Verificar datos en PostgreSQL
        export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"
        local pg_count=$(psql -U imdb_user -d imdb_scraper_db -t -c "SELECT COUNT(*) FROM peliculas;" 2>/dev/null | tr -d ' ')
        if [[ "$pg_count" =~ ^[0-9]+$ ]] && [[ $pg_count -gt 0 ]]; then
            echo -e "${GREEN}✅ Datos guardados en PostgreSQL: $pg_count películas${NC}"
        else
            echo -e "${YELLOW}⚠️  No se pudieron verificar datos en PostgreSQL${NC}"
        fi
        
        return 0
    else
        echo -e "${RED}❌ Error ejecutando el scraper${NC}"
        return 1
    fi
}

# Función principal
main() {
    # Activar entorno virtual
    if ! activate_venv; then
        echo -e "${RED}❌ No se pudo activar el entorno virtual${NC}"
        exit 1
    fi
    
    echo ""
    
    # Verificar PostgreSQL
    if ! check_postgres; then
        echo -e "${YELLOW}⚠️  Ejecutando sin PostgreSQL (solo CSV y SQLite)${NC}"
        echo ""
        read -p "¿Continuar sin PostgreSQL? (y/N): " continue_choice
        if [[ ! $continue_choice =~ ^[Yy]$ ]]; then
            echo -e "${BLUE}Para configurar PostgreSQL ejecuta: ./setup_postgres_local.sh${NC}"
            exit 1
        fi
    fi
    
    echo ""
    
    # Ejecutar scraper
    run_scraper
    
    echo ""
    echo -e "${BLUE}📁 Archivos generados en: data/exports/${NC}"
    echo -e "${BLUE}📜 Logs disponibles en: logs/scrapy.log${NC}"
    
    if check_postgres &> /dev/null; then
        echo -e "${BLUE}🐘 Para consultas SQL: psql -U imdb_user -d imdb_scraper_db${NC}"
    fi
}

# Ejecutar función principal
main
