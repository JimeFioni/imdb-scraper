#!/bin/bash

# ===================================================================
# Script de configuración automática para TOR y sistema de proxies
# ===================================================================

echo "🔧 Configurando sistema de proxies y TOR para IMDb Scraper..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir con colores
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[ℹ]${NC} $1"
}

# Detectar sistema operativo
OS=""
case "$(uname -s)" in
    Darwin*) OS="macOS";;
    Linux*)  OS="Linux";;
    *) print_error "Sistema operativo no soportado"; exit 1;;
esac

print_info "Sistema detectado: $OS"

# ===================================================================
# 1. INSTALACIÓN DE TOR
# ===================================================================

echo -e "\n🌐 Configurando TOR Network..."

install_tor() {
    if command -v tor &> /dev/null; then
        print_status "TOR ya está instalado"
        return 0
    fi
    
    print_info "Instalando TOR..."
    
    case $OS in
        "macOS")
            if command -v brew &> /dev/null; then
                brew install tor
            else
                print_error "Homebrew no encontrado. Instala Homebrew primero: https://brew.sh"
                return 1
            fi
            ;;
        "Linux")
            if command -v apt-get &> /dev/null; then
                sudo apt-get update
                sudo apt-get install -y tor
            elif command -v yum &> /dev/null; then
                sudo yum install -y tor
            elif command -v pacman &> /dev/null; then
                sudo pacman -S tor
            else
                print_error "Gestor de paquetes no soportado"
                return 1
            fi
            ;;
    esac
    
    if command -v tor &> /dev/null; then
        print_status "TOR instalado correctamente"
        return 0
    else
        print_error "Error instalando TOR"
        return 1
    fi
}

# ===================================================================
# 2. CONFIGURACIÓN DE TOR
# ===================================================================

configure_tor() {
    print_info "Configurando TOR..."
    
    # Crear directorio de configuración TOR si no existe
    TOR_CONFIG_DIR=""
    case $OS in
        "macOS")
            TOR_CONFIG_DIR="/usr/local/etc/tor"
            ;;
        "Linux")
            TOR_CONFIG_DIR="/etc/tor"
            ;;
    esac
    
    if [ ! -d "$TOR_CONFIG_DIR" ]; then
        print_warning "Directorio de configuración TOR no encontrado: $TOR_CONFIG_DIR"
        print_info "Creando configuración local..."
        
        # Crear configuración local
        mkdir -p "config/tor"
        TOR_CONFIG_FILE="config/tor/torrc"
    else
        TOR_CONFIG_FILE="$TOR_CONFIG_DIR/torrc"
    fi
    
    # Configuración TOR para scraping
    cat > "$TOR_CONFIG_FILE" << EOF
# Configuración TOR para IMDb Scraper
# Puerto SOCKS5
SocksPort 9050
# Puerto de control
ControlPort 9051
# Puerto HTTP (Privoxy)
# HTTPTunnelPort 8118

# Configuración de red
ExitPolicy accept *:80
ExitPolicy accept *:443
ExitPolicy reject *:*

# Configuración para cambio frecuente de identidad
MaxCircuitDirtiness 30
NewCircuitPeriod 30
MaxClientCircuitsPending 48
NumEntryGuards 8

# Logs
Log notice file logs/tor.log

# Configuración de seguridad
DisableDebuggerAttachment 0
EOF
    
    print_status "Configuración TOR creada en: $TOR_CONFIG_FILE"
}

# ===================================================================
# 3. INSTALACIÓN DE PRIVOXY (para HTTP sobre TOR)
# ===================================================================

install_privoxy() {
    print_info "Instalando Privoxy (proxy HTTP para TOR)..."
    
    if command -v privoxy &> /dev/null; then
        print_status "Privoxy ya está instalado"
        return 0
    fi
    
    case $OS in
        "macOS")
            if command -v brew &> /dev/null; then
                brew install privoxy
            else
                print_warning "Sin Homebrew, saltando Privoxy"
                return 1
            fi
            ;;
        "Linux")
            if command -v apt-get &> /dev/null; then
                sudo apt-get install -y privoxy
            elif command -v yum &> /dev/null; then
                sudo yum install -y privoxy
            elif command -v pacman &> /dev/null; then
                sudo pacman -S privoxy
            else
                print_warning "Gestor de paquetes no soportado para Privoxy"
                return 1
            fi
            ;;
    esac
    
    if command -v privoxy &> /dev/null; then
        print_status "Privoxy instalado correctamente"
        configure_privoxy
    else
        print_warning "Privoxy no se pudo instalar"
    fi
}

