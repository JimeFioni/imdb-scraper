#!/usr/bin/env python3
"""
Implementación Práctica: Playwright para IMDb Scraping
Configuración anti-detección avanzada, stealth mode y concurrencia asyncio
"""

import asyncio
from playwright.async_api import async_playwright, BrowserContext, Page, Browser
from typing import List, Dict, Optional, Tuple
import json
import random
from dataclasses import dataclass, asdict
import logging
import os
import time
import csv
from contextlib import asynccontextmanager

@dataclass
class MovieData:
    """Estructura de datos de película"""
    rank: int
    title: str
    year: int
    rating: float
    director: str = ""
    stars: List[str] = None
    genre: List[str] = None
    duration: str = ""
    
    def __post_init__(self):
        if self.stars is None:
            self.stars = []
        if self.genre is None:
            self.genre = []

@dataclass
class BrowserConfig:
    """Configuración avanzada del navegador"""
    headless: bool = True
    viewport: Dict[str, int] = None
    user_agent: str = None
    locale: str = "en-US"
    timezone: str = "America/New_York"
    geolocation: Dict[str, float] = None
    permissions: List[str] = None
    proxy: Dict[str, str] = None
    
    def __post_init__(self):
        if self.viewport is None:
            self.viewport = {"width": 1920, "height": 1080}
        if self.permissions is None:
            self.permissions = []

