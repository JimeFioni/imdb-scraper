#!/usr/bin/env python3
"""
Script de Ejemplos Prácticos: Selectores y Configuraciones para IMDb
Demuestra configuraciones específicas para cada herramienta
"""

# ========================================================================
# 1. SCRAPY - CONFIGURACIÓN OPTIMIZADA PARA IMDB
# ========================================================================

SCRAPY_IMDB_SPIDER = '''
import scrapy
from urllib.parse import urljoin

class IMDbOptimizedSpider(scrapy.Spider):
    """Spider optimizado específicamente para IMDb Top 250"""
    
    name = 'imdb_top_optimized'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/chart/top/']
    
    # Configuración específica para IMDb
    custom_settings = {
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': 2,  # Respetar rate limits
        'RANDOMIZE_DOWNLOAD_DELAY': 0.5,
        'CONCURRENT_REQUESTS': 1,
        'USER_AGENT': 'Mozilla/5.0 (compatible; IMDbScraper/1.0)',
        
        # Headers específicos para IMDb
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    }
    
    def parse(self, response):
        """Extracción con selectores robustos para IMDb"""
        
        # Selectores específicos para IMDb Top 250
        movies = response.css('.listItem')
        
        for movie in movies:
            # Datos básicos con fallbacks
            title = movie.css('.titleColumn a::text').get()
            year_text = movie.css('.titleColumn .secondaryInfo::text').get()
            rating = movie.css('.ratingColumn strong::text').get()
            
            # Limpiar año
            year = None
            if year_text:
                year_clean = year_text.strip('()')
                if year_clean.isdigit():
                    year = int(year_clean)
            
            # Ranking desde el número
            rank_text = movie.css('.numberColumn::text').get()
            rank = None
            if rank_text:
                rank = int(rank_text.strip('.'))
            
            # URL de detalles para información adicional
            detail_url = movie.css('.titleColumn a::attr(href)').get()
            full_url = urljoin(response.url, detail_url) if detail_url else None
            
            # Yield item básico
            item = {
                'ranking': rank,
                'titulo': title.strip() if title else None,
                'anio': year,
                'calificacion': float(rating) if rating else None,
                'url': full_url
            }
            
            # Si necesitamos detalles adicionales, hacer request
            if full_url and self.should_get_details():
                yield response.follow(
                    detail_url,
                    callback=self.parse_movie_details,
                    meta={'item': item}
                )
            else:
                yield item
    
    def should_get_details(self):
        """Determinar si obtener detalles adicionales"""
        # Solo obtener detalles si CLOSESPIDER_ITEMCOUNT no está definido
        # o es mayor a 50 (para evitar sobrecarga en tests)
        limit = self.settings.get('CLOSESPIDER_ITEMCOUNT')
        return limit is None or limit > 50
    
    def parse_movie_details(self, response):
        """Extraer detalles adicionales de la página de película"""
        item = response.meta['item']
        
        # Directores
        directors = response.css('.credit_summary_item:contains("Director") a::text').getall()
        item['director'] = ', '.join(directors) if directors else None
        
        # Actores principales (primeros 3)
        stars = response.css('.credit_summary_item:contains("Stars") a::text').getall()[:3]
        item['actores'] = ', '.join(stars) if stars else None
        
        # Géneros
        genres = response.css('.subtext a[href*="genres"]::text').getall()
        item['generos'] = ', '.join(genres) if genres else None
        
        # Duración
        duration = response.css('.subtext time::text').get()
        item['duracion'] = duration.strip() if duration else None
        
        # Metascore
        metascore = response.css('.metacriticScore span::text').get()
        item['metascore'] = int(metascore) if metascore and metascore.isdigit() else None
        
        yield item
'''

# ========================================================================
# 2. SELENIUM - CONFIGURACIÓN ANTI-DETECCIÓN PARA IMDB
# ========================================================================

