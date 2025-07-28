#!/bin/bash
# Script para configurar y probar el sistema de proxies y VPN

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🌐 Configuración de Proxies y Control de Red${NC}"
echo "=============================================="
echo ""

# Función para verificar dependencias
check_dependencies() {
    echo -e "${BLUE}🔍 Verificando dependencias...${NC}"
    
    # Verificar Docker
    if command -v docker &> /dev/null; then
        echo -e "${GREEN}✅ Docker instalado${NC}"
    else
        echo -e "${RED}❌ Docker no encontrado${NC}"
        echo "Instalar desde: https://docs.docker.com/get-docker/"
        return 1
    fi
    
    # Verificar Docker Compose
    if command -v docker-compose &> /dev/null; then
        echo -e "${GREEN}✅ Docker Compose instalado${NC}"
    else
        echo -e "${RED}❌ Docker Compose no encontrado${NC}"
        return 1
    fi
    
    # Verificar TOR (opcional)
    if command -v tor &> /dev/null; then
        echo -e "${GREEN}✅ TOR instalado localmente${NC}"
    else
        echo -e "${YELLOW}⚠️  TOR no instalado localmente (se usará Docker)${NC}"
    fi
    
    return 0
}

# Función para instalar TOR localmente
install_tor() {
    echo -e "${BLUE}🧅 Instalando TOR...${NC}"
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install tor
        else
            echo -e "${RED}❌ Homebrew requerido para instalar TOR en macOS${NC}"
            return 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y tor
        elif command -v yum &> /dev/null; then
            sudo yum install -y tor
        else
            echo -e "${RED}❌ Gestor de paquetes no soportado${NC}"
            return 1
        fi
    else
        echo -e "${YELLOW}⚠️  Sistema no soportado para instalación automática${NC}"
        return 1
    fi
    
    echo -e "${GREEN}✅ TOR instalado${NC}"
    return 0
}

# Función para configurar TOR
configure_tor() {
    echo -e "${BLUE}🔧 Configurando TOR...${NC}"
    
    # Crear directorio de configuración
    mkdir -p config/tor
    
    # Crear archivo de configuración TOR
    cat > config/tor/torrc << EOF
# Configuración TOR para IMDb Scraper
SocksPort 9050
ControlPort 9051
HashedControlPassword 16:872860B76453A77D60CA2BB8C1A7042072093276A3D701AD684053EC4C
CookieAuthentication 1
DataDirectory /var/lib/tor

# Rotación automática de circuitos
MaxCircuitDirtiness 30
NewCircuitPeriod 15
MaxClientCircuitsPending 32

# Configuración de salida
ExitPolicy accept *:80
ExitPolicy accept *:443
ExitPolicy reject *:*

# Logging
Log notice file /var/log/tor/notices.log
EOF
    
    echo -e "${GREEN}✅ Configuración TOR creada${NC}"
}

# Función para iniciar TOR local
start_tor_local() {
    echo -e "${BLUE}🧅 Iniciando TOR local...${NC}"
    
    # Verificar si TOR ya está ejecutándose
    if pgrep -x "tor" > /dev/null; then
        echo -e "${YELLOW}⚠️  TOR ya está ejecutándose${NC}"
        return 0
    fi
    
    # Iniciar TOR
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew services start tor
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        sudo systemctl start tor
        sudo systemctl enable tor
    fi
    
    # Esperar a que TOR se inicie
    echo -e "${BLUE}⏳ Esperando a que TOR se inicie...${NC}"
    sleep 10
    
    # Verificar conexión
    if curl --socks5 127.0.0.1:9050 --max-time 10 -s https://check.torproject.org/api/ip > /dev/null; then
        echo -e "${GREEN}✅ TOR funcionando correctamente${NC}"
        return 0
    else
        echo -e "${RED}❌ Error iniciando TOR${NC}"
        return 1
    fi
}

# Función para probar proxies
test_proxies() {
    echo -e "${BLUE}🧪 Probando sistema de proxies...${NC}"
    
    # Activar entorno virtual
    source venv/bin/activate 2>/dev/null || {
        echo -e "${RED}❌ Entorno virtual no encontrado${NC}"
        return 1
    }
    
    # Ejecutar test de proxies
    python3 << 'EOF'
import sys
sys.path.append('imdb_scraper')

from proxy_manager import ProxyRotator
import requests

def test_direct_connection():
    """Probar conexión directa"""
    try:
        response = requests.get('https://httpbin.org/ip', timeout=10)
        if response.status_code == 200:
            ip = response.json().get('ip')
            print(f"✅ Conexión directa: IP {ip}")
            return ip
    except Exception as e:
        print(f"❌ Error conexión directa: {e}")
    return None

def test_tor_connection():
    """Probar conexión TOR"""
    try:
        proxies = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050'
        }
        response = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=15)
        if response.status_code == 200:
            ip = response.json().get('ip')
            print(f"✅ Conexión TOR: IP {ip}")
            return ip
    except Exception as e:
        print(f"❌ Error conexión TOR: {e}")
    return None

