#!/usr/bin/env python3
"""
Implementación Práctica: Selenium para IMDb Scraping
Configuración anti-detección, proxy rotation y manejo de errores avanzado
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import random
import time
import json
import logging
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import os
from dataclasses import dataclass
import csv

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

class SeleniumIMDbScraper:
    """Scraper IMDb usando Selenium con configuración profesional"""
    
    def __init__(self, headless: bool = True, max_workers: int = 2, use_proxy: bool = False):
        self.headless = headless
        self.max_workers = max_workers
        self.use_proxy = use_proxy
        self.logger = self._setup_logger()
        
        # Configuraciones anti-detección
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        
        # Thread-local storage para drivers
        self.local_data = threading.local()
        
        # Proxies (si están disponibles)
        self.proxies = self._load_proxies() if use_proxy else []
    
    def _setup_logger(self) -> logging.Logger:
        """Configurar sistema de logging"""
        logger = logging.getLogger('selenium_scraper')
        logger.setLevel(logging.INFO)
        
        # Evitar duplicar handlers
        if logger.handlers:
            return logger
        
        os.makedirs('logs', exist_ok=True)
        
        # File handler
        file_handler = logging.FileHandler('logs/selenium_scraper.log')
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    def _load_proxies(self) -> List[Dict]:
        """Cargar lista de proxies desde configuración"""
        try:
            with open('config/proxies.json', 'r') as f:
                proxy_config = json.load(f)
                return proxy_config.get('proxies', [])
        except (FileNotFoundError, json.JSONDecodeError):
            self.logger.warning("No se pudieron cargar proxies, continuando sin proxy")
            return []
    
    def create_driver(self, proxy: Optional[Dict] = None) -> webdriver.Chrome:
        """Crear driver Chrome con configuración anti-detección completa"""
        chrome_options = Options()
        
        # Configuración básica
        if self.headless:
            chrome_options.add_argument('--headless=new')
        
        # Argumentos anti-detección extensivos
        stealth_args = [
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--disable-features=VizDisplayCompositor',
            '--disable-extensions',
            '--disable-plugins',
            '--disable-images',  # Acelerar carga
            '--disable-javascript-harmony-shipping',
            '--disable-blink-features=AutomationControlled',
            '--disable-infobars',
            '--disable-notifications',
            '--disable-popup-blocking',
            '--no-first-run',
            '--no-default-browser-check',
            '--ignore-certificate-errors',
            '--ignore-ssl-errors',
            '--ignore-certificate-errors-spki-list'
        ]
        
        for arg in stealth_args:
            chrome_options.add_argument(arg)
        
        # User agent aleatorio
        user_agent = random.choice(self.user_agents)
        chrome_options.add_argument(f'--user-agent={user_agent}')
        
        # Viewport aleatorio para parecer más humano
        viewport_width = random.randint(1200, 1920)
        viewport_height = random.randint(800, 1080)
        chrome_options.add_argument(f'--window-size={viewport_width},{viewport_height}')
        
        # Configurar proxy si está disponible
        if proxy and proxy.get('host'):
            proxy_arg = f"--proxy-server={proxy['protocol']}://{proxy['host']}:{proxy['port']}"
            chrome_options.add_argument(proxy_arg)
            self.logger.info(f"Usando proxy: {proxy['host']}:{proxy['port']}")
        
        # Desactivar banderas de automatización
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Configurar preferencias adicionales
        prefs = {
            "profile.default_content_setting_values": {
                "notifications": 2,
                "media_stream": 2,
            },
            "profile.default_content_settings.popups": 0,
            "profile.managed_default_content_settings.images": 2  # Bloquear imágenes
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        try:
            # Usar webdriver automático si está disponible
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                service = Service(ChromeDriverManager().install())
                self.logger.info("Usando ChromeDriver automático")
            except ImportError:
                # Fallback al driver del sistema
                service = Service()
                self.logger.warning("webdriver-manager no disponible, usando driver del sistema")
            
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Scripts anti-detección post-creación
            driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined,
                    });
                    
                    // Simular plugins
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5],
                    });
                    
                    // Ocultar automatización
                    window.chrome = {
                        runtime: {},
                    };
                    
                    // Remover propiedades de automatización
                    ['__driver_evaluate', '__webdriver_evaluate', '__selenium_evaluate', 
                     '__fxdriver_evaluate', '__driver_unwrapped', '__webdriver_unwrapped', 
                     '__selenium_unwrapped', '__fxdriver_unwrapped'].forEach(prop => {
                        delete window[prop];
                    });
                '''
            })
            
            # Configurar timeouts
            driver.implicitly_wait(10)
            driver.set_page_load_timeout(30)
            
            # Agregar retardo humano inicial
            time.sleep(random.uniform(1, 3))
            
            self.logger.info("Driver Chrome creado exitosamente con anti-detección")
            return driver
            
        except Exception as e:
            self.logger.error(f"Error creando driver: {e}")
            raise
    
    def get_driver(self) -> webdriver.Chrome:
        """Obtener driver del thread local storage"""
        if not hasattr(self.local_data, 'driver') or self.local_data.driver is None:
            proxy = random.choice(self.proxies) if self.proxies else None
            self.local_data.driver = self.create_driver(proxy)
        return self.local_data.driver
    
    def close_driver(self):
        """Cerrar driver del thread actual"""
        if hasattr(self.local_data, 'driver') and self.local_data.driver:
            try:
                self.local_data.driver.quit()
            except Exception:
                pass
            self.local_data.driver = None
    
    def scrape_movie_details(self, movie_element, rank: int) -> Optional[MovieData]:
        """Extraer detalles de una película específica"""
        try:
            # Título
            title_elem = movie_element.find_element(
                By.CSS_SELECTOR, 
                '.titleColumn a, .cli-title a, h3.titleColumn a'
            )
            title = title_elem.text.strip()
            
            # Año
            year_elem = movie_element.find_element(
                By.CSS_SELECTOR, 
                '.titleColumn .secondaryInfo, .cli-title .secondaryInfo'
            )
            year_text = year_elem.text.strip('()')
            year = int(year_text) if year_text.isdigit() else 0
            
            # Rating
            rating_elem = movie_element.find_element(
                By.CSS_SELECTOR, 
                '.ratingColumn strong, .imdbRating strong'
            )
            rating = float(rating_elem.text.strip())
            
            # Intentar obtener información adicional (opcional)
            director = ""
            stars = []
            genre = []
            duration = ""
            
            try:
                # Buscar enlace de detalles y hacer click si es necesario
                detail_link = title_elem.get_attribute('href')
                if detail_link:
                    # Por ahora solo extraemos lo básico para evitar complejidad
                    pass
            except Exception:
                pass
            
            movie_data = MovieData(
                rank=rank,
                title=title,
                year=year,
                rating=rating,
                director=director,
                stars=stars,
                genre=genre,
                duration=duration
            )
            
            self.logger.debug(f"Extraída película: {title} ({year}) - {rating}")
            return movie_data
            
        except Exception as e:
            self.logger.error(f"Error extrayendo película rank {rank}: {e}")
            return None
    
    def scrape_page(self, page_url: str, max_retries: int = 3) -> List[MovieData]:
        """Scrapeado de una página con manejo de errores"""
        driver = self.get_driver()
        movies = []
        
        for attempt in range(max_retries):
            try:
                self.logger.info(f"Cargando página: {page_url} (intento {attempt + 1})")
                
                # Navegar a la página
                driver.get(page_url)
                
                # Esperar que la página cargue
                wait = WebDriverWait(driver, 20)
                wait.until(EC.presence_of_element_located((
                    By.CSS_SELECTOR, 
                    '.listItem, .titleColumn, .cli-item'
                )))
                
                # Retardo humano
                time.sleep(random.uniform(2, 5))
                
                # Encontrar elementos de películas
                movie_elements = driver.find_elements(
                    By.CSS_SELECTOR, 
                    '.listItem, .titleColumn, .cli-item'
                )
                
                self.logger.info(f"Encontrados {len(movie_elements)} elementos de películas")
                
                # Extraer datos de cada película
                for i, movie_elem in enumerate(movie_elements, 1):
                    movie_data = self.scrape_movie_details(movie_elem, i)
                    if movie_data:
                        movies.append(movie_data)
                        
                        # Retardo entre extracciones
                        time.sleep(random.uniform(0.5, 1.5))
                
                self.logger.info(f"Extraídas {len(movies)} películas exitosamente")
                break  # Éxito, salir del loop de reintentos
                
            except TimeoutException:
                self.logger.warning(f"Timeout en intento {attempt + 1}")
                if attempt == max_retries - 1:
                    self.logger.error("Timeout final, abandonando página")
                else:
                    time.sleep(random.uniform(5, 10))
                    
            except Exception as e:
                self.logger.error(f"Error en intento {attempt + 1}: {e}")
                if attempt == max_retries - 1:
                    self.logger.error("Error final, abandonando página")
                else:
                    time.sleep(random.uniform(3, 7))
        
        return movies
    
    def scrape_top_movies(self, limit: int = 50) -> List[MovieData]:
        """Scraping principal de top movies"""
        self.logger.info(f"🎬 Iniciando scraping de top {limit} películas con Selenium")
        
        # URL de IMDb Top 250
        base_url = "https://www.imdb.com/chart/top/"
        
        try:
            all_movies = self.scrape_page(base_url)
            
            # Limitar resultados
            limited_movies = all_movies[:limit]
            
            self.logger.info(f"✅ Scraping completado: {len(limited_movies)} películas")
            return limited_movies
            
        except Exception as e:
            self.logger.error(f"❌ Error en scraping principal: {e}")
            return []
        finally:
            self.close_driver()
    
    def save_to_csv(self, movies: List[MovieData], filename: str = "selenium_movies.csv"):
        """Guardar películas en archivo CSV"""
        if not movies:
            self.logger.warning("No hay películas para guardar")
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
            self.logger.error(f"Error guardando CSV: {e}")
    
    def run_benchmark(self, limit: int = 25) -> Dict:
        """Ejecutar benchmark de rendimiento"""
        import psutil
        
        self.logger.info(f"🚀 Iniciando benchmark Selenium con {limit} películas")
        
        # Medición inicial
        process = psutil.Process()
        memory_before = process.memory_info().rss / 1024 / 1024
        start_time = time.time()
        
        # Ejecutar scraping
        movies = self.scrape_top_movies(limit)
        
        # Medición final
        end_time = time.time()
        memory_after = process.memory_info().rss / 1024 / 1024
        
        execution_time = end_time - start_time
        memory_used = memory_after - memory_before
        
        # Guardar resultados
        output_file = f"selenium_benchmark_{limit}.csv"
        self.save_to_csv(movies, output_file)
        
        metrics = {
            'tool': 'selenium',
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


def main():
    """Función principal para testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Selenium IMDb Scraper')
    parser.add_argument('--limit', type=int, default=10, help='Número de películas a extraer')
    parser.add_argument('--headless', action='store_true', help='Ejecutar en modo headless')
    parser.add_argument('--proxy', action='store_true', help='Usar proxies')
    parser.add_argument('--benchmark', action='store_true', help='Ejecutar benchmark')
    
    args = parser.parse_args()
    
    scraper = SeleniumIMDbScraper(
        headless=args.headless,
        use_proxy=args.proxy
    )
    
    try:
        if args.benchmark:
            metrics = scraper.run_benchmark(args.limit)
            print(f"\n📊 Resultados del benchmark:")
            print(f"   Películas: {metrics['items_scraped']}/{metrics['items_target']}")
            print(f"   Tiempo: {metrics['execution_time_seconds']}s")
            print(f"   Memoria: {metrics['memory_used_mb']:.1f}MB")
            print(f"   Velocidad: {metrics['items_per_second']:.1f} items/s")
        else:
            movies = scraper.scrape_top_movies(args.limit)
            scraper.save_to_csv(movies)
            print(f"\n🎉 Scraping completado: {len(movies)} películas extraídas")
    
    except KeyboardInterrupt:
        print("\n⚠️  Scraping interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == '__main__':
    main()