SELENIUM_IMDB_SCRAPER = '''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import random
import time
import json

class SeleniumIMDbScraper:
    """Scraper Selenium optimizado para IMDb con anti-detección"""
    
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        ]
    
    def create_imdb_driver(self):
        """Driver específicamente configurado para IMDb"""
        options = Options()
        
        # Configuración stealth para IMDb
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-images')  # Acelerar carga
        
        # Anti-detección específica
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # User agent aleatorio
        ua = random.choice(self.user_agents)
        options.add_argument(f'--user-agent={ua}')
        
        # Viewport realista
        width = random.randint(1200, 1920)
        height = random.randint(800, 1080)
        options.add_argument(f'--window-size={width},{height}')
        
        # Configuraciones adicionales para IMDb
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
            "profile.managed_default_content_settings.images": 2  # Bloquear imágenes
        }
        options.add_experimental_option("prefs", prefs)
        
        driver = webdriver.Chrome(options=options)
        
        # Script anti-detección post-creación
        driver.execute_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
        });
        
        // Simular plugins reales
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5],
        });
        
        // Chrome runtime
        window.chrome = { runtime: {} };
        """)
        
        # Timeouts apropiados para IMDb
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(30)
        
        return driver
    
    def scrape_imdb_top250(self, limit=50):
        """Scraping específico para IMDb Top 250"""
        driver = self.create_imdb_driver()
        movies = []
        
        try:
            # Navegar a IMDb Top 250
            driver.get('https://www.imdb.com/chart/top/')
            
            # Esperar que la página cargue
            wait = WebDriverWait(driver, 20)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.listItem')))
            
            # Retardo humano
            time.sleep(random.uniform(2, 4))
            
            # Encontrar elementos de películas
            movie_elements = driver.find_elements(By.CSS_SELECTOR, '.listItem')
            
            for i, element in enumerate(movie_elements[:limit]):
                try:
                    # Selectores específicos para IMDb
                    title_elem = element.find_element(By.CSS_SELECTOR, '.titleColumn a')
                    year_elem = element.find_element(By.CSS_SELECTOR, '.titleColumn .secondaryInfo')
                    rating_elem = element.find_element(By.CSS_SELECTOR, '.ratingColumn strong')
                    
                    # Extraer datos
                    title = title_elem.text.strip()
                    year = year_elem.text.strip('()')
                    rating = rating_elem.text.strip()
                    
                    movie = {
                        'rank': i + 1,
                        'title': title,
                        'year': int(year) if year.isdigit() else None,
                        'rating': float(rating) if rating else None,
                        'url': title_elem.get_attribute('href')
                    }
                    
                    movies.append(movie)
                    
                    # Retardo humano entre extracciones
                    time.sleep(random.uniform(0.5, 1.5))
                    
                except Exception as e:
                    print(f"Error extrayendo película {i+1}: {e}")
                    continue
        
        finally:
            driver.quit()
        
        return movies
    
    def scrape_with_error_handling(self, limit=50, max_retries=3):
        """Scraping con manejo robusto de errores"""
        for attempt in range(max_retries):
            try:
                movies = self.scrape_imdb_top250(limit)
                if movies:
                    return movies
            except Exception as e:
                print(f"Intento {attempt + 1} falló: {e}")
                if attempt < max_retries - 1:
                    time.sleep(random.uniform(5, 10))
        
        return []
'''

# ========================================================================
# 3. PLAYWRIGHT - CONFIGURACIÓN STEALTH PARA IMDB
# ========================================================================