configure_privoxy() {
    print_info "Configurando Privoxy..."
    
    # Configuración Privoxy
    PRIVOXY_CONFIG=""
    case $OS in
        "macOS")
            PRIVOXY_CONFIG="/usr/local/etc/privoxy/config"
            ;;
        "Linux")
            PRIVOXY_CONFIG="/etc/privoxy/config"
            ;;
    esac
    
    if [ -f "$PRIVOXY_CONFIG" ]; then
        # Backup de configuración original
        sudo cp "$PRIVOXY_CONFIG" "$PRIVOXY_CONFIG.backup"
        
        # Añadir configuración para TOR
        echo "" | sudo tee -a "$PRIVOXY_CONFIG"
        echo "# Configuración para TOR" | sudo tee -a "$PRIVOXY_CONFIG"
        echo "forward-socks5 / 127.0.0.1:9050 ." | sudo tee -a "$PRIVOXY_CONFIG"
        echo "listen-address 127.0.0.1:8118" | sudo tee -a "$PRIVOXY_CONFIG"
        
        print_status "Privoxy configurado para usar TOR"
    else
        print_warning "Archivo de configuración Privoxy no encontrado"
    fi
}

# ===================================================================
# 4. INSTALACIÓN DE DEPENDENCIAS PYTHON
# ===================================================================

install_python_deps() {
    print_info "Instalando dependencias Python para proxies..."
    
    # Crear requirements específico para proxies
    cat > "requirements_proxies.txt" << EOF
requests[socks]>=2.31.0
PySocks>=1.7.1
stem>=1.8.1
fake-useragent>=1.4.0
python-decouple>=3.8
aiohttp>=3.9.0
EOF
    
    # Instalar dependencias
    if command -v pip &> /dev/null; then
        pip install -r requirements_proxies.txt
        print_status "Dependencias Python instaladas"
    else
        print_error "pip no encontrado"
        return 1
    fi
}

# ===================================================================
# 5. CONFIGURACIÓN DE PROXIES PÚBLICOS
# ===================================================================

setup_public_proxies() {
    print_info "Configurando proxies públicos..."
    
    # Actualizar configuración de proxies con proxies públicos reales
    cat > "config/proxies.json" << EOF
{
  "proxies": [
    {
      "host": "proxy1.example.com",
      "port": 8080,
      "protocol": "http",
      "country": "US",
      "provider": "Free Public",
      "status": "testing"
    },
    {
      "host": "proxy2.example.com", 
      "port": 3128,
      "protocol": "http",
      "country": "UK",
      "provider": "Free Public",
      "status": "testing"
    },
    {
      "host": "127.0.0.1",
      "port": 9050,
      "protocol": "socks5",
      "country": "TOR",
      "provider": "TOR Network",
      "status": "active"
    },
    {
      "host": "127.0.0.1",
      "port": 8118,
      "protocol": "http",
      "country": "TOR",
      "provider": "Privoxy + TOR",
      "status": "active"
    }
  ],
  "rotation_config": {
    "strategy": "round_robin",
    "requests_per_proxy": 5,
    "retry_attempts": 3,
    "retry_delay": 5,
    "health_check_interval": 300,
    "ip_change_detection": true,
    "log_ip_changes": true
  },
  "tor_config": {
    "control_port": 9051,
    "socks_port": 9050,
    "http_port": 8118,
    "new_identity_interval": 30,
    "enable_auto_rotation": true
  },
  "vpn_config": {
    "provider": "gluetun",
    "target_countries": ["US", "UK", "CA", "DE"],
    "docker_image": "qmcgaw/gluetun",
    "health_check_url": "https://httpbin.org/ip",
    "connection_timeout": 60
  }
}
EOF
    
    print_status "Configuración de proxies actualizada"
}

