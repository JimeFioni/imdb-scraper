#!/bin/bash
# Script para instalar y configurar Docker + PostgreSQL en macOS

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🐳 Configurando Docker y PostgreSQL para IMDb Scraper${NC}"
echo "========================================================"
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

# Función para verificar si Docker está instalado
check_docker() {
    if command -v docker &> /dev/null; then
        echo -e "${GREEN}✅ Docker ya está instalado${NC}"
        docker --version
        return 0
    else
        echo -e "${YELLOW}⚠️  Docker no está instalado${NC}"
        return 1
    fi
}

# Función para verificar si Homebrew está instalado
check_brew() {
    if command -v brew &> /dev/null; then
        echo -e "${GREEN}✅ Homebrew está disponible${NC}"
        return 0
    else
        echo -e "${RED}❌ Homebrew no está instalado${NC}"
        echo -e "${BLUE}🍺 Instalando Homebrew...${NC}"
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        return $?
    fi
}

# Función para instalar Docker Desktop
install_docker() {
    echo -e "${BLUE}🐳 Instalando Docker Desktop...${NC}"
    
    # Verificar Homebrew
    if ! check_brew; then
        echo -e "${RED}❌ Error instalando Homebrew${NC}"
        return 1
    fi
    
    # Instalar Docker Desktop usando Homebrew
    echo -e "${BLUE}📦 Instalando Docker Desktop via Homebrew...${NC}"
    brew install --cask docker
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Docker Desktop instalado exitosamente${NC}"
        echo -e "${YELLOW}⚠️  IMPORTANTE: Necesitas abrir Docker Desktop manualmente la primera vez${NC}"
        echo -e "${BLUE}   1. Abre Applications/Docker.app${NC}"
        echo -e "${BLUE}   2. Acepta los términos y condiciones${NC}"
        echo -e "${BLUE}   3. Espera a que Docker se inicie completamente${NC}"
        echo ""
        
        # Intentar abrir Docker Desktop automáticamente
        echo -e "${BLUE}🚀 Abriendo Docker Desktop...${NC}"
        open /Applications/Docker.app
        
        echo -e "${YELLOW}Esperando a que Docker se inicie... (esto puede tomar unos minutos)${NC}"
        
        # Esperar a que Docker esté listo
        local counter=0
        while ! docker system info &> /dev/null && [ $counter -lt 60 ]; do
            echo -n "."
            sleep 5
            ((counter++))
        done
        echo ""
        
        if docker system info &> /dev/null; then
            echo -e "${GREEN}✅ Docker está funcionando correctamente${NC}"
            return 0
        else
            echo -e "${YELLOW}⚠️  Docker puede necesitar más tiempo para iniciarse${NC}"
            echo -e "${BLUE}   Por favor, verifica que Docker Desktop esté ejecutándose${NC}"
            return 1
        fi
    else
        echo -e "${RED}❌ Error instalando Docker Desktop${NC}"
        return 1
    fi
}

# Función para configurar PostgreSQL
setup_postgresql() {
    echo -e "${BLUE}🐘 Configurando PostgreSQL con Docker...${NC}"
    
    # Verificar que estamos en el directorio correcto
    if [[ ! -f "docker-compose.yml" ]]; then
        if [[ -f "config/docker/docker-compose.yml" ]]; then
            cd config/docker
        else
            echo -e "${RED}❌ No se encontró docker-compose.yml${NC}"
            return 1
        fi
    fi
    
    # Detener contenedores anteriores si existen
    echo -e "${BLUE}🛑 Deteniendo contenedores anteriores...${NC}"
    docker-compose down -v &> /dev/null
    
    # Iniciar PostgreSQL
    echo -e "${BLUE}🚀 Iniciando PostgreSQL...${NC}"
    docker-compose up -d
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ PostgreSQL iniciado correctamente${NC}"
        
        # Esperar a que PostgreSQL esté listo
        echo -e "${BLUE}⏳ Esperando a que PostgreSQL esté listo...${NC}"
        sleep 10
        
        # Verificar conexión
        if docker-compose exec -T postgres pg_isready -U imdb_user -d imdb_scraper_db &> /dev/null; then
            echo -e "${GREEN}✅ PostgreSQL está listo para recibir conexiones${NC}"
            echo ""
            echo -e "${BLUE}📊 Información de conexión:${NC}"
            echo "   Host: localhost"
            echo "   Puerto: 5432"
            echo "   Base de datos: imdb_scraper_db"
            echo "   Usuario: imdb_user"
            echo "   Contraseña: imdb_secure_2024"
            echo ""
            echo -e "${BLUE}🌐 pgAdmin disponible en: http://localhost:8080${NC}"
            echo "   Email: admin@imdb-scraper.local"
            echo "   Contraseña: admin123"
            return 0
        else
            echo -e "${YELLOW}⚠️  PostgreSQL aún se está iniciando...${NC}"
            return 1
        fi
    else
        echo -e "${RED}❌ Error iniciando PostgreSQL${NC}"
        return 1
    fi
}