PLAYWRIGHT_IMDB_SCRAPER = '''
import asyncio
from playwright.async_api import async_playwright
import random
import json

class PlaywrightIMDbScraper:
    """Scraper Playwright con máxima evasión para IMDb"""
    
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        
        self.viewports = [
            {"width": 1920, "height": 1080},
            {"width": 1366, "height": 768},
            {"width": 1440, "height": 900}
        ]
    
    async def create_stealth_context(self, browser):
        """Contexto ultra-stealth para IMDb"""
        
        # Configuración aleatoria
        user_agent = random.choice(self.user_agents)
        viewport = random.choice(self.viewports)
        
        # Geolocalización US (IMDb es sitio estadounidense)
        geolocation = {
            "latitude": round(random.uniform(25.0, 49.0), 6),
            "longitude": round(random.uniform(-125.0, -66.0), 6)
        }
        
        context = await browser.new_context(
            user_agent=user_agent,
            viewport=viewport,
            locale="en-US",
            timezone_id="America/New_York",
            geolocation=geolocation,
            permissions=['geolocation'],
            
            # Headers optimizados para IMDb
            extra_http_headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none'
            }
        )
        
        # Script anti-detección ultra-completo
        await context.add_init_script("""
        // Remover todas las banderas de automatización
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
        
        // Chrome específico para pasar validaciones
        window.chrome = {
            runtime: {},
            loadTimes: function() {
                return {
                    requestTime: performance.timing.navigationStart / 1000,
                    startLoadTime: performance.timing.navigationStart / 1000,
                    commitLoadTime: performance.timing.responseStart / 1000,
                    finishDocumentLoadTime: performance.timing.domContentLoadedEventStart / 1000,
                    finishLoadTime: performance.timing.loadEventStart / 1000,
                };
            },
            csi: function() {
                return { pageT: Date.now(), tran: 15 };
            }
        };
        
        // Remover propiedades de automatización
        const props = [
            '__driver_evaluate', '__webdriver_evaluate', '__selenium_evaluate',
            '__fxdriver_evaluate', '__driver_unwrapped', '__webdriver_unwrapped',
            '__selenium_unwrapped', '__fxdriver_unwrapped', '__webdriver_script_fn'
        ];
        
        props.forEach(prop => delete window[prop]);
        
        // Mock de permissions API
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
            Promise.resolve({ state: Notification.permission }) :
            originalQuery(parameters)
        );
        """)
        
        return context
    
    async def scrape_imdb_top250(self, limit=50):
        """Scraping principal con manejo de errores"""
        async with async_playwright() as p:
            # Configurar navegador
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-zygote',
                    '--disable-gpu',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-blink-features=AutomationControlled'
                ]
            )
            
            context = await self.create_stealth_context(browser)
            page = await context.new_page()
            
            # Bloquear recursos innecesarios
            await page.route('**/*.{png,jpg,jpeg,gif,webp,svg,ico,css,woff,woff2,ttf}', 
                           lambda route: route.abort())
            
            movies = []
            
            try:
                # Navegar a IMDb Top 250
                await page.goto('https://www.imdb.com/chart/top/', 
                              wait_until='domcontentloaded', timeout=30000)
                
                # Esperar estabilización
                await asyncio.sleep(random.uniform(2, 4))
                
                # Selectores específicos para IMDb
                movie_locators = await page.locator('.listItem').all()
                
                for i, locator in enumerate(movie_locators[:limit]):
                    try:
                        # Extraer datos con selectores robustos
                        title = await locator.locator('.titleColumn a').inner_text()
                        year_text = await locator.locator('.titleColumn .secondaryInfo').inner_text()
                        rating_text = await locator.locator('.ratingColumn strong').inner_text()
                        
                        # Limpiar datos
                        year = int(year_text.strip('()')) if year_text.strip('()').isdigit() else None
                        rating = float(rating_text.strip()) if rating_text.strip() else None
                        
                        movie = {
                            'rank': i + 1,
                            'title': title.strip(),
                            'year': year,
                            'rating': rating
                        }
                        
                        movies.append(movie)
                        
                        # Retardo humano
                        await asyncio.sleep(random.uniform(0.2, 0.8))
                        
                    except Exception as e:
                        print(f"Error extrayendo película {i+1}: {e}")
                        continue
            
            finally:
                await browser.close()
            
            return movies
    
    async def scrape_with_retries(self, limit=50, max_retries=3):
        """Scraping con reintentos automáticos"""
        for attempt in range(max_retries):
            try:
                movies = await self.scrape_imdb_top250(limit)
                if movies:
                    return movies
            except Exception as e:
                print(f"Intento {attempt + 1} falló: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(random.uniform(5, 10))
        
        return []
'''

# ========================================================================
# 4. SELECTORES ESPECÍFICOS PARA IMDB
# ========================================================================

IMDB_SELECTORS = {
    "top_250_page": {
        "url": "https://www.imdb.com/chart/top/",
        "container": ".listItem",
        "movie_title": ".titleColumn a",
        "movie_year": ".titleColumn .secondaryInfo",
        "movie_rating": ".ratingColumn strong",
        "movie_rank": ".numberColumn",
        "movie_link": ".titleColumn a::attr(href)"
    },
    
    "movie_detail_page": {
        "director": ".credit_summary_item:contains('Director') a",
        "stars": ".credit_summary_item:contains('Stars') a",
        "genres": ".subtext a[href*='genres']",
        "duration": ".subtext time",
        "metascore": ".metacriticScore span",
        "plot": ".plot_summary .summary_text",
        "poster": ".poster img::attr(src)"
    },
    
    "fallback_selectors": {
        # Selectores alternativos en caso de cambios
        "title_alt": [".titleColumn .title", ".title a", "h3.titleColumn a"],
        "year_alt": [".titleColumn .year", ".year", ".title-year"],
        "rating_alt": [".imdbRating strong", ".rating strong", ".ratingColumn .value"]
    }
}

