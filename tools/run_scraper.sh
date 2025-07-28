#!/bin/bash
# Script para ejecutar el scraper de IMDb

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🎬 Iniciando scraper de IMDb Top 250...${NC}"
echo "=============================================="

# Ir al directorio raíz del proyecto
cd "$(dirname "$0")/.."

# Verificar que estamos en el directorio correcto
if [[ ! -f "run.sh" ]] || [[ ! -d "imdb_scraper" ]]; then
    echo -e "${RED}❌ Error: No se encontró el proyecto. Asegúrate de estar en el directorio correcto.${NC}"
    exit 1
fi

# Función para activar entorno virtual
activate_venv() {
    if [[ -d "venv" ]]; then
        echo -e "${BLUE}🐍 Activando entorno virtual...${NC}"
        source venv/bin/activate
        if [[ "$VIRTUAL_ENV" != "" ]]; then
            echo -e "${GREEN}✅ Entorno virtual activado: $(basename $VIRTUAL_ENV)${NC}"
            echo -e "${BLUE}📍 Python: $(which python3)${NC}"
        else
            echo -e "${RED}❌ Error activando entorno virtual${NC}"
            exit 1
        fi
    else
        echo -e "${RED}❌ Entorno virtual no encontrado. Ejecuta: python3 -m venv venv${NC}"
        exit 1
    fi
}

# Activar entorno virtual
activate_venv

# Verificar que scrapy está disponible
if ! command -v scrapy &> /dev/null; then
    echo -e "${YELLOW}⚠️  Scrapy no está disponible. Instalando dependencias...${NC}"
    pip install -r config/requirements.txt
fi

# Crear directorio exports si no existe
mkdir -p data/exports

# Limpiar archivos anteriores si existen
if [ -f "data/exports/peliculas.csv" ]; then
    rm data/exports/peliculas.csv
    echo "🗑️ Archivo CSV anterior eliminado"
fi

if [ -f "data/exports/peliculas.db" ]; then
    rm data/exports/peliculas.db
    echo "🗑️ Base de datos anterior eliminada"
fi

# Ejecutar scraper
echo "🚀 Ejecutando scraper..."
scrapy crawl top_movies -L INFO

# Verificar resultado
echo ""
echo "📊 Verificando resultados..."

if [ -f "data/exports/peliculas.csv" ]; then
    lines=$(wc -l < data/exports/peliculas.csv)
    movies=$((lines - 1))
    echo "✅ CSV generado: $movies películas extraídas"
    echo "📄 Archivo: data/exports/peliculas.csv"
else
    echo "⚠️  Archivo CSV no encontrado en data/exports/"
fi

if [ -f "data/exports/peliculas.db" ]; then
    echo "✅ Base de datos SQLite generada"
    echo "🗃️  Archivo: data/exports/peliculas.db"
else
    echo "⚠️  Base de datos SQLite no encontrada"
    echo ""
    echo "✅ ¡Scraping completado exitosamente!"
    echo "📄 Archivo generado: output/peliculas.csv"
    echo "📊 Películas extraídas: $movies"
    echo ""
    echo "🔍 Primeras 5 líneas del archivo:"
    head -6 output/peliculas.csv
else
    echo "❌ Error: No se pudo generar el archivo CSV"
fi

echo ""
echo "🎉 ¡Proceso terminado!"
