#!/bin/bash
# Script universal para activar entorno virtual venv

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Función para activar entorno virtual
activate_venv() {
    local current_dir=$(pwd)
    
    # Buscar el entorno virtual en el directorio actual o padre
    if [[ -d "venv" ]]; then
        VENV_PATH="venv"
    elif [[ -d "../venv" ]]; then
        VENV_PATH="../venv"
    elif [[ -d "../../venv" ]]; then
        VENV_PATH="../../venv"
    else
        echo -e "${RED}❌ Entorno virtual 'venv' no encontrado${NC}"
        echo -e "${BLUE}Creando entorno virtual...${NC}"
        python3 -m venv venv
        VENV_PATH="venv"
    fi
    
    echo -e "${BLUE}🐍 Activando entorno virtual desde: $VENV_PATH${NC}"
    source "$VENV_PATH/bin/activate"
    
    if [[ "$VIRTUAL_ENV" != "" ]]; then
        echo -e "${GREEN}✅ Entorno virtual activado: $(basename $VIRTUAL_ENV)${NC}"
        echo -e "${BLUE}📍 Python: $(which python3)${NC}"
        
        # Verificar dependencias principales
        if ! python3 -c "import scrapy" &> /dev/null; then
            echo -e "${YELLOW}⚠️  Instalando dependencias...${NC}"
            if [[ -f "config/requirements.txt" ]]; then
                pip install -r config/requirements.txt
            elif [[ -f "../config/requirements.txt" ]]; then
                pip install -r ../config/requirements.txt
            elif [[ -f "requirements.txt" ]]; then
                pip install -r requirements.txt
            fi
        fi
        
        return 0
    else
        echo -e "${RED}❌ Error activando entorno virtual${NC}"
        return 1
    fi
}

# Exportar la función para que otros scripts puedan usarla
export -f activate_venv

# Si el script se ejecuta directamente (no siendo importado)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    activate_venv
    echo ""
    echo -e "${GREEN}🎉 Entorno virtual activado exitosamente${NC}"
    echo -e "${BLUE}Para mantener el entorno activo, ejecuta:${NC}"
    echo "source venv/bin/activate"
    echo ""
    echo -e "${BLUE}Para verificar el estado:${NC}"
    echo "echo \$VIRTUAL_ENV"
    echo "which python3"
fi