class PlaywrightIMDbScraper:
    """Scraper IMDb usando Playwright con configuración anti-detección avanzada"""
    
    def __init__(self, config: BrowserConfig = None, max_concurrent: int = 3):
        self.config = config or BrowserConfig()
        self.max_concurrent = max_concurrent
        self.logger = self._setup_logger()
        self.playwright = None
        self.browser = None
        
        # User agents rotativos para máxima evasión
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
        ]
        
        # Configuraciones de viewport aleatorias
        self.viewports = [
            {"width": 1920, "height": 1080},
            {"width": 1366, "height": 768},
            {"width": 1440, "height": 900},
            {"width": 1600, "height": 900}
        ]
    
    def _setup_logger(self) -> logging.Logger:
        """Configurar sistema de logging avanzado"""
        logger = logging.getLogger('playwright_scraper')
        logger.setLevel(logging.INFO)
        
        # Evitar duplicar handlers
        if logger.handlers:
            return logger
        
        os.makedirs('logs', exist_ok=True)
        
        # File handler con rotación
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler(
            'logs/playwright_scraper.log', 
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    async def setup_browser(self) -> Browser:
        """Configurar navegador con evasión de detección ultra-avanzada"""
        if self.playwright is None:
            self.playwright = await async_playwright().start()
        
        # Configuración del navegador con stealth extremo
        browser_args = [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--no-first-run',
            '--no-zygote',
            '--disable-gpu',
            '--disable-features=VizDisplayCompositor',
            '--disable-background-networking',
            '--disable-background-timer-throttling',
            '--disable-renderer-backgrounding',
            '--disable-backgrounding-occluded-windows',
            '--disable-ipc-flooding-protection',
            '--disable-client-side-phishing-detection',
            '--disable-default-apps',
            '--disable-extensions',
            '--disable-component-extensions-with-background-pages',
            '--disable-sync',
            '--metrics-recording-only',
            '--no-default-browser-check',
            '--mute-audio',
            '--disable-prompt-on-repost',
            '--disable-domain-reliability',
            '--disable-features=TranslateUI',
            '--disable-features=BlinkGenPropertyTrees',
            '--disable-features=ImprovedCookieControls',
            '--disable-blink-features=AutomationControlled',
            '--no-experiments',
            '--disable-web-security',
            '--disable-features=VizDisplayCompositor'
        ]
        
        # Configurar proxy si está disponible
        proxy_config = None
        if self.config.proxy:
            proxy_config = {
                "server": f"{self.config.proxy.get('protocol', 'http')}://{self.config.proxy['host']}:{self.config.proxy['port']}"
            }
            if self.config.proxy.get('username'):
                proxy_config.update({
                    "username": self.config.proxy['username'],
                    "password": self.config.proxy.get('password', '')
                })
        
        self.browser = await self.playwright.chromium.launch(
            headless=self.config.headless,
            args=browser_args,
            proxy=proxy_config
        )
        
        self.logger.info("🚀 Navegador Playwright configurado con anti-detección avanzada")
        return self.browser
    
    async def create_stealth_context(self) -> BrowserContext:
        """Crear contexto del navegador con configuración stealth máxima"""
        if not self.browser:
            await self.setup_browser()
        
        # Seleccionar configuraciones aleatorias
        user_agent = random.choice(self.user_agents)
        viewport = random.choice(self.viewports)
        
        # Configurar geolocalización aleatoria (Estados Unidos)
        geolocation = {
            "latitude": round(random.uniform(25.0, 49.0), 6),
            "longitude": round(random.uniform(-125.0, -66.0), 6)
        }
        
        # Crear contexto con máxima evasión
        context = await self.browser.new_context(
            user_agent=user_agent,
            viewport=viewport,
            locale=self.config.locale,
            timezone_id=self.config.timezone,
            geolocation=geolocation,
            permissions=['geolocation'],
            
            # Headers adicionales para evasión
            extra_http_headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Cache-Control': 'max-age=0'
            }
        )
        
        # Scripts anti-detección avanzados
        await context.add_init_script("""
        // Remover webdriver flag
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
        });
        
        // Mock de propiedades de navegador real
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5],
        });
        
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en'],
        });
        
        // Chrome específico
        window.chrome = {
            runtime: {},
            loadTimes: function() {
                return {
                    requestTime: performance.timing.navigationStart / 1000,
                    startLoadTime: performance.timing.navigationStart / 1000,
                    commitLoadTime: performance.timing.responseStart / 1000,
                    finishDocumentLoadTime: performance.timing.domContentLoadedEventStart / 1000,
                    finishLoadTime: performance.timing.loadEventStart / 1000,
                    firstPaintTime: performance.timing.responseStart / 1000,
                    firstPaintAfterLoadTime: 0,
                    navigationType: 'Other',
                    wasFetchedViaSpdy: false,
                    wasNpnNegotiated: false,
                    npnNegotiatedProtocol: 'unknown',
                    wasAlternateProtocolAvailable: false,
                    connectionInfo: 'http/1.1'
                };
            },
            csi: function() {
                return {
                    pageT: Date.now(),
                    tran: 15
                };
            }
        };
        
        // Remover propiedades de automatización
        const propsToRemove = [
            '__driver_evaluate', '__webdriver_evaluate', '__selenium_evaluate', 
            '__fxdriver_evaluate', '__driver_unwrapped', '__webdriver_unwrapped', 
            '__selenium_unwrapped', '__fxdriver_unwrapped', '__webdriver_script_fn'
        ];
        
        propsToRemove.forEach(prop => {
            delete window[prop];
        });
        
        // Mock de permissions API
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
            Promise.resolve({ state: Notification.permission }) :
            originalQuery(parameters)
        );
        
        // Mock de propiedades de pantalla
        Object.defineProperty(screen, 'availWidth', {
            get: () => window.innerWidth,
        });
        
        Object.defineProperty(screen, 'availHeight', {
            get: () => window.innerHeight,
        });
        """)
        
        self.logger.info(f"🎭 Contexto stealth creado - UA: {user_agent[:50]}...")
        return context
    
    async def scrape_movie_details(self, page: Page, movie_selector: str, rank: int) -> Optional[MovieData]:
        """Extraer detalles de una película específica con selectores robustos"""
        try:
            # Esperar a que el elemento esté presente
            await page.wait_for_selector(movie_selector, timeout=10000)
            
            movie_element = page.locator(movie_selector)
            
            # Título - múltiples selectores
            title_selectors = [
                '.titleColumn a',
                '.cli-title a', 
                'h3.titleColumn a',
                '.titleColumn .title',
                '.title a'
            ]
            
            title = ""
            for selector in title_selectors:
                try:
                    title_elem = movie_element.locator(selector)
                    if await title_elem.count() > 0:
                        title = await title_elem.inner_text()
                        title = title.strip()
                        break
                except:
                    continue
            
            if not title:
                self.logger.warning(f"No se pudo extraer título para rank {rank}")
                return None
            
            # Año - múltiples selectores
            year_selectors = [
                '.titleColumn .secondaryInfo',
                '.cli-title .secondaryInfo',
                '.titleColumn .year',
                '.year'
            ]
            
            year = 0
            for selector in year_selectors:
                try:
                    year_elem = movie_element.locator(selector)
                    if await year_elem.count() > 0:
                        year_text = await year_elem.inner_text()
                        year_text = year_text.strip('()')
                        if year_text.isdigit():
                            year = int(year_text)
                            break
                except:
                    continue
            
            # Rating - múltiples selectores
            rating_selectors = [
                '.ratingColumn strong',
                '.imdbRating strong',
                '.rating strong',
                '.ratingColumn .value'
            ]
            
            rating = 0.0
            for selector in rating_selectors:
                try:
                    rating_elem = movie_element.locator(selector)
                    if await rating_elem.count() > 0:
                        rating_text = await rating_elem.inner_text()
                        rating = float(rating_text.strip())
                        break
                except:
                    continue
            
            # Crear objeto de película
            movie_data = MovieData(
                rank=rank,
                title=title,
                year=year,
                rating=rating
            )
            
            self.logger.debug(f"✅ Extraída: {title} ({year}) - {rating}")
            return movie_data
            
        except Exception as e:
            self.logger.error(f"❌ Error extrayendo película rank {rank}: {e}")
            return None
    
    async def scrape_page_with_retries(self, url: str, max_retries: int = 3) -> List[MovieData]:
        """Scraping de página con reintentos y manejo de errores avanzado"""
        movies = []
        
        for attempt in range(max_retries):
            context = None
            page = None
            
            try:
                self.logger.info(f"🌐 Cargando página: {url} (intento {attempt + 1})")
                
                # Crear nuevo contexto para cada intento
                context = await self.create_stealth_context()
                page = await context.new_page()
                
                # Configurar interceptores
                await page.route('**/*.{png,jpg,jpeg,gif,webp,svg,ico}', lambda route: route.abort())
                await page.route('**/*.{css,woff,woff2,ttf}', lambda route: route.abort())
                
                # Navegar con timeout extendido
                await page.goto(url, wait_until='domcontentloaded', timeout=30000)
                
                # Esperar que la página se estabilice
                await asyncio.sleep(random.uniform(2, 5))
                
                # Buscar elementos de películas con múltiples selectores
                movie_selectors = [
                    '.listItem',
                    '.titleColumn',
                    '.cli-item',
                    'li.list-item',
                    '.list .item'
                ]
                
                movie_elements = []
                for selector in movie_selectors:
                    try:
                        elements = page.locator(selector)
                        count = await elements.count()
                        if count > 0:
                            self.logger.info(f"📋 Encontrados {count} elementos con selector: {selector}")
                            
                            # Extraer datos de cada película
                            for i in range(min(count, 250)):  # Límite de seguridad
                                movie_data = await self.scrape_movie_details(page, f"{selector}:nth-child({i+1})", i+1)
                                if movie_data:
                                    movies.append(movie_data)
                                    
                                    # Retardo humano entre extracciones
                                    await asyncio.sleep(random.uniform(0.2, 0.8))
                            
                            break  # Usar el primer selector que funcione
                    except Exception as e:
                        self.logger.debug(f"Selector {selector} falló: {e}")
                        continue
                
                if movies:
                    self.logger.info(f"✅ Extraídas {len(movies)} películas exitosamente")
                    break  # Éxito, salir del loop de reintentos
                else:
                    self.logger.warning(f"⚠️  No se encontraron películas en intento {attempt + 1}")
                
            except Exception as e:
                self.logger.error(f"❌ Error en intento {attempt + 1}: {e}")
                
                if attempt == max_retries - 1:
                    self.logger.error("💥 Error final, abandonando página")
                else:
                    # Esperar antes del siguiente intento
                    await asyncio.sleep(random.uniform(5, 10))
            
            finally:
                # Limpiar recursos
                if page:
                    await page.close()
                if context:
                    await context.close()
        
        return movies
    
    async def scrape_top_movies(self, limit: int = 50) -> List[MovieData]:
        """Método principal de scraping con concurrencia asyncio"""
        self.logger.info(f"🎬 Iniciando scraping de top {limit} películas con Playwright")
        
        # URL de IMDb Top 250
        base_url = "https://www.imdb.com/chart/top/"
        
        try:
            # Configurar navegador
            await self.setup_browser()
            
            # Scraping de la página principal
            all_movies = await self.scrape_page_with_retries(base_url)
            
            # Limitar resultados
            limited_movies = all_movies[:limit]
            
            self.logger.info(f"🎯 Scraping completado: {len(limited_movies)} películas de {limit} solicitadas")
            return limited_movies
            
        except Exception as e:
            self.logger.error(f"💥 Error en scraping principal: {e}")
            return []
        
        finally:
            await self.cleanup()
    
    async def cleanup(self):
        """Limpiar recursos del navegador"""
        try:
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            self.logger.info("🧹 Recursos limpiados")
        except Exception as e:
            self.logger.error(f"Error en cleanup: {e}")
    
    def save_to_csv(self, movies: List[MovieData], filename: str = "playwright_movies.csv"):
        """Guardar películas en archivo CSV"""
        if not movies:
            self.logger.warning("⚠️  No hay películas para guardar")
            return
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['rank', 'title', 'year', 'rating', 'director', 'stars', 'genre', 'duration']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for movie in movies:
                    writer.writerow({
                        'rank': movie.rank,
                        'title': movie.title,
                        'year': movie.year,
                        'rating': movie.rating,
                        'director': movie.director,
                        'stars': ', '.join(movie.stars),
                        'genre': ', '.join(movie.genre),
                        'duration': movie.duration
                    })
            
            self.logger.info(f"📁 Películas guardadas en: {filename}")
            
        except Exception as e:
            self.logger.error(f"❌ Error guardando CSV: {e}")
    
    async def run_benchmark(self, limit: int = 25) -> Dict:
        """Ejecutar benchmark de rendimiento"""
        import psutil
        
        self.logger.info(f"🚀 Iniciando benchmark Playwright con {limit} películas")
        
        # Medición inicial
        process = psutil.Process()
        memory_before = process.memory_info().rss / 1024 / 1024
        start_time = time.time()
        
        # Ejecutar scraping
        movies = await self.scrape_top_movies(limit)
        
        # Medición final
        end_time = time.time()
        memory_after = process.memory_info().rss / 1024 / 1024
        
        execution_time = end_time - start_time
        memory_used = memory_after - memory_before
        
        # Guardar resultados
        output_file = f"playwright_benchmark_{limit}.csv"
        self.save_to_csv(movies, output_file)
        
        metrics = {
            'tool': 'playwright',
            'items_target': limit,
            'items_scraped': len(movies),
            'execution_time_seconds': round(execution_time, 2),
            'memory_used_mb': round(memory_used, 2),
            'items_per_second': round(len(movies) / execution_time, 2) if execution_time > 0 else 0,
            'success_rate': round((len(movies) / limit) * 100, 2) if limit > 0 else 0,
            'output_file': output_file
        }
        
        self.logger.info(f"📊 Benchmark completado: {metrics}")
        return metrics