# ========================================================================
# 5. CONFIGURACIONES DE CAPTCHA Y JAVASCRIPT
# ========================================================================

CAPTCHA_HANDLING = '''
# Para Selenium - Manejo de CAPTCHAs
def handle_captcha_selenium(driver):
    """Detectar y manejar CAPTCHAs en Selenium"""
    try:
        # Detectar presencia de CAPTCHA
        captcha_elements = [
            "//div[contains(@class, 'captcha')]",
            "//iframe[contains(@src, 'captcha')]",
            "//*[contains(text(), 'unusual traffic')]"
        ]
        
        for xpath in captcha_elements:
            if driver.find_elements(By.XPATH, xpath):
                print("CAPTCHA detectado! Esperando resolución manual...")
                input("Resuelve el CAPTCHA y presiona Enter para continuar...")
                return True
    except:
        pass
    return False

# Para Playwright - Manejo más avanzado
async def handle_javascript_challenges(page):
    """Manejar challenges de JavaScript en Playwright"""
    
    # Esperar challenges comunes
    try:
        # Detectar posibles challenges
        await page.wait_for_selector('body', timeout=5000)
        
        # Verificar si hay JavaScript blockers
        js_challenge = await page.locator('text=/checking your browser/i').count()
        if js_challenge > 0:
            print("JavaScript challenge detectado, esperando...")
            await page.wait_for_timeout(5000)
        
        # Verificar redirección a página de verificación
        current_url = page.url
        if 'security' in current_url or 'verify' in current_url:
            print("Página de verificación detectada")
            return False
        
        return True
        
    except Exception as e:
        print(f"Error manejando challenges: {e}")
        return False
'''

# ========================================================================
# 6. CONTROL DE CONCURRENCIA
# ========================================================================

CONCURRENCY_EXAMPLES = '''
# Scrapy - Concurrencia nativa con settings
SCRAPY_CONCURRENCY = {
    'CONCURRENT_REQUESTS': 1,  # Para IMDb: conservador
    'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    'DOWNLOAD_DELAY': 2,
    'RANDOMIZE_DOWNLOAD_DELAY': 0.5,
    'AUTOTHROTTLE_ENABLED': True,
    'AUTOTHROTTLE_START_DELAY': 1,
    'AUTOTHROTTLE_MAX_DELAY': 10,
    'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0
}

# Selenium - ThreadPoolExecutor
import concurrent.futures
import threading

class SeleniumConcurrency:
    def __init__(self, max_workers=2):
        self.max_workers = max_workers
        self.local_data = threading.local()
    
    def scrape_concurrent(self, urls):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(self.scrape_single_url, url) for url in urls]
            results = []
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    print(f"Error en thread: {e}")
            
            return results

# Playwright - AsyncIO nativo
import asyncio
import aiohttp

class PlaywrightConcurrency:
    async def scrape_concurrent(self, urls, max_concurrent=3):
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def scrape_with_semaphore(url):
            async with semaphore:
                return await self.scrape_single_url(url)
        
        tasks = [scrape_with_semaphore(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filtrar errores
        return [r for r in results if not isinstance(r, Exception)]
'''

def main():
    """Función principal - mostrar ejemplos"""
    import json
    
    print("🎬 Ejemplos Prácticos de Configuración para IMDb")
    print("=" * 60)
    print()
    
    examples = {
        "1. Scrapy Spider Optimizado": SCRAPY_IMDB_SPIDER,
        "2. Selenium Anti-detección": SELENIUM_IMDB_SCRAPER,
        "3. Playwright Stealth": PLAYWRIGHT_IMDB_SCRAPER,
        "4. Selectores IMDb": json.dumps(IMDB_SELECTORS, indent=2),
        "5. Manejo de CAPTCHA": CAPTCHA_HANDLING,
        "6. Control de Concurrencia": CONCURRENCY_EXAMPLES
    }
    
    print("📚 Ejemplos de código disponibles:")
    for i, title in enumerate(examples.keys(), 1):
        print(f"   {i}. {title}")
    
    print(f"\n💡 Cada ejemplo muestra configuraciones específicas para IMDb")
    print(f"📖 Revisa los archivos en examples/ para implementaciones completas")
    print(f"🚀 Usa demo_comparison.py para ver funcionamiento real")

if __name__ == '__main__':
    main()