# Ejecutar pruebas
print("🔍 Probando conexiones...")
direct_ip = test_direct_connection()
tor_ip = test_tor_connection()

if direct_ip and tor_ip and direct_ip != tor_ip:
    print(f"🎉 ¡Rotación de IP exitosa!")
    print(f"   Directa: {direct_ip}")
    print(f"   TOR:     {tor_ip}")
else:
    print("⚠️  Las IPs no cambiaron o hubo errores")

# Probar gestor de proxies
proxy_manager = ProxyRotator()
stats = proxy_manager.get_stats()
print(f"\n📊 Estadísticas del gestor:")
print(f"   Proxies totales: {stats['total_proxies']}")
print(f"   Proxies activos: {stats['active_proxies']}")
EOF
}

# Función para configurar VPN con Docker
setup_vpn_docker() {
    echo -e "${BLUE}🐳 Configurando VPN con Docker...${NC}"
    
    # Verificar archivo de configuración VPN
    if [[ ! -f "config/docker/docker-compose-vpn.yml" ]]; then
        echo -e "${RED}❌ Archivo docker-compose-vpn.yml no encontrado${NC}"
        return 1
    fi
    
    # Crear archivo .env para credenciales VPN
    if [[ ! -f ".env" ]]; then
        echo -e "${YELLOW}⚠️  Creando archivo .env para credenciales VPN${NC}"
        cat > .env << EOF
# Credenciales VPN (actualizar con datos reales)
VPN_USER=your_vpn_username
VPN_PASSWORD=your_vpn_password

# Para SurfShark, ExpressVPN, etc.
# VPN_USER=tu_usuario_vpn
# VPN_PASSWORD=tu_password_vpn
EOF
        echo -e "${BLUE}📝 Edita el archivo .env con tus credenciales VPN reales${NC}"
    fi
    
    # Iniciar servicios VPN
    echo -e "${BLUE}🚀 Iniciando servicios VPN y TOR...${NC}"
    cd config/docker
    docker-compose -f docker-compose-vpn.yml up -d
    cd ../..
    
    # Esperar a que los servicios se inicien
    echo -e "${BLUE}⏳ Esperando a que los servicios se inicien...${NC}"
    sleep 30
    
    # Verificar health checks
    echo -e "${BLUE}🔍 Verificando servicios...${NC}"
    
    vpn_health=$(docker inspect --format='{{.State.Health.Status}}' imdb_scraper_vpn 2>/dev/null || echo "unknown")
    echo -e "VPN Health: $vpn_health"
    
    if [[ "$vpn_health" == "healthy" ]]; then
        echo -e "${GREEN}✅ VPN funcionando correctamente${NC}"
    else
        echo -e "${YELLOW}⚠️  VPN no está completamente listo${NC}"
    fi
    
    # Mostrar logs de servicios
    echo -e "${BLUE}📋 Logs de servicios:${NC}"
    docker-compose -f config/docker/docker-compose-vpn.yml logs --tail=20
}

