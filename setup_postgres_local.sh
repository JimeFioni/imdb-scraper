#!/bin/bash
# Script para configurar PostgreSQL local (sin Docker)

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🐘 Configuración PostgreSQL Local (sin Docker)${NC}"
echo "=================================================="
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

# Activar entorno virtual al inicio
if ! activate_venv; then
    echo -e "${RED}❌ No se pudo activar el entorno virtual${NC}"
    exit 1
fi

# Verificar si PostgreSQL está instalado
check_postgres() {
    if command -v psql &> /dev/null; then
        echo -e "${GREEN}✅ PostgreSQL está instalado${NC}"
        psql --version
        return 0
    else
        echo -e "${YELLOW}⚠️  PostgreSQL no está instalado${NC}"
        return 1
    fi
}

# Instalar PostgreSQL con Homebrew
install_postgres() {
    echo -e "${BLUE}📦 Instalando PostgreSQL con Homebrew...${NC}"
    
    if ! command -v brew &> /dev/null; then
        echo -e "${RED}❌ Homebrew no está instalado${NC}"
        echo -e "${BLUE}Instalando Homebrew...${NC}"
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    brew install postgresql@15
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ PostgreSQL instalado correctamente${NC}"
        
        # Iniciar PostgreSQL
        brew services start postgresql@15
        
        # Agregar al PATH
        echo 'export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"' >> ~/.zshrc
        export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"
        
        return 0
    else
        echo -e "${RED}❌ Error instalando PostgreSQL${NC}"
        return 1
    fi
}

# Configurar base de datos
setup_database() {
    echo -e "${BLUE}🗄️  Configurando base de datos...${NC}"
    
    # Crear usuario y base de datos
    createuser -s imdb_user 2>/dev/null || echo "Usuario ya existe"
    createdb -O imdb_user imdb_scraper_db 2>/dev/null || echo "Base de datos ya existe"
    
    # Establecer contraseña
    psql -c "ALTER USER imdb_user WITH PASSWORD 'imdb_secure_2024';" 2>/dev/null
    
    # Ejecutar esquema
    if [[ -f "config/database/schema.sql" ]]; then
        echo -e "${BLUE}📊 Ejecutando esquema SQL...${NC}"
        psql -U imdb_user -d imdb_scraper_db -f config/database/schema.sql
        
        if [[ -f "config/database/initial_data.sql" ]]; then
            echo -e "${BLUE}📝 Insertando datos iniciales...${NC}"
            psql -U imdb_user -d imdb_scraper_db -f config/database/initial_data.sql
        fi
    fi
    
    echo -e "${GREEN}✅ Base de datos configurada${NC}"
}

# Probar conexión
test_connection() {
    echo -e "${BLUE}🧪 Probando conexión...${NC}"
    
    if psql -U imdb_user -d imdb_scraper_db -c "SELECT version();" &> /dev/null; then
        echo -e "${GREEN}✅ Conexión PostgreSQL: OK${NC}"
        
        # Probar desde Python
        source venv/bin/activate
        python3 -c "
import psycopg2
try:
    conn = psycopg2.connect(
        host='localhost',
        port='5432',
        database='imdb_scraper_db',
        user='imdb_user',
        password='imdb_secure_2024'
    )
    print('✅ Conexión Python-PostgreSQL: OK')
    conn.close()
except Exception as e:
    print(f'❌ Error en conexión Python: {e}')
"
        return 0
    else
        echo -e "${RED}❌ Error en conexión${NC}"
        return 1
    fi
}

# Función principal
main() {
    if ! check_postgres; then
        read -p "¿Instalar PostgreSQL localmente? (y/N): " install_choice
        if [[ $install_choice =~ ^[Yy]$ ]]; then
            if ! install_postgres; then
                exit 1
            fi
        else
            echo -e "${YELLOW}⚠️  PostgreSQL es necesario${NC}"
            exit 1
        fi
    fi
    
    echo ""
    read -p "¿Configurar base de datos? (y/N): " setup_choice
    if [[ $setup_choice =~ ^[Yy]$ ]]; then
        setup_database
        
        echo ""
        read -p "¿Probar conexión? (y/N): " test_choice
        if [[ $test_choice =~ ^[Yy]$ ]]; then
            test_connection
        fi
    fi
    
    echo ""
    echo -e "${BLUE}📊 Información de conexión:${NC}"
    echo "   🏠 Host: localhost"
    echo "   🔌 Puerto: 5432"
    echo "   🗄️  Base de datos: imdb_scraper_db"
    echo "   👤 Usuario: imdb_user"
    echo "   🔑 Contraseña: imdb_secure_2024"
    echo ""
    echo -e "${BLUE}📋 Comandos útiles:${NC}"
    echo "🚀 Iniciar PostgreSQL: brew services start postgresql@15"
    echo "🛑 Detener PostgreSQL: brew services stop postgresql@15"
    echo "🔍 Estado: brew services list | grep postgresql"
    echo "💻 Conectar: psql -U imdb_user -d imdb_scraper_db"
    echo ""
    echo "🎬 Usar con scraper: scrapy crawl top_movies"
}

# Ejecutar
main