# ===================================================================
# 6. CREAR SCRIPTS DE CONTROL
# ===================================================================

create_control_scripts() {
    print_info "Creando scripts de control..."
    
    # Script para iniciar TOR
    cat > "scripts/start_tor.sh" << 'EOF'
#!/bin/bash
echo "🌐 Iniciando TOR..."

# Crear directorio de logs
mkdir -p logs

# Iniciar TOR
if command -v tor &> /dev/null; then
    tor -f config/tor/torrc &
    TOR_PID=$!
    echo $TOR_PID > logs/tor.pid
    echo "✅ TOR iniciado (PID: $TOR_PID)"
    
    # Esperar que TOR esté listo
    sleep 10
    
    # Verificar conexión TOR
    if curl --socks5 127.0.0.1:9050 https://httpbin.org/ip 2>/dev/null; then
        echo "✅ TOR funcionando correctamente"
    else
        echo "❌ Error en conexión TOR"
    fi
else
    echo "❌ TOR no está instalado"
    exit 1
fi
EOF

    # Script para detener TOR
    cat > "scripts/stop_tor.sh" << 'EOF'
#!/bin/bash
echo "🛑 Deteniendo TOR..."

if [ -f "logs/tor.pid" ]; then
    TOR_PID=$(cat logs/tor.pid)
    if kill -0 $TOR_PID 2>/dev/null; then
        kill $TOR_PID
        rm logs/tor.pid
        echo "✅ TOR detenido"
    else
        echo "⚠️ Proceso TOR no encontrado"
    fi
else
    echo "⚠️ Archivo PID no encontrado"
fi

# Detener todos los procesos TOR como fallback
pkill -f "tor" 2>/dev/null || true
EOF

    # Script para rotar identidad TOR
    cat > "scripts/rotate_tor.sh" << 'EOF'
#!/bin/bash
echo "🔄 Rotando identidad TOR..."

# Enviar señal NEWNYM al puerto de control
echo -e 'AUTHENTICATE ""\r\nSIGNAL NEWNYM\r\nQUIT' | nc 127.0.0.1 9051

if [ $? -eq 0 ]; then
    echo "✅ Identidad TOR rotada"
    sleep 5
    
    # Verificar nueva IP
    NEW_IP=$(curl --socks5 127.0.0.1:9050 https://httpbin.org/ip 2>/dev/null | grep -o '"origin":"[^"]*"' | cut -d'"' -f4)
    echo "🌍 Nueva IP TOR: $NEW_IP"
else
    echo "❌ Error rotando identidad TOR"
fi
EOF

    # Hacer scripts ejecutables
    chmod +x scripts/*.sh
    
    print_status "Scripts de control creados en scripts/"
}

# ===================================================================
# 7. FUNCIÓN PRINCIPAL
# ===================================================================

main() {
    echo "🚀 Iniciando configuración completa del sistema de proxies..."
    
    # Crear directorios necesarios
    mkdir -p config/tor
    mkdir -p scripts
    mkdir -p logs
    
    # Ejecutar configuraciones
    install_tor
    configure_tor
    install_privoxy
    install_python_deps
    setup_public_proxies
    create_control_scripts
    
    echo -e "\n🎉 Configuración completada!"
    echo -e "\n📋 Próximos pasos:"
    echo "1. Ejecutar: ./scripts/start_tor.sh"
    echo "2. Probar sistema: python test_proxy_rotation.py"
    echo "3. Ejecutar scraper: scrapy crawl top_movies -s PROXY_ROTATION_ENABLED=True"
    
    echo -e "\n🔧 Comandos útiles:"
    echo "- Iniciar TOR: ./scripts/start_tor.sh"
    echo "- Detener TOR: ./scripts/stop_tor.sh"
    echo "- Rotar TOR: ./scripts/rotate_tor.sh"
    echo "- Probar proxies: python test_proxy_rotation.py"
    
    print_status "Sistema de proxies listo para usar!"
}

# Ejecutar configuración
main "$@"
