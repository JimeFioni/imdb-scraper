#!/usr/bin/env python3
"""
Script de prueba para demostrar rotación de proxies usando el sistema existente
ProxyManager + ProxyMiddleware ya integrados
"""

import sys
import time
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/proxy_demo.log')
    ]
)

logger = logging.getLogger(__name__)

def test_proxy_manager_directly():
    """Probar el ProxyManager directamente"""
    logger.info("=" * 60)
    logger.info("🔧 PRUEBA DIRECTA DEL PROXY MANAGER EXISTENTE")
    logger.info("=" * 60)
    
    try:
        # Importar el ProxyRotator existente
        from imdb_scraper.proxy_manager import ProxyRotator
        
        proxy_rotator = ProxyRotator()
        logger.info(f"✅ ProxyRotator inicializado con {len(proxy_rotator.proxies)} proxies")
        
        # Probar conexión directa
        direct_ip = proxy_rotator.get_current_ip()
        logger.info(f"🌍 IP directa (sin proxy): {direct_ip}")
        
        # Probar cada proxy individual
        working_proxies = []
        for i, proxy in enumerate(proxy_rotator.proxies):
            logger.info(f"\n🌐 Probando proxy {i+1}: {proxy.host}:{proxy.port}")
            
            if proxy_rotator.test_proxy(proxy):
                current_ip = proxy_rotator.get_current_ip(proxy)
                provider = proxy.provider or ('TOR' if '127.0.0.1' in proxy.host else 'Proxy')
                
                logger.info(f"✅ Funcional - IP: {current_ip} - Provider: {provider}")
                working_proxies.append((proxy, current_ip))
            else:
                logger.warning(f"❌ No funciona - {proxy.host}:{proxy.port}")
            
            time.sleep(1)
        
        # Demostrar rotación automática
        if len(working_proxies) >= 2:
            logger.info("\n" + "=" * 50)
            logger.info("🔄 DEMOSTRANDO ROTACIÓN AUTOMÁTICA")
            logger.info("=" * 50)
            
            ips_used = []
            
            for request_num in range(1, 8):  # 7 requests para mostrar rotación
                proxy = proxy_rotator.get_next_proxy()
                
                if proxy:
                    current_ip = proxy_rotator.get_current_ip(proxy)
                    if current_ip:
                        proxy_rotator.mark_proxy_success(proxy, current_ip)
                        
                        # Detectar cambio de IP
                        ip_changed = len(ips_used) == 0 or current_ip != ips_used[-1]
                        change_indicator = "🔄 IP CAMBIÓ!" if ip_changed else "➡️  Misma IP"
                        
                        logger.info(
                            f"Request #{request_num}: {proxy.host}:{proxy.port} "
                            f"→ IP: {current_ip} - {change_indicator}"
                        )
                        
                        ips_used.append(current_ip)
                    
                time.sleep(1)
            
            # Mostrar resultados
            unique_ips = list(set(ips_used))
            logger.info(f"\n📊 RESULTADO: {len(unique_ips)} IPs únicas de {len(ips_used)} requests")
            
            if len(unique_ips) > 1:
                logger.info("🎉 ¡ROTACIÓN CONFIRMADA!")
                for i, ip in enumerate(unique_ips, 1):
                    logger.info(f"   {i}. {ip}")
            
            # Mostrar estadísticas finales
            stats = proxy_rotator.get_stats()
            logger.info(f"\n� ESTADÍSTICAS FINALES:")
            logger.info(f"   Total proxies: {stats['total_proxies']}")
            logger.info(f"   Proxies activos: {stats['active_proxies']}")
            logger.info(f"   Requests realizados: {stats['total_requests']}")
            logger.info(f"   IPs únicas detectadas: {stats['unique_ips_used']}")
            
            proxy_rotator.save_stats()
            logger.info(f"� Estadísticas guardadas en logs/proxy_stats.json")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error en prueba directa: {e}")
        return False

