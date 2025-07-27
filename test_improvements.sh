#!/bin/bash
# Script de prueba rápida - solo 3 películas

echo "🧪 Probando scraper con mejoras implementadas..."
echo "=============================================="

# Activar entorno virtual
source venv/bin/activate

# Probar solo las primeras 3 películas
echo "🎬 Probando Factory Pattern y Base de datos..."
scrapy crawl top_movies -L INFO -s CLOSESPIDER_ITEMCOUNT=3

# Verificar resultados
echo ""
echo "📊 Verificando resultados:"
if [ -f "output/peliculas.csv" ]; then
    echo "✅ CSV generado:"
    head -5 output/peliculas.csv
fi

if [ -f "output/peliculas.db" ]; then
    echo ""
    echo "✅ Base de datos generada:"
    echo "Verificando tabla..."
    sqlite3 output/peliculas.db "SELECT COUNT(*) as total_peliculas FROM peliculas;"
    echo "Primeras 3 películas en BD:"
    sqlite3 output/peliculas.db "SELECT ranking, titulo, anio, calificacion FROM peliculas LIMIT 3;"
fi