# Funciones de utilidad para ejecución
async def main():
    """Función principal para testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Playwright IMDb Scraper')
    parser.add_argument('--limit', type=int, default=10, help='Número de películas a extraer')
    parser.add_argument('--headless', action='store_true', help='Ejecutar en modo headless')
    parser.add_argument('--benchmark', action='store_true', help='Ejecutar benchmark')
    
    args = parser.parse_args()
    
    config = BrowserConfig(headless=args.headless)
    scraper = PlaywrightIMDbScraper(config)
    
    try:
        if args.benchmark:
            metrics = await scraper.run_benchmark(args.limit)
            print(f"\n📊 Resultados del benchmark:")
            print(f"   Películas: {metrics['items_scraped']}/{metrics['items_target']}")
            print(f"   Tiempo: {metrics['execution_time_seconds']}s")
            print(f"   Memoria: {metrics['memory_used_mb']:.1f}MB")
            print(f"   Velocidad: {metrics['items_per_second']:.1f} items/s")
        else:
            movies = await scraper.scrape_top_movies(args.limit)
            scraper.save_to_csv(movies)
            print(f"\n🎉 Scraping completado: {len(movies)} películas extraídas")
    
    except KeyboardInterrupt:
        print("\n⚠️  Scraping interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        await scraper.cleanup()


if __name__ == '__main__':
    asyncio.run(main())
