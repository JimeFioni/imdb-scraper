"""
Middleware de Scrapy para rotación automática de proxies
Integra con el ProxyManager para control avanzado de red
"""

import random
import time
import logging
from typing import Optional
from scrapy import signals
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
from scrapy.exceptions import NotConfigured, IgnoreRequest
from twisted.internet.error import TimeoutError, DNSLookupError, ConnectionRefusedError, ConnectionLost

from .proxy_manager import ProxyRotator, ProxyConfig


class ProxyRotationMiddleware:
    """
    Middleware avanzado para rotación de proxies con fallback automático
    """
    
    def __init__(self, settings):
        self.proxy_rotator = ProxyRotator()
        self.enabled = settings.getbool('PROXY_ROTATION_ENABLED', True)
        self.max_retry_times = settings.getint('PROXY_RETRY_TIMES', 3)
        self.retry_priority_adjust = settings.getint('RETRY_PRIORITY_ADJUST', -1)
        
        # Configurar logging
        self.logger = logging.getLogger(__name__)
        
        if not self.enabled:
            raise NotConfigured('Proxy rotation middleware disabled')
        
        # Inicializar estadísticas
        self.stats = {
            'requests_total': 0,
            'requests_with_proxy': 0,
            'proxy_failures': 0,
            'ip_changes': 0,
            'retries': 0
        }
        
        self.logger.info("ProxyRotationMiddleware inicializado")
    
    @classmethod
    def from_crawler(cls, crawler):
        """Crear instancia desde crawler"""
        settings = crawler.settings
        middleware = cls(settings)
        
        # Conectar señales
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        
        return middleware
    
    def spider_opened(self, spider):
        """Ejecutar cuando el spider se abre"""
        self.logger.info(f"Spider {spider.name} iniciado con rotación de proxies")
        
        # Probar proxies al inicio
        self._test_initial_proxies()
    
    def spider_closed(self, spider):
        """Ejecutar cuando el spider se cierra"""
        # Guardar estadísticas finales
        self.proxy_rotator.save_stats()
        
        # Log de estadísticas finales
        stats = self.proxy_rotator.get_stats()
        self.logger.info(f"Spider {spider.name} finalizado. Estadísticas de proxy:")
        self.logger.info(f"  - Total requests: {stats['total_requests']}")
        self.logger.info(f"  - IPs únicas usadas: {stats['unique_ips_used']}")
        self.logger.info(f"  - Proxies activos: {stats['active_proxies']}/{stats['total_proxies']}")
    
    def _test_initial_proxies(self):
        """Probar proxies al inicio para validar disponibilidad"""
        self.logger.info("Probando proxies disponibles...")
        
        working_proxies = 0
        for proxy in self.proxy_rotator.proxies:
            if self.proxy_rotator.test_proxy(proxy):
                working_proxies += 1
        
        self.logger.info(f"{working_proxies}/{len(self.proxy_rotator.proxies)} proxies funcionando")
    
    def process_request(self, request, spider):
        """Procesar request agregando proxy"""
        self.stats['requests_total'] += 1
        
        # Obtener proxy para este request
        proxy = self.proxy_rotator.get_next_proxy()
        
        if proxy and proxy.is_active:
            # Configurar proxy en el request
            proxy_url = self._build_proxy_url(proxy)
            request.meta['proxy'] = proxy_url
            request.meta['proxy_config'] = proxy
            
            # Headers adicionales para evitar detección
            self._add_stealth_headers(request)
            
            self.stats['requests_with_proxy'] += 1
            
            # Log del proxy usado
            self.logger.debug(f"Request {request.url} usando proxy {proxy.host}:{proxy.port}")
            
        else:
            # Sin proxy disponible - usar conexión directa
            request.meta.pop('proxy', None)
            request.meta['proxy_config'] = None
            self.logger.warning("No hay proxies disponibles - usando conexión directa")
        
        return None
    
    def process_response(self, request, response, spider):
        """Procesar respuesta y manejar errores de proxy"""
        proxy_config = request.meta.get('proxy_config')
        
        # Verificar si la respuesta indica bloqueo
        if self._is_blocked_response(response):
            return self._retry_with_different_proxy(request, response, spider, "Respuesta bloqueada")
        
        # Respuesta exitosa
        if proxy_config and response.status == 200:
            # Obtener IP usada si es posible
            current_ip = self._extract_ip_from_response(response)
            if current_ip:
                self.proxy_rotator.mark_proxy_success(proxy_config, current_ip)
            else:
                # Intentar obtener IP en segundo plano
                self._verify_proxy_ip(proxy_config)
        
        return response
    
    def process_exception(self, request, exception, spider):
        """Procesar excepciones de red y cambiar proxy"""
        proxy_config = request.meta.get('proxy_config')
        
        # Excepciones que indican problemas de proxy
        proxy_errors = (TimeoutError, DNSLookupError, ConnectionRefusedError, ConnectionLost)
        
        if isinstance(exception, proxy_errors) and proxy_config:
            self.proxy_rotator.mark_proxy_failed(proxy_config)
            self.stats['proxy_failures'] += 1
            
            return self._retry_with_different_proxy(
                request, exception, spider, f"Excepción de proxy: {type(exception).__name__}"
            )
        
        return None
    
    def _retry_with_different_proxy(self, request, response_or_exception, spider, reason):
        """Reintentar request con un proxy diferente"""
        retry_times = request.meta.get('retry_times', 0) + 1
        
        if retry_times <= self.max_retry_times:
            self.logger.info(f"Reintentando request {request.url} (intento {retry_times}): {reason}")
            
            # Obtener nuevo proxy
            new_proxy = self.proxy_rotator.get_next_proxy()
            
            if new_proxy and new_proxy.is_active:
                # Crear nuevo request con proxy diferente
                new_request = request.copy()
                new_request.meta['retry_times'] = retry_times
                new_request.meta['proxy'] = self._build_proxy_url(new_proxy)
                new_request.meta['proxy_config'] = new_proxy
                new_request.priority = request.priority + self.retry_priority_adjust
                
                # Añadir delay para evitar detección
                time.sleep(random.uniform(1, 3))
                
                self.stats['retries'] += 1
                self.stats['ip_changes'] += 1
                
                return new_request
            else:
                self.logger.error("No hay proxies disponibles para reintentar")
        
        # Si se agotaron los intentos o no hay proxies
        self.logger.error(f"Request fallido tras {retry_times} intentos: {request.url}")
        return None
    
    def _build_proxy_url(self, proxy: ProxyConfig) -> str:
        """Construir URL del proxy"""
        auth = ""
        if proxy.username and proxy.password:
            auth = f"{proxy.username}:{proxy.password}@"
        
        return f"{proxy.protocol}://{auth}{proxy.host}:{proxy.port}"
    
    def _add_stealth_headers(self, request):
        """Añadir headers para evitar detección"""
        stealth_headers = {
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        for header, value in stealth_headers.items():
            if header not in request.headers:
                request.headers[header] = value
    
    def _is_blocked_response(self, response) -> bool:
        """Detectar si la respuesta indica bloqueo"""
        # Códigos de estado que indican bloqueo
        blocked_status_codes = [403, 429, 503, 521, 522, 523, 524]
        
        if response.status in blocked_status_codes:
            return True
        
        # Verificar contenido que indica bloqueo
        blocked_indicators = [
            b'blocked',
            b'access denied',
            b'rate limit',
            b'too many requests',
            b'captcha',
            b'cloudflare',
            b'please verify',
        ]
        
        body_lower = response.body.lower()
        for indicator in blocked_indicators:
            if indicator in body_lower:
                return True
        
        return False
    
    def _extract_ip_from_response(self, response) -> Optional[str]:
        """Intentar extraer IP de la respuesta si es posible"""
        # Para páginas que muestran la IP (como httpbin.org)
        try:
            if b'"origin"' in response.body:
                import json
                data = json.loads(response.text)
                return data.get('origin', '').split(',')[0].strip()
        except:
            pass
        
        return None
    
    def _verify_proxy_ip(self, proxy_config: ProxyConfig):
        """Verificar IP del proxy en segundo plano"""
        try:
            current_ip = self.proxy_rotator.get_current_ip(proxy_config)
            if current_ip:
                self.proxy_rotator.mark_proxy_success(proxy_config, current_ip)
        except:
            pass  # No es crítico si falla


class TorRotationMiddleware:
    """
    Middleware específico para rotación de identidad TOR
    """
    
    def __init__(self, settings):
        self.enabled = settings.getbool('TOR_ROTATION_ENABLED', False)
        self.rotation_interval = settings.getint('TOR_ROTATION_INTERVAL', 30)
        self.control_port = settings.getint('TOR_CONTROL_PORT', 9051)
        self.control_password = settings.get('TOR_CONTROL_PASSWORD', '')
        
        self.request_count = 0
        self.logger = logging.getLogger(__name__)
        
        if not self.enabled:
            raise NotConfigured('TOR rotation middleware disabled')
        
        self.logger.info("TorRotationMiddleware inicializado")
    
    @classmethod
    def from_crawler(cls, crawler):
        """Crear instancia desde crawler"""
        return cls(crawler.settings)
    
    def process_request(self, request, spider):
        """Procesar request y rotar identidad TOR si es necesario"""
        self.request_count += 1
        
        # Rotar identidad cada X requests
        if self.request_count % self.rotation_interval == 0:
            self._rotate_tor_identity()
        
        return None
    
    def _rotate_tor_identity(self):
        """Rotar identidad TOR usando el puerto de control"""
        try:
            import socket
            
            # Conectar al puerto de control de TOR
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('127.0.0.1', self.control_port))
                
                # Autenticar si hay password
                if self.control_password:
                    s.send(f'AUTHENTICATE "{self.control_password}"\r\n'.encode())
                else:
                    s.send(b'AUTHENTICATE\r\n')
                
                # Leer respuesta
                response = s.recv(1024)
                
                if b'250 OK' in response:
                    # Solicitar nueva identidad
                    s.send(b'SIGNAL NEWNYM\r\n')
                    response = s.recv(1024)
                    
                    if b'250 OK' in response:
                        self.logger.info("Identidad TOR rotada exitosamente")
                        time.sleep(2)  # Esperar a que TOR establezca nueva ruta
                    else:
                        self.logger.error("Error rotando identidad TOR")
                else:
                    self.logger.error("Error autenticando con TOR")
                    
        except Exception as e:
            self.logger.error(f"Error rotando identidad TOR: {e}")


# Configuración para settings.py
PROXY_MIDDLEWARE_CONFIG = {
    'DOWNLOADER_MIDDLEWARES': {
        'imdb_scraper.proxy_middleware.ProxyRotationMiddleware': 350,
        'imdb_scraper.proxy_middleware.TorRotationMiddleware': 351,
        'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,  # Deshabilitar retry por defecto
    },
    
    # Configuración de proxy
    'PROXY_ROTATION_ENABLED': True,
    'PROXY_RETRY_TIMES': 3,
    'RETRY_PRIORITY_ADJUST': -1,
    
    # Configuración de TOR
    'TOR_ROTATION_ENABLED': False,
    'TOR_ROTATION_INTERVAL': 10,
    'TOR_CONTROL_PORT': 9051,
    'TOR_CONTROL_PASSWORD': '',
    
    # Configuración de requests
    'DOWNLOAD_TIMEOUT': 30,
    'DOWNLOAD_DELAY': 2,
    'RANDOMIZE_DOWNLOAD_DELAY': 0.5,
    'CONCURRENT_REQUESTS': 1,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
}