# Función para demostrar cambio de IP
demonstrate_ip_rotation() {
    echo -e "${BLUE}🎭 Demostración de rotación de IP${NC}"
    echo "=================================="
    
    echo -e "${BLUE}📊 Probando diferentes métodos de conexión:${NC}"
    
    # IP directa
    echo -e "\n1️⃣ ${YELLOW}Conexión directa:${NC}"
    direct_ip=$(curl -s --max-time 10 https://httpbin.org/ip | grep -o '"[0-9.]*"' | tr -d '"' || echo "Error")
    echo "   IP: $direct_ip"
    
    # IP por TOR local (si está disponible)
    echo -e "\n2️⃣ ${YELLOW}TOR local (SOCKS5):${NC}"
    tor_ip=$(curl -s --max-time 15 --socks5 127.0.0.1:9050 https://httpbin.org/ip | grep -o '"[0-9.]*"' | tr -d '"' || echo "Error")
    echo "   IP: $tor_ip"
    
    # IP por VPN Docker (si está disponible)
    echo -e "\n3️⃣ ${YELLOW}VPN Docker (HTTP proxy):${NC}"
    vpn_ip=$(curl -s --max-time 15 --proxy http://127.0.0.1:8888 https://httpbin.org/ip | grep -o '"[0-9.]*"' | tr -d '"' 2>/dev/null || echo "Error/No disponible")
    echo "   IP: $vpn_ip"
    
    # Resumen
    echo -e "\n📊 ${BLUE}Resumen de IPs obtenidas:${NC}"
    echo "   Directa: $direct_ip"
    echo "   TOR:     $tor_ip"
    echo "   VPN:     $vpn_ip"
    
    # Verificar si hubo rotación
    unique_ips=($(echo "$direct_ip $tor_ip $vpn_ip" | tr ' ' '\n' | grep -v "Error" | sort -u))
    echo -e "\n🎯 ${GREEN}IPs únicas obtenidas: ${#unique_ips[@]}${NC}"
    
    if [[ ${#unique_ips[@]} -gt 1 ]]; then
        echo -e "${GREEN}🎉 ¡Rotación de IP exitosa!${NC}"
    else
        echo -e "${YELLOW}⚠️  No se detectó rotación de IP${NC}"
    fi
}

# Función para ejecutar scraper con proxies
run_scraper_with_proxies() {
    echo -e "${BLUE}🕷️ Ejecutando scraper con rotación de proxies...${NC}"
    
    # Activar entorno virtual
    source venv/bin/activate
    
    # Configurar settings de Scrapy para usar proxies
    cd imdb_scraper
    
    # Ejecutar con configuración de proxies
    scrapy crawl top_movies \
        -s PROXY_ROTATION_ENABLED=True \
        -s TOR_ROTATION_ENABLED=True \
        -s DOWNLOAD_DELAY=3 \
        -s RANDOMIZE_DOWNLOAD_DELAY=1 \
        -s CONCURRENT_REQUESTS=1 \
        -L INFO
    
    cd ..
    
    # Mostrar estadísticas de proxy
    echo -e "\n${BLUE}📊 Estadísticas de proxy:${NC}"
    if [[ -f "logs/proxy_stats.json" ]]; then
        python3 -c "
import json
with open('logs/proxy_stats.json', 'r') as f:
    stats = json.load(f)
print(f'Total requests: {stats[\"total_requests\"]}')
print(f'IPs únicas: {stats[\"unique_ips_used\"]}')
print(f'Proxies activos: {stats[\"active_proxies\"]}/{stats[\"total_proxies\"]}')
"
    fi
    
    # Mostrar logs de proxy
    echo -e "\n${BLUE}📋 Últimos logs de proxy:${NC}"
    tail -20 logs/proxy_manager.log 2>/dev/null || echo "No hay logs de proxy disponibles"
}

# Función principal del menú
main_menu() {
    while true; do
        echo ""
        echo -e "${BLUE}🌐 Menú de Configuración de Proxies y Red${NC}"
        echo "=========================================="
        echo "1. 🔍 Verificar dependencias"
        echo "2. 🧅 Instalar y configurar TOR local"
        echo "3. 🐳 Configurar VPN con Docker"
        echo "4. 🧪 Probar sistema de proxies"
        echo "5. 🎭 Demostrar rotación de IP"
        echo "6. 🕷️ Ejecutar scraper con proxies"
        echo "7. 📊 Ver estadísticas"
        echo "8. 🚪 Salir"
        echo ""
        read -p "Selecciona una opción (1-8): " choice
        
        case $choice in
            1)
                check_dependencies
                ;;
            2)
                install_tor && configure_tor && start_tor_local
                ;;
            3)
                setup_vpn_docker
                ;;
            4)
                test_proxies
                ;;
            5)
                demonstrate_ip_rotation
                ;;
            6)
                run_scraper_with_proxies
                ;;
            7)
                echo -e "${BLUE}📊 Estadísticas de proxy:${NC}"
                cat logs/proxy_stats.json 2>/dev/null | python3 -m json.tool || echo "No hay estadísticas disponibles"
                ;;
            8)
                echo -e "${GREEN}👋 ¡Hasta luego!${NC}"
                break
                ;;
            *)
                echo -e "${RED}❌ Opción inválida${NC}"
                ;;
        esac
        
        echo ""
        read -p "Presiona Enter para continuar..."
    done
}

# Verificar si se ejecuta con argumentos
if [[ $# -eq 0 ]]; then
    # Sin argumentos - mostrar menú
    main_menu
else
    # Con argumentos - ejecutar función específica
    case $1 in
        "test")
            check_dependencies && test_proxies
            ;;
        "setup")
            check_dependencies && install_tor && configure_tor && start_tor_local
            ;;
        "demo")
            demonstrate_ip_rotation
            ;;
        "scrape")
            run_scraper_with_proxies
            ;;
        *)
            echo "Uso: $0 [test|setup|demo|scrape]"
            echo "Sin argumentos para mostrar menú interactivo"
            ;;
    esac
fi
