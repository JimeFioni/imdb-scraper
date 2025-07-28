#!/bin/bash
# Script principal para IMDb Scraper con PostgreSQL

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

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
            exit 1
        fi
    else
        echo -e "${RED}❌ Entorno virtual no encontrado. Ejecuta: python3 -m venv venv${NC}"
        exit 1
    fi
}

# Activar entorno virtual al inicio
activate_venv

echo -e "${BLUE}🎬 IMDb Scraper con PostgreSQL - v2.0${NC}"
echo "=========================================="
echo ""

# Mostrar opciones disponibles
echo -e "${YELLOW}Opciones disponibles:${NC}"
echo "1. 🚀 Ejecutar scraper básico (CSV + SQLite)"
echo "2. 🐘 Ejecutar scraper con PostgreSQL local"
echo "3. 📊 Análisis SQL (requiere PostgreSQL activo)"
echo "4. 🧪 Ejecutar todas las pruebas"
echo "5. 🎯 Demostración completa interactiva"
echo "6. 🐳 Configurar Docker + PostgreSQL"
echo "7. 🐘 Configurar PostgreSQL local (sin Docker)"
echo "8. 🔍 Diagnóstico completo del sistema"
echo "9. 🐍 Scraper con venv garantizado + PostgreSQL"
echo ""

read -p "Selecciona una opción (1-9) o Enter para opción 1: " choice

case ${choice:-1} in
    1)
        echo -e "${GREEN}🚀 Ejecutando scraper básico...${NC}"
        ./tools/run_scraper.sh
        ;;
    2)
        echo -e "${GREEN}🐘 Ejecutando scraper con PostgreSQL local...${NC}"
        chmod +x run_scraper_postgres_fixed.sh
        ./run_scraper_postgres_fixed.sh
        ;;
    3)
        echo -e "${GREEN}📊 Iniciando análisis SQL...${NC}"
        ./tools/analysis/analyze_data.sh
        ;;
    4)
        echo -e "${GREEN}🧪 Ejecutando suite de pruebas...${NC}"
        ./tools/maintenance/test_complete.sh
        ;;
    5)
        echo -e "${GREEN}🎯 Iniciando demostración completa...${NC}"
        ./tools/setup/demo_complete.sh
        ;;
    6)
        echo -e "${GREEN}🐳 Configurando Docker + PostgreSQL...${NC}"
        ./setup_docker_simple.sh
        ;;
    7)
        echo -e "${GREEN}🐘 Configurando PostgreSQL local...${NC}"
        ./setup_postgres_local.sh
        ;;
    8)
        echo -e "${GREEN}🔍 Ejecutando diagnóstico completo...${NC}"
        chmod +x diagnostico_completo.sh
        ./diagnostico_completo.sh
        ;;
    9)
        echo -e "${GREEN}🐍 Ejecutando scraper con venv garantizado...${NC}"
        ./run_scraper_with_venv.sh
        ;;
    *)
        echo -e "${GREEN}🚀 Ejecutando scraper básico por defecto...${NC}"
        ./tools/run_scraper.sh
        ;;
esac

echo ""
echo -e "${BLUE}📁 Archivos generados en: data/exports/${NC}"
echo -e "${BLUE}🐘 PostgreSQL: config/docker/docker-compose.yml${NC}"
echo -e "${BLUE}📊 Análisis SQL: docs/sql/SQL_ANALYSIS_GUIDE.md${NC}"
echo -e "${BLUE}📜 Documentación: README.md${NC}"
echo -e "${BLUE}📋 Estructura: docs/PROJECT_STRUCTURE.md${NC}"
