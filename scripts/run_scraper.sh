#!/bin/bash
# Script para ejecutar el scraper de IMDb

echo "🎬 Iniciando scraper de IMDb Top 250..."
echo "=============================================="

# Ir al directorio raíz del proyecto
cd "$(dirname "$0")/.."

# Activar entorno virtual
source venv/bin/activate

# Crear directorio output si no existe
mkdir -p output

# Limpiar archivo anterior si existe
if [ -f "output/peliculas.csv" ]; then
    rm output/peliculas.csv
    echo "🗑️ Archivo anterior eliminado"
fi

# Ejecutar scraper
echo "🚀 Ejecutando scraper..."
scrapy crawl top_movies -L INFO

# Verificar resultado
if [ -f "output/peliculas.csv" ]; then
    lines=$(wc -l < output/peliculas.csv)
    movies=$((lines - 1))
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