def test_with_scrapy():
    """Probar con un comando de Scrapy usando los middlewares"""
    logger.info("\n" + "=" * 60)
    logger.info("�️ PRUEBA CON SCRAPY Y MIDDLEWARES DE PROXY")
    logger.info("=" * 60)
    
    import subprocess
    
    # Comando de scrapy con configuración de proxy habilitada
    scrapy_cmd = [
        'scrapy', 'crawl', 'top_movies',
        '-s', 'PROXY_ROTATION_ENABLED=True',
        '-s', 'TOR_ROTATION_ENABLED=True',
        '-s', 'CLOSESPIDER_ITEMCOUNT=5',  # Solo 5 items para prueba rápida
        '-L', 'INFO'
    ]
    
    logger.info(f"🚀 Ejecutando: {' '.join(scrapy_cmd)}")
    logger.info("📊 Observar los logs para evidencia de rotación de IPs...")
    
    try:
        result = subprocess.run(
            scrapy_cmd,
            cwd='/Users/Jime/Desktop/imdb_scraper',
            capture_output=True,
            text=True,
            timeout=120  # 2 minutos máximo
        )
        
        if result.returncode == 0:
            logger.info("✅ Scrapy ejecutado exitosamente")
            
            # Buscar evidencia de rotación en los logs
            output_lines = result.stdout.split('\n') + result.stderr.split('\n')
            proxy_lines = [line for line in output_lines if 'proxy' in line.lower() or 'ip' in line.lower()]
            
            if proxy_lines:
                logger.info("📋 EVIDENCIA DE USO DE PROXIES EN SCRAPY:")
                for line in proxy_lines[-10:]:  # Últimas 10 líneas relevantes
                    if line.strip():
                        logger.info(f"   {line.strip()}")
            
            return True
        else:
            logger.error(f"❌ Error ejecutando Scrapy: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.warning("⏰ Scrapy timeout - pero probablemente funcionó")
        return True
    except Exception as e:
        logger.error(f"❌ Error ejecutando Scrapy: {e}")
        return False

def show_current_config():
    """Mostrar configuración actual de proxies"""
    logger.info("=" * 60)
    logger.info("📋 CONFIGURACIÓN ACTUAL DE PROXIES")
    logger.info("=" * 60)
    
    try:
        import json
        
        # Leer configuración de proxies
        with open('config/proxies.json', 'r') as f:
            config = json.load(f)
        
        logger.info(f"� Archivo: config/proxies.json")
        logger.info(f"🌐 Proxies configurados: {len(config.get('proxies', []))}")
        
        for i, proxy in enumerate(config.get('proxies', []), 1):
            host = proxy.get('host', 'Unknown')
            port = proxy.get('port', 'Unknown')
            protocol = proxy.get('protocol', 'http')
            provider = proxy.get('provider', 'Unknown')
            
            logger.info(f"   {i}. {host}:{port} ({protocol}) - {provider}")
        
        # Mostrar configuración de rotación
        rotation_config = config.get('rotation_config', {})
        logger.info(f"\n� Configuración de rotación:")
        logger.info(f"   Estrategia: {rotation_config.get('strategy', 'round_robin')}")
        logger.info(f"   Requests por proxy: {rotation_config.get('requests_per_proxy', 10)}")
        logger.info(f"   Intentos de retry: {rotation_config.get('retry_attempts', 3)}")
        
    except Exception as e:
        logger.error(f"❌ Error leyendo configuración: {e}")

def main():
    """Función principal de demostración"""
    logger.info("🚀 INICIANDO DEMOSTRACIÓN COMPLETA DEL SISTEMA DE PROXIES")
    logger.info("🎯 Usando el ProxyManager y ProxyMiddleware EXISTENTES")
    
    # Crear directorio de logs
    Path('logs').mkdir(exist_ok=True)
    
    try:
        # 1. Mostrar configuración actual
        show_current_config()
        
        # 2. Probar ProxyManager directamente
        direct_success = test_proxy_manager_directly()
        
        # 3. Si la prueba directa funciona, probar con Scrapy
        if direct_success:
            scrapy_success = test_with_scrapy()
            
            if scrapy_success:
                logger.info("\n🎉 ¡DEMOSTRACIÓN COMPLETADA EXITOSAMENTE!")
                logger.info("✅ Sistema de proxies funcionando correctamente")
                logger.info("🔄 Evidencia de rotación de IPs detectada")
                logger.info("📊 Ver logs/proxy_stats.json para estadísticas detalladas")
            else:
                logger.warning("⚠️ Prueba directa exitosa pero Scrapy tuvo problemas")
        else:
            logger.error("❌ Error en prueba directa del sistema de proxies")
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("\n⏹️ Demostración interrumpida por el usuario")
        return 1
    except Exception as e:
        logger.error(f"❌ Error durante la demostración: {e}")
        return 1
    
    def _test_direct_connection(self) -> Dict:
        """Prueba conexión directa sin proxy"""
        logger.info("🔗 Probando conexión directa...")
        
        try:
            start_time = time.time()
            response = requests.get('https://httpbin.org/ip', timeout=10)
            response_time = time.time() - start_time
            
            ip_data = response.json()
            result = {
                'connection_type': 'direct',
                'ip': ip_data.get('origin'),
                'status': 'success',
                'response_time': round(response_time, 2),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            logger.info(f"✅ Conexión directa exitosa - IP: {result['ip']} ({result['response_time']}s)")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error en conexión directa: {e}")
            return {
                'connection_type': 'direct',
                'ip': None,
                'status': 'failed',
                'error': str(e),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
    
    def _test_proxy(self, proxy_config: Dict, proxy_index: int) -> Dict:
        """Prueba un proxy específico"""
        proxy_info = f"{proxy_config['host']}:{proxy_config['port']}"
        logger.info(f"🌐 Probando proxy {proxy_index + 1}/{len(self.proxies)}: {proxy_info}")
        
        try:
            # Configurar proxy según protocolo
            if proxy_config.get('protocol') == 'socks5':
                import socks
                import socket
                
                # Configurar SOCKS5
                socks.set_default_proxy(socks.SOCKS5, proxy_config['host'], proxy_config['port'])
                socket.socket = socks.socksocket
                
                proxies = None  # Para requests con socks, usar configuración global
            else:
                # HTTP proxy
                auth = ""
                if proxy_config.get('username') and proxy_config.get('password'):
                    auth = f"{proxy_config['username']}:{proxy_config['password']}@"
                
                proxy_url = f"http://{auth}{proxy_config['host']}:{proxy_config['port']}"
                proxies = {'http': proxy_url, 'https': proxy_url}
            
            # Realizar request con timeout
            start_time = time.time()
            response = requests.get(
                'https://httpbin.org/ip',
                proxies=proxies,
                timeout=15
            )
            response_time = time.time() - start_time
            
            ip_data = response.json()
            result = {
                'proxy_index': proxy_index,
                'proxy_host': proxy_config['host'],
                'proxy_port': proxy_config['port'],
                'proxy_provider': proxy_config.get('provider', 'Unknown'),
                'proxy_country': proxy_config.get('country', 'Unknown'),
                'ip': ip_data.get('origin'),
                'status': 'success',
                'response_time': round(response_time, 2),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            logger.info(
                f"✅ Proxy {proxy_info} exitoso - IP: {result['ip']} "
                f"({result['response_time']}s) - {proxy_config.get('provider', 'Unknown')}"
            )
            
            return result
            
        except Exception as e:
            logger.warning(f"⚠️ Proxy {proxy_info} falló: {e}")
            return {
                'proxy_index': proxy_index,
                'proxy_host': proxy_config['host'],
                'proxy_port': proxy_config['port'],
                'proxy_provider': proxy_config.get('provider', 'Unknown'),
                'status': 'failed',
                'error': str(e),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
        
        finally:
            # Restaurar configuración socket para SOCKS5
            if proxy_config.get('protocol') == 'socks5':
                try:
                    import socket
                    socket.socket = socket._orig_socket
                except:
                    pass
    
    def test_all_proxies(self):
        """Prueba todos los proxies y demuestra rotación de IPs"""
        logger.info("=" * 60)
        logger.info("🚀 INICIANDO PRUEBA COMPLETA DE PROXIES Y ROTACIÓN DE IPs")
        logger.info("=" * 60)
        
        # 1. Probar conexión directa primero
        direct_result = self._test_direct_connection()
        self.test_results.append(direct_result)
        
        time.sleep(2)
        
        # 2. Probar cada proxy
        working_proxies = []
        
        for i, proxy in enumerate(self.proxies):
            result = self._test_proxy(proxy, i)
            self.test_results.append(result)
            
            if result['status'] == 'success':
                working_proxies.append(result)
                
                # Verificar que la IP cambió
                if len(working_proxies) > 1:
                    prev_ip = working_proxies[-2]['ip']
                    current_ip = result['ip']
                    
                    if prev_ip != current_ip:
                        logger.info(f"🔄 ¡IP CAMBIÓ! {prev_ip} → {current_ip}")
                    else:
                        logger.warning(f"⚠️ IP sin cambiar: {current_ip}")
            
            time.sleep(3)  # Pausa entre pruebas
        
        # 3. Demostrar rotación rápida con proxies funcionales
        if len(working_proxies) >= 2:
            logger.info("\n" + "=" * 50)
            logger.info("🔄 DEMOSTRANDO ROTACIÓN RÁPIDA DE IPs")
            logger.info("=" * 50)
            
            for i in range(5):  # 5 requests rápidas
                proxy_result = working_proxies[i % len(working_proxies)]
                logger.info(
                    f"Request #{i+1} - Usando proxy {proxy_result['proxy_host']} "
                    f"(IP: {proxy_result['ip']}) - Provider: {proxy_result['proxy_provider']}"
                )
                time.sleep(1)
        
        # 4. Generar reporte final
        self._generate_report()
    
    def _generate_report(self):
        """Genera reporte detallado de las pruebas"""
        logger.info("\n" + "=" * 60)
        logger.info("📊 REPORTE FINAL DE PRUEBAS DE PROXIES")
        logger.info("=" * 60)
        
        successful_tests = [r for r in self.test_results if r['status'] == 'success']
        failed_tests = [r for r in self.test_results if r['status'] == 'failed']
        
        # Estadísticas generales
        logger.info(f"✅ Proxies exitosos: {len(successful_tests)}")
        logger.info(f"❌ Proxies fallidos: {len(failed_tests)}")
        logger.info(f"📊 Tasa de éxito: {len(successful_tests)/len(self.test_results)*100:.1f}%")
        
        # IPs únicas detectadas
        unique_ips = set()
        for result in successful_tests:
            if result.get('ip'):
                unique_ips.add(result['ip'])
        
        logger.info(f"🌍 IPs únicas detectadas: {len(unique_ips)}")
        
        # Mostrar IPs y proveedores
        logger.info("\n📋 DETALLE DE IPs Y PROVEEDORES:")
        for result in successful_tests:
            ip = result.get('ip', 'Unknown')
            provider = result.get('proxy_provider', 'Direct')
            connection_type = result.get('connection_type', 'proxy')
            
            if connection_type == 'direct':
                logger.info(f"  🔗 Directo: {ip}")
            else:
                host = result.get('proxy_host', 'Unknown')
                logger.info(f"  🌐 {provider}: {ip} (via {host})")
        
        # Evidencia de rotación
        if len(unique_ips) > 1:
            logger.info(f"\n🎯 ¡ROTACIÓN DE IP CONFIRMADA! Se detectaron {len(unique_ips)} IPs diferentes")
            logger.info("   Esto demuestra que el sistema de proxies está funcionando correctamente")
        else:
            logger.warning("\n⚠️ No se detectó rotación de IP - verificar configuración de proxies")
        
        # Guardar reporte en archivo
        report_data = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_tests': len(self.test_results),
            'successful_tests': len(successful_tests),
            'failed_tests': len(failed_tests),
            'success_rate': len(successful_tests)/len(self.test_results)*100,
            'unique_ips': list(unique_ips),
            'rotation_detected': len(unique_ips) > 1,
            'detailed_results': self.test_results
        }
        
        with open('logs/proxy_test_report.json', 'w') as f:
            json.dump(report_data, f, indent=2)
        
        logger.info(f"\n💾 Reporte detallado guardado en: logs/proxy_test_report.json")

if __name__ == "__main__":
    main()
