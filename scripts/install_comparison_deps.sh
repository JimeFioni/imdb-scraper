#!/bin/bash

echo "🔧 INSTALACIÓN DE DEPENDENCIAS PARA COMPARACIÓN TÉCNICA"
echo "======================================================="

# Verificar que estamos en el entorno virtual
if [ -z "$VIRTUAL_ENV" ] && [ ! -f "venv/bin/activate" ]; then
    echo "❌ Error: Entorno virtual no encontrado"
    echo "💡 Ejecuta: source venv/bin/activate"
    exit 1
fi

# Activar entorno virtual si no está activo
if [ -z "$VIRTUAL_ENV" ]; then
    echo "🔄 Activando entorno virtual..."
    source venv/bin/activate
fi

echo "✅ Entorno virtual activo: $VIRTUAL_ENV"

# Función para instalar y verificar paquetes
install_package() {
    local package=$1
    local description=$2
    
    echo -e "\n📦 Instalando $description..."
    
    if pip install "$package" --quiet; then
        echo "✅ $description instalado exitosamente"
    else
        echo "❌ Error instalando $description"
        return 1
    fi
}

# Función para verificar instalación
verify_installation() {
    local package=$1
    local description=$2
    
    if python -c "import $package" 2>/dev/null; then
        echo "✅ $description verificado"
        return 0
    else
        echo "❌ $description no disponible"
        return 1
    fi
}

echo -e "\n🚀 INSTALANDO DEPENDENCIAS DE BENCHMARKING..."

# 1. Dependencias básicas de sistema
install_package "psutil" "Monitor de procesos del sistema"

# 2. Selenium y dependencias
echo -e "\n🌐 INSTALANDO SELENIUM..."
install_package "selenium" "Selenium WebDriver"
install_package "webdriver-manager" "WebDriver Manager"

# 3. Playwright (más complejo)
echo -e "\n🎭 INSTALANDO PLAYWRIGHT..."
if install_package "playwright" "Playwright"; then
    echo "🔧 Instalando navegadores de Playwright..."
    if playwright install chromium --quiet 2>/dev/null; then
        echo "✅ Navegador Chromium instalado"
    else
        echo "⚠️  Error instalando navegadores (puede requerir permisos)"
    fi
fi

# 4. Dependencias adicionales para benchmark
echo -e "\n📊 INSTALANDO DEPENDENCIAS DE ANÁLISIS..."
install_package "matplotlib" "Gráficos y visualización"
install_package "pandas" "Análisis de datos"

echo -e "\n🔍 VERIFICANDO INSTALACIONES..."

# Verificar todas las dependencias
verify_installation "psutil" "PSUtil"
verify_installation "selenium" "Selenium"
verify_installation "playwright" "Playwright"

# Verificar Scrapy (ya debería estar instalado)
verify_installation "scrapy" "Scrapy"

echo -e "\n📋 RESUMEN DE INSTALACIÓN:"
echo "=========================="

# Generar reporte de dependencias
python -c "
import sys
packages = ['scrapy', 'selenium', 'playwright', 'psutil', 'requests']

print('Paquete       | Estado    | Versión')
print('-' * 40)

for pkg in packages:
    try:
        module = __import__(pkg)
        version = getattr(module, '__version__', 'N/A')
        print(f'{pkg:<12} | ✅ OK      | {version}')
    except ImportError:
        print(f'{pkg:<12} | ❌ Error   | No instalado')
"

echo -e "\n💡 PRÓXIMOS PASOS:"
echo "=================="
echo "1. Ejecutar benchmark: python benchmark/performance_comparison.py"
echo "2. Ver ejemplos: python examples/playwright_scraper.py"
echo "3. Comparar resultados en benchmark/performance_report.txt"

echo -e "\n✅ Instalación de dependencias completada"
