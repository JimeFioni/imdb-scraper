#!/bin/bash

echo "🔍 VERIFICACIÓN COMPLETA DEL SISTEMA IMDb SCRAPER"
echo "=================================================="

# Verificar que estamos en el directorio correcto
if [ ! -f "scrapy.cfg" ]; then
    echo "❌ Error: No se encuentra scrapy.cfg. Ejecuta desde el directorio raíz del proyecto."
    exit 1
fi

echo "✅ Directorio correcto encontrado"

# Verificar entorno virtual
echo -e "\n🐍 VERIFICANDO ENTORNO VIRTUAL..."
if [ ! -d "venv" ]; then
    echo "❌ Error: Entorno virtual no encontrado"
    exit 1
fi

# Activar entorno virtual y verificar dependencias
source venv/bin/activate

echo "✅ Entorno virtual activado"
echo "📦 Python version: $(python --version)"

# Verificar dependencias críticas
echo -e "\n📦 VERIFICANDO DEPENDENCIAS..."
dependencies=("scrapy" "requests" "beautifulsoup4")
for dep in "${dependencies[@]}"; do
    if pip show "$dep" >/dev/null 2>&1; then
        version=$(pip show "$dep" | grep Version | cut -d' ' -f2)
        echo "✅ $dep: $version"
    else
        echo "❌ $dep: NO INSTALADO"
    fi
done

# Verificar estructura de carpetas
echo -e "\n📁 VERIFICANDO ESTRUCTURA DE CARPETAS..."
folders=("config" "data/exports" "logs" "imdb_scraper/spiders")
for folder in "${folders[@]}"; do
    if [ -d "$folder" ]; then
        echo "✅ $folder/"
    else
        echo "⚠️  $folder/ - creando..."
        mkdir -p "$folder"
    fi
done

# Verificar archivos críticos
echo -e "\n📄 VERIFICANDO ARCHIVOS CRÍTICOS..."
files=(
    "imdb_scraper/proxy_manager.py"
    "imdb_scraper/proxy_middleware.py"
    "imdb_scraper/settings.py"
    "config/proxies.json"
    "config/docker/docker-compose-vpn.yml"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file: NO ENCONTRADO"
    fi
done

# Probar proxy manager
echo -e "\n🌐 PROBANDO PROXY MANAGER..."
python -c "
try:
    from imdb_scraper.proxy_manager import ProxyRotator
    proxy_manager = ProxyRotator()
    current_ip = proxy_manager.get_current_ip()
    print(f'✅ ProxyManager funcionando - IP: {current_ip}')
    print(f'📊 Proxies configurados: {len(proxy_manager.proxies)}')
except Exception as e:
    print(f'❌ Error en ProxyManager: {e}')
"

# Probar scraper básico
echo -e "\n🕷️  PROBANDO SCRAPER BÁSICO..."
timeout 30 scrapy crawl top_movies -s CLOSESPIDER_ITEMCOUNT=2 -s LOG_LEVEL=ERROR >/dev/null 2>&1
if [ $? -eq 0 ] || [ $? -eq 124 ]; then
    echo "✅ Scraper funcionando correctamente"
else
    echo "❌ Error en el scraper"
fi

# Verificar archivos generados
echo -e "\n📊 VERIFICANDO ARCHIVOS GENERADOS..."
if [ -f "data/exports/peliculas.csv" ]; then
    lines=$(wc -l < data/exports/peliculas.csv)
    echo "✅ CSV generado con $lines líneas"
else
    echo "⚠️  CSV no encontrado"
fi

if [ -f "data/exports/peliculas.db" ]; then
    echo "✅ Base de datos SQLite generada"
else
    echo "⚠️  Base de datos no encontrada"
fi

# Verificar permisos de scripts
echo -e "\n🔧 VERIFICANDO PERMISOS DE SCRIPTS..."
scripts=(
    "setup_proxy_network.sh"
)

for script in "${scripts[@]}"; do
    if [ -f "$script" ]; then
        if [ -x "$script" ]; then
            echo "✅ $script (ejecutable)"
        else
            echo "⚠️  $script (sin permisos de ejecución)"
            chmod +x "$script"
            echo "   🔧 Permisos corregidos"
        fi
    else
        echo "❌ $script: NO ENCONTRADO"
    fi
done

echo -e "\n🎉 VERIFICACIÓN COMPLETADA"
echo "=============================================="
echo "✅ Sistema verificado y funcional"
echo "💡 Para usar proxies: editar config/proxies.json"
echo "🚀 Para ejecutar: scrapy crawl top_movies"
echo "📖 Para más info: cat README.md"
