#!/usr/bin/env python3
"""
Demo Práctico: Comparación de las 3 herramientas en IMDb
Ejecuta Scrapy, Selenium y Playwright en el mismo dataset para comparar
"""

import subprocess
import asyncio
import time
import json
import os
import logging
from typing import Dict, List
from datetime import datetime
import sys

class IMDbComparisonDemo:
    """Demo práctico de las tres herramientas de scraping"""
    
    def __init__(self):
        self.logger = self._setup_logger()
        self.results = {}
        self.test_limit = 10  # Items para probar
        
    def _setup_logger(self):
        """Configurar logging para el demo"""
        logger = logging.getLogger('imdb_comparison')
        logger.setLevel(logging.INFO)
        
        # Console handler
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def run_scrapy_test(self) -> Dict:
        """Ejecutar test con Scrapy (herramienta actual)"""
        self.logger.info("🕷️  EJECUTANDO SCRAPY TEST")
        self.logger.info("=" * 40)
        
        start_time = time.time()
        
        try:
            # Ejecutar el scraper Scrapy actual
            cmd = [
                'scrapy', 'crawl', 'top_movies',
                '-s', f'CLOSESPIDER_ITEMCOUNT={self.test_limit}',
                '-s', 'LOG_LEVEL=WARNING',
                '-o', f'demo_scrapy_{self.test_limit}.csv'
            ]
            
            self.logger.info(f"Comando: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Verificar archivo de salida
            output_file = f'demo_scrapy_{self.test_limit}.csv'
            items_count = 0
            
            if os.path.exists(output_file):
                with open(output_file, 'r') as f:
                    lines = f.readlines()
                    items_count = max(0, len(lines) - 1)  # -1 por header
                
                # Mostrar muestra de datos
                self.logger.info(f"📄 Muestra de datos extraídos:")
                for i, line in enumerate(lines[:3]):
                    self.logger.info(f"   {line.strip()}")
            
            metrics = {
                'tool': 'scrapy',
                'execution_time': round(execution_time, 2),
                'items_extracted': items_count,
                'items_per_second': round(items_count / execution_time, 2) if execution_time > 0 else 0,
                'success': result.returncode == 0,
                'output_file': output_file
            }
            
            self.logger.info(f"✅ Scrapy completado: {items_count} items en {execution_time:.2f}s")
            return metrics
            
        except Exception as e:
            self.logger.error(f"❌ Error en Scrapy: {e}")
            return {'tool': 'scrapy', 'error': str(e)}
    
    def run_selenium_demo(self) -> Dict:
        """Demo simplificado de Selenium (sin ejecutar realmente)"""
        self.logger.info("🌐 SELENIUM DEMO (SIMULADO)")
        self.logger.info("=" * 40)
        
        # Código ejemplo de lo que haría Selenium
        selenium_code = '''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def scrape_imdb_selenium():
    # Configurar driver con anti-detección
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get('https://www.imdb.com/chart/top/')
        
        # Esperar y extraer elementos
        movies = []
        elements = driver.find_elements(By.CSS_SELECTOR, '.listItem')
        
        for i, element in enumerate(elements[:10]):
            title = element.find_element(By.CSS_SELECTOR, '.titleColumn a').text
            year = element.find_element(By.CSS_SELECTOR, '.secondaryInfo').text
            rating = element.find_element(By.CSS_SELECTOR, '.ratingColumn strong').text
            
            movies.append({
                'rank': i + 1,
                'title': title,
                'year': year.strip('()'),
                'rating': rating
            })
            
            time.sleep(1)  # Retardo humano
        
        return movies
        
    finally:
        driver.quit()
'''
        
        self.logger.info("📝 Código Selenium (ejemplo):")
        for line in selenium_code.strip().split('\n')[:15]:
            self.logger.info(f"   {line}")
        self.logger.info("   ... (código completo en examples/selenium_scraper_advanced.py)")
        
        # Métricas estimadas basadas en benchmark real
        estimated_metrics = {
            'tool': 'selenium',
            'execution_time': 143.39,  # Del benchmark real
            'items_extracted': 9,
            'items_per_second': 0.06,
            'memory_usage_mb': 150,
            'note': 'Métricas estimadas - requiere instalación completa'
        }
        
        self.logger.info(f"📊 Métricas estimadas: ~143s para 10 items (3.5x más lento que Scrapy)")
        return estimated_metrics
    
    def run_playwright_demo(self) -> Dict:
        """Demo simplificado de Playwright (sin ejecutar realmente)"""
        self.logger.info("🎭 PLAYWRIGHT DEMO (SIMULADO)")
        self.logger.info("=" * 40)
        
        # Código ejemplo de lo que haría Playwright
        playwright_code = '''
import asyncio
from playwright.async_api import async_playwright

async def scrape_imdb_playwright():
    async with async_playwright() as p:
        # Configurar navegador con stealth
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        
        # Script anti-detección
        await context.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
        });
        """)
        
        page = await context.new_page()
        await page.goto('https://www.imdb.com/chart/top/')
        
        # Extraer datos
        movies = []
        elements = await page.locator('.listItem').all()
        
        for i, element in enumerate(elements[:10]):
            title = await element.locator('.titleColumn a').inner_text()
            year = await element.locator('.secondaryInfo').inner_text()
            rating = await element.locator('.ratingColumn strong').inner_text()
            
            movies.append({
                'rank': i + 1,
                'title': title.strip(),
                'year': year.strip('()'),
                'rating': rating.strip()
            })
            
            await asyncio.sleep(0.5)  # Retardo humano
        
        await browser.close()
        return movies
'''
        
        self.logger.info("📝 Código Playwright (ejemplo):")
        for line in playwright_code.strip().split('\n')[:15]:
            self.logger.info(f"   {line}")
        self.logger.info("   ... (código completo en examples/playwright_scraper_advanced.py)")
        
        # Métricas estimadas basadas en benchmark real
        estimated_metrics = {
            'tool': 'playwright',
            'execution_time': 90.13,  # Del benchmark real
            'items_extracted': 10,
            'items_per_second': 0.11,
            'memory_usage_mb': 80,
            'note': 'Métricas estimadas - requiere instalación completa'
        }
        
        self.logger.info(f"📊 Métricas estimadas: ~90s para 10 items (2.2x más lento que Scrapy)")
        return estimated_metrics
    
    def generate_comparison_report(self):
        """Generar reporte de comparación"""
        self.logger.info("\n" + "=" * 60)
        self.logger.info("📊 REPORTE DE COMPARACIÓN TÉCNICA")
        self.logger.info("=" * 60)
        
        # Tabla de comparación
        tools_data = [
            {
                'tool': 'Scrapy',
                'time': self.results.get('scrapy', {}).get('execution_time', 'N/A'),
                'items': self.results.get('scrapy', {}).get('items_extracted', 'N/A'),
                'speed': self.results.get('scrapy', {}).get('items_per_second', 'N/A'),
                'memory': '~5MB',
                'complexity': 'Media',
                'best_for': 'Contenido estático (IMDb Top 250)'
            },
            {
                'tool': 'Selenium',
                'time': '~143s',
                'items': '~9',
                'speed': '~0.06/s',
                'memory': '~150MB',
                'complexity': 'Fácil',
                'best_for': 'JS pesado, interacciones complejas'
            },
            {
                'tool': 'Playwright',
                'time': '~90s',
                'items': '~10',
                'speed': '~0.11/s',
                'memory': '~80MB',
                'complexity': 'Media',
                'best_for': 'SPAs modernas, anti-bot avanzado'
            }
        ]
        
        # Mostrar tabla
        self.logger.info(f"{'Herramienta':<12} | {'Tiempo':<8} | {'Items':<6} | {'Velocidad':<10} | {'Memoria':<8} | {'Complejidad':<12}")
        self.logger.info("-" * 80)
        
        for tool in tools_data:
            self.logger.info(
                f"{tool['tool']:<12} | {str(tool['time']):<8} | {str(tool['items']):<6} | "
                f"{str(tool['speed']):<10} | {tool['memory']:<8} | {tool['complexity']:<12}"
            )
        
        # Recomendaciones específicas para IMDb
        self.logger.info("\n🎯 RECOMENDACIONES PARA IMDB:")
        self.logger.info("=" * 40)
        self.logger.info("✅ USAR SCRAPY porque:")
        self.logger.info("   • IMDb Top 250 es contenido estático (no requiere JS)")
        self.logger.info("   • Máximo rendimiento: 0.27 items/s vs 0.06 (Selenium)")
        self.logger.info("   • Mínimo uso de memoria: 5MB vs 150MB (Selenium)")
        self.logger.info("   • Selectores CSS estables y confiables")
        self.logger.info("   • Sistema de middleware robusto (proxies, delays)")
        
        self.logger.info("\n🔄 CONSIDERAR SELENIUM/PLAYWRIGHT cuando:")
        self.logger.info("   • Necesites JavaScript (reviews dinámicas, search)")
        self.logger.info("   • Requieras interacciones (login, clicks, formularios)")
        self.logger.info("   • Anti-bot sea intensivo (captchas frecuentes)")
        self.logger.info("   • Debugging visual sea necesario")
        
        # Guardar reporte
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'test_summary': {
                'target_site': 'IMDb Top 250',
                'test_items': self.test_limit,
                'scrapy_actual': self.results.get('scrapy', {}),
                'selenium_estimated': self.results.get('selenium', {}),
                'playwright_estimated': self.results.get('playwright', {})
            },
            'recommendations': {
                'current_project': 'Scrapy (óptimo para contenido estático)',
                'alternatives': {
                    'selenium': 'Para JS pesado e interacciones',
                    'playwright': 'Para SPAs y anti-bot avanzado'
                }
            }
        }
        
        report_file = f'imdb_comparison_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        self.logger.info(f"\n📄 Reporte completo guardado: {report_file}")
    
    def run_complete_demo(self):
        """Ejecutar demo completo de comparación"""
        self.logger.info("🎬 DEMO DE COMPARACIÓN TÉCNICA: SCRAPY vs SELENIUM vs PLAYWRIGHT")
        self.logger.info("Objetivo: Extraer top 10 películas de IMDb para comparar rendimiento")
        self.logger.info("=" * 80)
        
        # 1. Ejecutar Scrapy (real)
        scrapy_result = self.run_scrapy_test()
        self.results['scrapy'] = scrapy_result
        
        print()  # Línea en blanco
        
        # 2. Demo Selenium (simulado)
        selenium_result = self.run_selenium_demo()
        self.results['selenium'] = selenium_result
        
        print()  # Línea en blanco
        
        # 3. Demo Playwright (simulado)
        playwright_result = self.run_playwright_demo()
        self.results['playwright'] = playwright_result
        
        # 4. Generar reporte de comparación
        self.generate_comparison_report()
        
        self.logger.info("\n🎉 Demo de comparación completado!")
        self.logger.info("💡 Para ejecutar Selenium/Playwright reales:")
        self.logger.info("   ./scripts/install_comparison_deps.sh")
        self.logger.info("   python examples/selenium_scraper_advanced.py --limit 10")
        self.logger.info("   python examples/playwright_scraper_advanced.py --limit 10")


def main():
    """Función principal del demo"""
    print("🎬 IMDb Scraping: Comparación Técnica Práctica")
    print("=" * 50)
    print("Este demo compara Scrapy (actual) vs Selenium vs Playwright")
    print("para extraer datos de IMDb Top 250 películas")
    print()
    
    demo = IMDbComparisonDemo()
    
    try:
        demo.run_complete_demo()
    except KeyboardInterrupt:
        print("\n⚠️  Demo interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error en el demo: {e}")


if __name__ == '__main__':
    main()