# Función para probar la configuración
test_setup() {
    echo -e "${BLUE}🧪 Probando configuración...${NC}"
    
    # Probar Docker
    if docker --version &> /dev/null; then
        echo -e "${GREEN}✅ Docker: OK${NC}"
    else
        echo -e "${RED}❌ Docker: Error${NC}"
        return 1
    fi
    
    # Probar Docker Compose
    if docker-compose --version &> /dev/null; then
        echo -e "${GREEN}✅ Docker Compose: OK${NC}"
    else
        echo -e "${RED}❌ Docker Compose: Error${NC}"
        return 1
    fi
    
    # Probar PostgreSQL
    cd ../../  # Volver al directorio raíz
    if docker-compose -f config/docker/docker-compose.yml exec -T postgres pg_isready -U imdb_user -d imdb_scraper_db &> /dev/null; then
        echo -e "${GREEN}✅ PostgreSQL: OK${NC}"
        
        # Probar conexión desde Python
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
    print('✅ Conexión Python a PostgreSQL: OK')
    conn.close()
except Exception as e:
    print(f'❌ Conexión Python a PostgreSQL: {e}')
"
    else
        echo -e "${RED}❌ PostgreSQL: Error${NC}"
        return 1
    fi
    
    echo ""
    echo -e "${GREEN}🎉 ¡Configuración completada exitosamente!${NC}"
    return 0
}

# Función principal
main() {
    echo -e "${BLUE}Verificando estado actual...${NC}"
    
    # Verificar Docker
    if ! check_docker; then
        echo ""
        read -p "¿Deseas instalar Docker Desktop? (y/N): " install_choice
        if [[ $install_choice =~ ^[Yy]$ ]]; then
            if ! install_docker; then
                echo -e "${RED}❌ Error instalando Docker${NC}"
                exit 1
            fi
        else
            echo -e "${YELLOW}⚠️  Docker es necesario para PostgreSQL${NC}"
            exit 1
        fi
    fi
    
    echo ""
    echo -e "${BLUE}🐘 ¿Configurar PostgreSQL?${NC}"
    read -p "¿Iniciar PostgreSQL con Docker? (y/N): " postgres_choice
    if [[ $postgres_choice =~ ^[Yy]$ ]]; then
        if ! setup_postgresql; then
            echo -e "${YELLOW}⚠️  PostgreSQL puede necesitar más tiempo para iniciarse${NC}"
        fi
    fi
    
    echo ""
    echo -e "${BLUE}🧪 ¿Ejecutar pruebas de configuración?${NC}"
    read -p "¿Probar la configuración? (y/N): " test_choice
    if [[ $test_choice =~ ^[Yy]$ ]]; then
        test_setup
    fi
    
    echo ""
    echo -e "${BLUE}📋 Próximos pasos:${NC}"
    echo "1. Ejecuta: ./run.sh (opción 2) para usar PostgreSQL"
    echo "2. Visita: http://localhost:8080 para pgAdmin"
    echo "3. Ejecuta: docker-compose -f config/docker/docker-compose.yml logs para ver logs"
    echo "4. Ejecuta: docker-compose -f config/docker/docker-compose.yml down para detener"
}

# Ejecutar función principal
main
