#!/usr/bin/env python3
"""
Implementación práctica con Playwright para IMDb Scraper
Configuración avanzada con anti-detección y control de concurrencia
"""

import asyncio
from playwright.async_api import async_playwright, BrowserContext, Page
from typing import List, Dict, Optional
import json
import random
from dataclasses import dataclass
import logging
import os

@dataclass
class BrowserConfig:
    """Configuración avanzada del navegador"""
    headless: bool = True
    viewport: Dict[str, int] = None
    user_agent: str = None
    locale: str = "en-US"
    timezone: str = "America/New_York"
    permissions: List[str] = None
    geolocation: Dict[str, float] = None
    
    def __post_init__(self):
        if self.viewport is None:
            self.viewport = {"width": 1920, "height": 1080}
        if self.permissions is None:
            self.permissions = []

class PlaywrightIMDbScraper:
    """Scraper IMDb usando Playwright con configuración anti-detección"""
    
    def __init__(self, config: BrowserConfig = None):
        self.config = config or BrowserConfig()
        self.browser = None
        self.context = None
        self.logger = self._setup_logger()
        
        # User agents rotativos para evasión
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
    
    def _setup_logger(self) -> logging.Logger:
        """Configurar logging específico"""
        logger = logging.getLogger('playwright_scraper')
        logger.setLevel(logging.INFO)
        
        os.makedirs('logs', exist_ok=True)
        handler = logging.FileHandler('logs/playwright_scraper.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    async def setup_browser(self) -> BrowserContext:
        """Configurar navegador con evasión de detección avanzada"""
        playwright = await async_playwright().start()
        
        # Configuración del navegador con stealth
        browser = await playwright.chromium.launch(
            headless=self.config.headless,
            args=[
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
                '--disable-features=BlinkGenPropertyTrees'
            ]
        )
        
        # Crear contexto con configuración anti-detección
        context = await browser.new_context(
            viewport=self.config.viewport,
            user_agent=random.choice(self.user_agents),
            locale=self.config.locale,
            timezone_id=self.config.timezone,
            permissions=self.config.permissions,
            geolocation=self.config.geolocation,
            # Headers adicionales para parecer más humano
            extra_http_headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Cache-Control': 'max-age=0'
            }
        )
        
        # Inyectar scripts anti-detección
        await context.add_init_script("""
        // Ocultar webdriver
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
        });
        
        // Modificar chrome object
        window.chrome = {
            runtime: {},
            loadTimes: function() {},
            csi: function() {},
            app: {}
        };
        
        // Ocultar plugins de automatización
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5],
        });
        
        // Modificar permissions API
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
        );
        """)
        
        self.browser = browser
        self.context = context
        
        self.logger.info("Navegador configurado con anti-detección")
        return context
    
    async def create_page_with_stealth(self) -> Page:
        """Crear página con configuración stealth adicional"""
        page = await self.context.new_page()
        
        # Interceptar requests para modificar headers
        await page.route("**/*", self._handle_route)
        
        # Configurar timeouts
        page.set_default_navigation_timeout(30000)
        page.set_default_timeout(10000)
        
        return page
    
    async def _handle_route(self, route, request):
        """Manejar y modificar requests para evasión"""
        # Agregar headers realistas
        headers = {
            **request.headers,
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"'
        }
        
        await route.continue_(headers=headers)
    
    async def wait_for_element_with_retry(self, page: Page, selector: str, timeout: int = 10000) -> bool:
        """Espera explícita con reintentos para selectores dinámicos"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                await page.wait_for_selector(selector, timeout=timeout)
                return True
            except Exception as e:
                self.logger.warning(f"Intento {attempt + 1} fallido para selector {selector}: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2)
                    # Refrescar página si es el último intento
                    if attempt == max_retries - 2:
                        await page.reload()
        return False
    
    async def handle_potential_captcha(self, page: Page) -> bool:
        """Detectar y manejar CAPTCHAs"""
        captcha_selectors = [
            '[class*="captcha"]',
            '[id*="captcha"]',
            'iframe[src*="recaptcha"]',
            '.g-recaptcha',
            '[data-callback*="captcha"]'
        ]
        
        for selector in captcha_selectors:
            try:
                captcha_element = await page.query_selector(selector)
                if captcha_element:
                    self.logger.warning("CAPTCHA detectado, implementar solución manual o servicio")
                    
                    # Estrategias de manejo:
                    # 1. Pausa para resolución manual
                    self.logger.info("Pausando 60 segundos para resolución manual de CAPTCHA")
                    await asyncio.sleep(60)
                    
                    # 2. Integración con servicio de CAPTCHA (2captcha, AntiCaptcha)
                    # await self._solve_captcha_with_service(page, captcha_element)
                    
                    return True
            except Exception:
                continue
        
        return False
    
    async def scrape_movie_details(self, page: Page, movie_url: str) -> Dict:
        """Extraer detalles de película con selectores dinámicos"""
        try:
            await page.goto(movie_url, wait_until="domcontentloaded")
            
            # Manejar posible CAPTCHA
            await self.handle_potential_captcha(page)
            
            # Esperar elementos críticos con selectores múltiples
            title_selectors = [
                'h1[data-testid="hero-title-block__title"]',
                '.title_wrapper h1',
                'h1.titleHeader__title'
            ]
            
            title = None
            for selector in title_selectors:
                if await self.wait_for_element_with_retry(page, selector, 5000):
                    title = await page.text_content(selector)
                    break
            
            # Extraer datos con selectores robustos
            movie_data = {
                'title': title or 'N/A',
                'year': await self._extract_with_fallback(page, [
                    '[data-testid="hero-title-block__metadata"] a',
                    '.titleBar__metadata a'
                ]),
                'rating': await self._extract_with_fallback(page, [
                    '[data-testid="hero-rating-bar__aggregate-rating__score"] span',
                    '.ratingValue strong span'
                ]),
                'duration': await self._extract_with_fallback(page, [
                    '[data-testid="title-techspec_runtime"]',
                    'time[datetime]'
                ]),
                'metascore': await self._extract_with_fallback(page, [
                    '[data-testid="meta-score"]',
                    '.metacriticScore span'
                ]),
                'cast': await self._extract_cast(page)
            }
            
            self.logger.info(f"Extraído: {movie_data['title']}")
            return movie_data
            
        except Exception as e:
            self.logger.error(f"Error extrayendo {movie_url}: {e}")
            return {}
    
    async def _extract_with_fallback(self, page: Page, selectors: List[str]) -> str:
        """Extraer texto con selectores de fallback"""
        for selector in selectors:
            try:
                element = await page.query_selector(selector)
                if element:
                    text = await element.text_content()
                    if text and text.strip():
                        return text.strip()
            except Exception:
                continue
        return 'N/A'
    
    async def _extract_cast(self, page: Page) -> str:
        """Extraer elenco principal"""
        cast_selectors = [
            '[data-testid="title-cast-item"] a',
            '.cast_list .primary_photo + td a'
        ]
        
        for selector in cast_selectors:
            try:
                elements = await page.query_selector_all(selector)
                if elements:
                    cast_names = []
                    for element in elements[:3]:  # Top 3 actores
                        name = await element.text_content()
                        if name:
                            cast_names.append(name.strip())
                    return ', '.join(cast_names)
            except Exception:
                continue
        
        return 'N/A'
    
    async def scrape_top_movies(self, limit: int = 10) -> List[Dict]:
        """Scraper principal con control de concurrencia"""
        movies = []
        
        try:
            await self.setup_browser()
            page = await self.create_page_with_stealth()
            
            # Navegar a la página principal
            await page.goto("https://www.imdb.com/chart/top/", wait_until="domcontentloaded")
            
            # Manejar posible CAPTCHA
            await self.handle_potential_captcha(page)
            
            # Esperar y extraer URLs de películas
            await self.wait_for_element_with_retry(page, '.cli-item', 15000)
            
            # Extraer URLs con selectores robustos
            movie_elements = await page.query_selector_all('.cli-item .cli-title a')
            movie_urls = []
            
            for element in movie_elements[:limit]:
                href = await element.get_attribute('href')
                if href:
                    full_url = f"https://www.imdb.com{href}"
                    movie_urls.append(full_url)
            
            self.logger.info(f"Encontradas {len(movie_urls)} URLs de películas")
            
            # Procesar películas con control de concurrencia
            await self._process_movies_concurrent(movie_urls, movies)
            
        except Exception as e:
            self.logger.error(f"Error en scraping principal: {e}")
        finally:
            if self.browser:
                await self.browser.close()
        
        return movies
    
    async def _process_movies_concurrent(self, urls: List[str], movies: List[Dict], 
                                       max_concurrent: int = 3):
        """Procesar películas con control de concurrencia"""
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def process_single_movie(url: str):
            async with semaphore:
                page = await self.create_page_with_stealth()
                try:
                    movie_data = await self.scrape_movie_details(page, url)
                    if movie_data:
                        movies.append(movie_data)
                    
                    # Delay aleatorio para parecer más humano
                    await asyncio.sleep(random.uniform(1, 3))
                    
                finally:
                    await page.close()
        
        # Ejecutar tasks concurrentes
        tasks = [process_single_movie(url) for url in urls]
        await asyncio.gather(*tasks, return_exceptions=True)
        
        self.logger.info(f"Procesadas {len(movies)} películas con concurrencia")

# Función principal para ejecutar
async def main():
    """Función principal del scraper Playwright"""
    config = BrowserConfig(
        headless=True,  # Cambiar a False para debugging
        viewport={"width": 1920, "height": 1080}
    )
    
    scraper = PlaywrightIMDbScraper(config)
    movies = await scraper.scrape_top_movies(limit=10)  # Limitar para pruebas
    
    # Guardar resultados
    os.makedirs('data/exports', exist_ok=True)
    with open('data/exports/playwright_movies.json', 'w') as f:
        json.dump(movies, f, indent=2)
    
    print(f"✅ Extraídas {len(movies)} películas con Playwright")
    
    # Mostrar ejemplo de resultado
    if movies:
        print(f"🎬 Ejemplo: {movies[0]['title']} ({movies[0]['year']}) - {movies[0]['rating']}")

if __name__ == "__main__":
    asyncio.run(main())
