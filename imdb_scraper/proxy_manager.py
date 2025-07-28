#!/usr/bin/env python3
"""
Gestor de Proxies Avanzado para IMDb Scraper
Implementa rotación automática, fallback y validación de IPs
"""

import random
import time
import requests
import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import json
import os

@dataclass
class ProxyConfig:
    """Configuración de un proxy individual"""
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    protocol: str = "http"
    country: Optional[str] = None
    provider: Optional[str] = None  # Proveedor del proxy
    last_used: Optional[datetime] = None
    failure_count: int = 0
    max_failures: int = 3
    is_active: bool = True

class ProxyRotator:
    """
    Gestor de rotación de proxies con estrategias avanzadas
    """
    
    def __init__(self, config_file: str = "config/proxies.json"):
        self.config_file = config_file
        self.proxies: List[ProxyConfig] = []
        self.current_proxy_index = 0
        self.request_count = 0
        self.rotation_threshold = 10  # Cambiar proxy cada 10 requests
        self.logger = self._setup_logger()
        self.ip_history: List[Dict] = []
        
        # Cargar configuración de proxies
        self._load_proxy_config()
        
        # Proxies públicos de respaldo (TOR y otros)
        self._setup_fallback_proxies()
    
    def _setup_logger(self) -> logging.Logger:
        """Configurar logger específico para proxies"""
        logger = logging.getLogger('proxy_manager')
        logger.setLevel(logging.INFO)
        
        # Crear handler para archivo
        os.makedirs('logs', exist_ok=True)
        handler = logging.FileHandler('logs/proxy_manager.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def _load_proxy_config(self):
        """Cargar configuración de proxies desde archivo"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config_data = json.load(f)
                    for proxy_data in config_data.get('proxies', []):
                        proxy = ProxyConfig(**proxy_data)
                        self.proxies.append(proxy)
                self.logger.info(f"Cargados {len(self.proxies)} proxies desde configuración")
        except Exception as e:
            self.logger.error(f"Error cargando configuración de proxies: {e}")
    
    def _setup_fallback_proxies(self):
        """Configurar proxies públicos de respaldo"""
        fallback_proxies = [
            # Proxies públicos gratuitos (pueden no estar siempre disponibles)
            ProxyConfig("proxy1.example.com", 8080, protocol="http"),
            ProxyConfig("proxy2.example.com", 3128, protocol="http"),
            ProxyConfig("127.0.0.1", 9050, protocol="socks5"),  # TOR local
            ProxyConfig("127.0.0.1", 8118, protocol="http"),    # Privoxy + TOR
        ]
        
        # Solo agregar si no tenemos proxies configurados
        if not self.proxies:
            self.proxies.extend(fallback_proxies)
            self.logger.info("Usando proxies de respaldo públicos")
    
    def get_current_ip(self, proxy: Optional[ProxyConfig] = None) -> Optional[str]:
        """Obtener la IP actual usando el proxy especificado"""
        try:
            proxy_dict = None
            if proxy:
                proxy_url = self._build_proxy_url(proxy)
                proxy_dict = {
                    'http': proxy_url,
                    'https': proxy_url
                }
            
            # Usar varios servicios para verificar IP
            ip_services = [
                'https://httpbin.org/ip',
                'https://api.ipify.org?format=json',
                'https://jsonip.com',
                'https://ifconfig.me/ip'
            ]
            
            for service in ip_services:
                try:
                    response = requests.get(
                        service, 
                        proxies=proxy_dict, 
                        timeout=10,
                        headers={'User-Agent': 'Mozilla/5.0 (compatible; IP-Checker)'}
                    )
                    
                    if response.status_code == 200:
                        if 'httpbin.org' in service:
                            return response.json().get('origin', '').split(',')[0].strip()
                        elif 'ipify.org' in service:
                            return response.json().get('ip')
                        elif 'jsonip.com' in service:
                            return response.json().get('ip')
                        else:
                            return response.text.strip()
                except:
                    continue
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error obteniendo IP actual: {e}")
            return None
    
    def _build_proxy_url(self, proxy: ProxyConfig) -> str:
        """Construir URL del proxy"""
        auth = ""
        if proxy.username and proxy.password:
            auth = f"{proxy.username}:{proxy.password}@"
        
        return f"{proxy.protocol}://{auth}{proxy.host}:{proxy.port}"
    
    def test_proxy(self, proxy: ProxyConfig) -> bool:
        """Probar si un proxy funciona correctamente"""
        try:
            proxy_url = self._build_proxy_url(proxy)
            proxy_dict = {
                'http': proxy_url,
                'https': proxy_url
            }
            
            # Probar con IMDb específicamente
            test_urls = [
                'https://httpbin.org/ip',
                'https://www.imdb.com/robots.txt'
            ]
            
            for url in test_urls:
                response = requests.get(
                    url,
                    proxies=proxy_dict,
                    timeout=15,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                )
                
                if response.status_code != 200:
                    return False
            
            # Obtener y registrar IP
            current_ip = self.get_current_ip(proxy)
            if current_ip:
                self.logger.info(f"Proxy {proxy.host}:{proxy.port} funciona. IP: {current_ip}")
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error probando proxy {proxy.host}:{proxy.port}: {e}")
            return False
    
    def get_next_proxy(self) -> Optional[ProxyConfig]:
        """Obtener el siguiente proxy en rotación"""
        if not self.proxies:
            return None
        
        # Filtrar proxies activos
        active_proxies = [p for p in self.proxies if p.is_active and p.failure_count < p.max_failures]
        
        if not active_proxies:
            # Reiniciar contadores de fallo si todos han fallado
            for proxy in self.proxies:
                proxy.failure_count = 0
                proxy.is_active = True
            active_proxies = self.proxies
            self.logger.warning("Reiniciando contadores de proxy - todos habían fallado")
        
        # Selección basada en estrategia
        if self.request_count % self.rotation_threshold == 0 or self.current_proxy_index >= len(active_proxies):
            # Rotación automática o reinicio
            self.current_proxy_index = 0
            
            # Ordenar por último uso y fallos
            active_proxies.sort(key=lambda p: (p.failure_count, p.last_used or datetime.min))
        
        proxy = active_proxies[self.current_proxy_index % len(active_proxies)]
        proxy.last_used = datetime.now()
        
        self.current_proxy_index += 1
        self.request_count += 1
        
        return proxy
    
    def mark_proxy_failed(self, proxy: ProxyConfig):
        """Marcar un proxy como fallido"""
        proxy.failure_count += 1
        
        if proxy.failure_count >= proxy.max_failures:
            proxy.is_active = False
            self.logger.warning(f"Proxy {proxy.host}:{proxy.port} desactivado tras {proxy.failure_count} fallos")
        else:
            self.logger.info(f"Proxy {proxy.host}:{proxy.port} falló. Intentos: {proxy.failure_count}/{proxy.max_failures}")
    
    def mark_proxy_success(self, proxy: ProxyConfig, ip_used: str):
        """Marcar un proxy como exitoso y registrar IP"""
        proxy.failure_count = max(0, proxy.failure_count - 1)  # Reducir contador de fallos
        proxy.is_active = True
        
        # Registrar en historial
        self.ip_history.append({
            'timestamp': datetime.now().isoformat(),
            'proxy': f"{proxy.host}:{proxy.port}",
            'ip_used': ip_used,
            'request_count': self.request_count
        })
        
        self.logger.info(f"Request exitoso usando proxy {proxy.host}:{proxy.port}, IP: {ip_used}")
    
    def get_proxy_dict(self, proxy: ProxyConfig) -> Dict[str, str]:
        """Obtener diccionario de proxy para requests"""
        proxy_url = self._build_proxy_url(proxy)
        return {
            'http': proxy_url,
            'https': proxy_url
        }
    
    def get_stats(self) -> Dict:
        """Obtener estadísticas del gestor de proxies"""
        active_count = sum(1 for p in self.proxies if p.is_active)
        total_requests = len(self.ip_history)
        unique_ips = len(set(record['ip_used'] for record in self.ip_history))
        
        return {
            'total_proxies': len(self.proxies),
            'active_proxies': active_count,
            'total_requests': total_requests,
            'unique_ips_used': unique_ips,
            'current_request_count': self.request_count,
            'ip_history': self.ip_history[-10:]  # Últimas 10 IPs usadas
        }
    
    def save_stats(self):
        """Guardar estadísticas a archivo"""
        try:
            os.makedirs('logs', exist_ok=True)
            stats = self.get_stats()
            
            with open('logs/proxy_stats.json', 'w') as f:
                json.dump(stats, f, indent=2)
            
            self.logger.info("Estadísticas de proxy guardadas")
            
        except Exception as e:
            self.logger.error(f"Error guardando estadísticas: {e}")


class VPNManager:
    """
    Gestor de VPN usando Docker con healthcheck
    """
    
    def __init__(self, target_country: str = "US"):
        self.target_country = target_country
        self.logger = logging.getLogger('vpn_manager')
        self.docker_compose_file = "config/docker/docker-compose-vpn.yml"
    
    def setup_vpn_docker(self):
        """Configurar VPN usando Docker"""
        vpn_compose = '''
version: '3.8'

services:
  vpn:
    image: qmcgaw/gluetun
    container_name: imdb_scraper_vpn
    cap_add:
      - NET_ADMIN
    devices:
      - /dev/net/tun:/dev/net/tun
    ports:
      - "8888:8888/tcp" # HTTP proxy
      - "8388:8388/tcp" # Shadowsocks
    volumes:
      - ./vpn-data:/gluetun
    environment:
      # VPN Provider (configurable)
      - VPN_SERVICE_PROVIDER=surfshark
      - VPN_TYPE=openvpn
      - OPENVPN_USER=${VPN_USER}
      - OPENVPN_PASSWORD=${VPN_PASSWORD}
      - SERVER_COUNTRIES=United States
      # Health check
      - HEALTH_SUCCESS_MSG=healthy
      - HEALTH_VPN_DURATION_INITIAL=6s
      - HEALTH_VPN_DURATION_ADDITION=5s
      # HTTP Proxy
      - HTTPPROXY=on
      - HTTPPROXY_LOG=on
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "/gluetun-entrypoint", "healthcheck"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

  vpn-test:
    image: curlimages/curl
    container_name: vpn_test
    depends_on:
      vpn:
        condition: service_healthy
    network_mode: "service:vpn"
    command: |
      sh -c "
        echo 'Testing VPN connection...'
        curl -s https://httpbin.org/ip
        echo 'VPN test completed'
      "
'''
        
        # Crear directorio y archivo
        os.makedirs(os.path.dirname(self.docker_compose_file), exist_ok=True)
        
        with open(self.docker_compose_file, 'w') as f:
            f.write(vpn_compose)
        
        self.logger.info("Configuración VPN Docker creada")
    
    def start_vpn(self) -> bool:
        """Iniciar VPN y verificar conexión"""
        try:
            import subprocess
            
            # Iniciar VPN
            result = subprocess.run([
                'docker-compose', '-f', self.docker_compose_file, 'up', '-d'
            ], capture_output=True, text=True, cwd='config/docker')
            
            if result.returncode != 0:
                self.logger.error(f"Error iniciando VPN: {result.stderr}")
                return False
            
            # Esperar y verificar health check
            time.sleep(30)  # Dar tiempo para la conexión VPN
            
            health_result = subprocess.run([
                'docker', 'inspect', '--format={{.State.Health.Status}}', 'imdb_scraper_vpn'
            ], capture_output=True, text=True)
            
            is_healthy = health_result.stdout.strip() == 'healthy'
            
            if is_healthy:
                self.logger.info("VPN iniciada y saludable")
                return True
            else:
                self.logger.error("VPN iniciada pero no está saludable")
                return False
                
        except Exception as e:
            self.logger.error(f"Error configurando VPN: {e}")
            return False


def create_proxy_config():
    """Crear archivo de configuración de proxies de ejemplo"""
    config = {
        "proxies": [
            {
                "host": "proxy1.example.com",
                "port": 8080,
                "username": "user1",
                "password": "pass1",
                "protocol": "http",
                "country": "US"
            },
            {
                "host": "proxy2.example.com", 
                "port": 3128,
                "username": "user2",
                "password": "pass2",
                "protocol": "http",
                "country": "UK"
            },
            {
                "host": "127.0.0.1",
                "port": 9050,
                "protocol": "socks5",
                "country": "TOR"
            }
        ]
    }
    
    os.makedirs('config', exist_ok=True)
    with open('config/proxies.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("Archivo de configuración de proxies creado en: config/proxies.json")


if __name__ == "__main__":
    # Crear configuración de ejemplo
    create_proxy_config()
    
    # Probar el gestor
    proxy_manager = ProxyRotator()
    
    # Obtener IP sin proxy
    direct_ip = proxy_manager.get_current_ip()
    print(f"IP directa: {direct_ip}")
    
    # Probar proxies
    for proxy in proxy_manager.proxies:
        if proxy_manager.test_proxy(proxy):
            print(f"✅ Proxy {proxy.host}:{proxy.port} funcionando")
        else:
            print(f"❌ Proxy {proxy.host}:{proxy.port} no funciona")
    
    # Mostrar estadísticas
    stats = proxy_manager.get_stats()
    print(f"Estadísticas: {stats}")
