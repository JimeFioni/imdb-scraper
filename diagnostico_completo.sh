#!/bin/bash
# Script de diagnóstico completo para IMDb Scraper con activación de venv

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🔍 Diagnóstico Completo - IMDb Scraper${NC}"
echo "=========================================="
echo ""

# Función para activar entorno virtual
activate_venv() {
    if [[ -d "venv" ]]; then
        echo -e "${BLUE}🐍 Activando entorno virtual...${NC}"
        source venv/bin/activate
        if [[ "$VIRTUAL_ENV" != "" ]]; then
            echo -e "${GREEN}✅ Entorno virtual activado: $(basename $VIRTUAL_ENV)${NC}"
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

# 1. VERIFICAR ENTORNO VIRTUAL
echo -e "${BLUE}1. 🐍 Verificando entorno virtual...${NC}"
if activate_venv; then
    echo -e "${GREEN}✅ Entorno virtual funcionando${NC}"
    echo "   Python: $(python --version)"
    echo "   Pip: $(pip --version)"
    echo "   Ubicación: $VIRTUAL_ENV"
else
    echo -e "${RED}❌ Problema con entorno virtual${NC}"
fi
echo ""

# 2. VERIFICAR DEPENDENCIAS PYTHON
echo -e "${BLUE}2. 📦 Verificando dependencias Python...${NC}"
dependencies=("scrapy" "pandas" "psycopg2" "requests")
for dep in "${dependencies[@]}"; do
    if python -c "import $dep" 2>/dev/null; then
        version=$(python -c "import $dep; print($dep.__version__)" 2>/dev/null || echo "N/A")
        echo -e "${GREEN}✅ $dep: $version${NC}"
    else
        echo -e "${RED}❌ $dep: No instalado${NC}"
    fi
done
echo ""

# 3. VERIFICAR POSTGRESQL LOCAL
echo -e "${BLUE}3. 🐘 Verificando PostgreSQL local...${NC}"
export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"
if command -v psql &> /dev/null; then
    echo -e "${GREEN}✅ PostgreSQL instalado: $(psql --version)${NC}"
    
    # Verificar si está ejecutándose
    if brew services list | grep postgresql@15 | grep started &> /dev/null; then
        echo -e "${GREEN}✅ PostgreSQL está ejecutándose${NC}"
        
        # Verificar conexión a la base de datos
        if psql -U imdb_user -d imdb_scraper_db -c "SELECT 1;" &> /dev/null; then
            echo -e "${GREEN}✅ Conexión a base de datos: OK${NC}"
            
            # Verificar tablas
            table_count=$(psql -U imdb_user -d imdb_scraper_db -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" 2>/dev/null | xargs)
            echo -e "${GREEN}✅ Tablas en BD: $table_count${NC}"
        else
            echo -e "${RED}❌ No se puede conectar a la base de datos${NC}"
        fi
    else
        echo -e "${YELLOW}⚠️  PostgreSQL no está ejecutándose${NC}"
        echo -e "${BLUE}   Iniciando PostgreSQL...${NC}"
        brew services start postgresql@15
    fi
else
    echo -e "${RED}❌ PostgreSQL no está instalado${NC}"
fi
echo ""

# 4. VERIFICAR DOCKER
echo -e "${BLUE}4. 🐳 Verificando Docker...${NC}"
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✅ Docker instalado: $(docker --version)${NC}"
    
    if docker system info &> /dev/null; then
        echo -e "${GREEN}✅ Docker está ejecutándose${NC}"
    else
        echo -e "${RED}❌ Docker no está ejecutándose${NC}"
    fi
else
    echo -e "${RED}❌ Docker no está instalado${NC}"
fi
echo ""

# 5. VERIFICAR ESTRUCTURA DEL PROYECTO
echo -e "${BLUE}5. 📁 Verificando estructura del proyecto...${NC}"
required_dirs=("config" "data/exports" "docs" "imdb_scraper" "tools" "logs")
for dir in "${required_dirs[@]}"; do
    if [[ -d "$dir" ]]; then
        echo -e "${GREEN}✅ $dir/${NC}"
    else
        echo -e "${RED}❌ $dir/${NC}"
    fi
done

required_files=("run.sh" "config/requirements.txt" "config/database/schema.sql")
for file in "${required_files[@]}"; do
    if [[ -f "$file" ]]; then
        echo -e "${GREEN}✅ $file${NC}"
    else
        echo -e "${RED}❌ $file${NC}"
    fi
done
echo ""

# 6. VERIFICAR ARCHIVOS GENERADOS
echo -e "${BLUE}6. 📄 Verificando archivos generados...${NC}"
if [[ -f "data/exports/peliculas.csv" ]]; then
    lines=$(wc -l < data/exports/peliculas.csv)
    echo -e "${GREEN}✅ peliculas.csv: $lines líneas${NC}"
else
    echo -e "${YELLOW}⚠️  peliculas.csv: No encontrado${NC}"
fi

if [[ -f "data/exports/peliculas.db" ]]; then
    size=$(ls -lh data/exports/peliculas.db | awk '{print $5}')
    echo -e "${GREEN}✅ peliculas.db: $size${NC}"
else
    echo -e "${YELLOW}⚠️  peliculas.db: No encontrado${NC}"
fi

if [[ -f "logs/scrapy.log" ]]; then
    size=$(ls -lh logs/scrapy.log | awk '{print $5}')
    echo -e "${GREEN}✅ scrapy.log: $size${NC}"
else
    echo -e "${YELLOW}⚠️  scrapy.log: No encontrado${NC}"
fi
echo ""

# 7. PRUEBA DE CONEXIÓN PYTHON-POSTGRESQL
echo -e "${BLUE}7. 🔗 Probando conexión Python-PostgreSQL...${NC}"
python3 << 'EOF'
try:
    import psycopg2
    conn = psycopg2.connect(
        host='localhost',
        port='5432',
        database='imdb_scraper_db',
        user='imdb_user',
        password='imdb_secure_2024'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"✅ Conexión exitosa: {version[0][:50]}...")
    
    # Verificar tablas
    cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
    tables = cursor.fetchall()
    print(f"✅ Tablas disponibles: {len(tables)}")
    for table in tables:
        print(f"   - {table[0]}")
    
    conn.close()
except Exception as e:
    print(f"❌ Error de conexión: {e}")
EOF
echo ""

# 8. RESUMEN Y RECOMENDACIONES
echo -e "${BLUE}8. 📋 Resumen y recomendaciones...${NC}"
echo ""

# Verificar qué está funcionando
working_components=0
total_components=4

if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo -e "${GREEN}✅ Entorno virtual activado${NC}"
    ((working_components++))
else
    echo -e "${RED}❌ Entorno virtual no activado${NC}"
fi

if python -c "import scrapy" 2>/dev/null; then
    echo -e "${GREEN}✅ Scrapy disponible${NC}"
    ((working_components++))
else
    echo -e "${RED}❌ Scrapy no disponible${NC}"
fi

if brew services list | grep postgresql@15 | grep started &> /dev/null; then
    echo -e "${GREEN}✅ PostgreSQL ejecutándose${NC}"
    ((working_components++))
else
    echo -e "${RED}❌ PostgreSQL no ejecutándose${NC}"
fi

if psql -U imdb_user -d imdb_scraper_db -c "SELECT 1;" &> /dev/null; then
    echo -e "${GREEN}✅ Base de datos accesible${NC}"
    ((working_components++))
else
    echo -e "${RED}❌ Base de datos no accesible${NC}"
fi

echo ""
echo -e "${BLUE}Estado general: $working_components/$total_components componentes funcionando${NC}"

if [[ $working_components -eq $total_components ]]; then
    echo -e "${GREEN}🎉 ¡Todo está funcionando correctamente!${NC}"
    echo ""
    echo -e "${BLUE}Comandos disponibles:${NC}"
    echo "• ./run.sh - Menú principal"
    echo "• source venv/bin/activate - Activar entorno virtual manualmente"
    echo "• psql -U imdb_user -d imdb_scraper_db - Conectar a PostgreSQL"
else
    echo -e "${YELLOW}⚠️  Algunos componentes necesitan atención${NC}"
    echo ""
    echo -e "${BLUE}Pasos recomendados:${NC}"
    if [[ "$VIRTUAL_ENV" == "" ]]; then
        echo "1. Activar entorno virtual: source venv/bin/activate"
    fi
    if ! python -c "import scrapy" 2>/dev/null; then
        echo "2. Instalar dependencias: pip install -r config/requirements.txt"
    fi
    if ! brew services list | grep postgresql@15 | grep started &> /dev/null; then
        echo "3. Iniciar PostgreSQL: brew services start postgresql@15"
    fi
    if ! psql -U imdb_user -d imdb_scraper_db -c "SELECT 1;" &> /dev/null; then
        echo "4. Configurar base de datos: ./setup_postgres_local.sh"
    fi
fi

echo ""
echo -e "${BLUE}Para obtener ayuda adicional, revisa: docs/ o README.md${NC}"
