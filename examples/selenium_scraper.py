#!/usr/bin/env python3
"""
Implementación práctica con Selenium para IMDb Scraper
Configuración anti-detección y control de concurrencia con ThreadPoolExecutor
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import random
import time
import json
import logging
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import os

class SeleniumIMDbScraper:
    """Scraper IMDb usando Selenium con configuración anti-detección"""
    
    def __init__(self, headless: bool = True, max_workers: int = 3):
        self.headless = headless
        self.max_workers = max_workers
        self.logger = self._setup_logger()
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        
        # Thread-local storage para drivers
        self.local_data = threading.local()
    
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger('selenium_scraper')
        logger.setLevel(logging.INFO)
        
        os.makedirs('logs', exist_ok=True)
        handler = logging.FileHandler('logs/selenium_scraper.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def create_driver(self) -> webdriver.Chrome:
        """Crear driver Chrome con configuración anti-detección"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless=new')
        
        # Argumentos anti-detección
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')
        chrome_options.add_argument(f'--user-agent={random.choice(self.user_agents)}')
        
        # Desactivar automatización flags
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Configurar viewport aleatorio
        viewport_width = random.randint(1200, 1920)
        viewport_height = random.randint(800, 1080)
        chrome_options.add_argument(f'--window-size={viewport_width},{viewport_height}')
        
        # Crear driver usando webdriver-manager
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())
        except ImportError:
            # Fallback si webdriver-manager no está disponible
            self.logger.warning("webdriver-manager no disponible, usando ChromeDriver del sistema")
            service = Service()
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Ejecutar script anti-detección
        driver.execute_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
        });
        """)
        
        # Configurar timeouts
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(30)
        
        self.logger.info("Driver Chrome creado con anti-detección")
        return driver
    
    def get_driver(self) -> webdriver.Chrome:
        """Obtener driver thread-local"""
        if not hasattr(self.local_data, 'driver'):
            self.local_data.driver = self.create_driver()
        return self.local_data.driver
    
    def wait_for_element_with_retries(self, driver: webdriver.Chrome, 
                                    locator: tuple, timeout: int = 10, 
                                    retries: int = 3):
        """Espera explícita con reintentos"""
        for attempt in range(retries):
            try:
                element = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located(locator)
                )
                return element
            except TimeoutException:
                if attempt < retries - 1:
                    self.logger.warning(f"Reintento {attempt + 1} para {locator}")
                    time.sleep(2)
                    driver.refresh()
                else:
                    raise
    
    def handle_captcha_detection(self, driver: webdriver.Chrome) -> bool:
        """Detectar y manejar CAPTCHAs"""
        captcha_indicators = [
            (By.XPATH, "//*[contains(@class, 'captcha')]"),
            (By.XPATH, "//*[contains(@id, 'captcha')]"),
            (By.TAG_NAME, "iframe[src*='recaptcha']")
        ]
        
        for locator in captcha_indicators:
            try:
                driver.find_element(*locator)
                self.logger.warning("CAPTCHA detectado")
                
                # Estrategia: Esperar resolución manual
                self.logger.info("Esperando resolución manual de CAPTCHA (60s)")
                time.sleep(60)
                
                return True
            except NoSuchElementException:
                continue
        
        return False
    
    def extract_movie_data_robust(self, driver: webdriver.Chrome, movie_url: str) -> Dict:
        """Extraer datos con selectores robustos y fallbacks"""
        try:
            driver.get(movie_url)
            
            # Verificar CAPTCHA
            self.handle_captcha_detection(driver)
            
            # Selectores múltiples para cada campo
            title_selectors = [
                (By.CSS_SELECTOR, 'h1[data-testid="hero-title-block__title"]'),
                (By.CSS_SELECTOR, '.title_wrapper h1'),
                (By.XPATH, "//h1[contains(@class, 'titleHeader')]")
            ]
            
            year_selectors = [
                (By.CSS_SELECTOR, '[data-testid="hero-title-block__metadata"] a'),
                (By.CSS_SELECTOR, '.titleBar__metadata a'),
                (By.XPATH, "//span[@class='year']")
            ]
            
            rating_selectors = [
                (By.CSS_SELECTOR, '[data-testid="hero-rating-bar__aggregate-rating__score"] span'),
                (By.CSS_SELECTOR, '.ratingValue strong span'),
                (By.XPATH, "//span[@itemprop='ratingValue']")
            ]
            
            # Extraer datos con fallbacks
            movie_data = {
                'title': self._extract_text_with_fallbacks(driver, title_selectors),
                'year': self._extract_text_with_fallbacks(driver, year_selectors),
                'rating': self._extract_text_with_fallbacks(driver, rating_selectors),
                'duration': self._extract_duration(driver),
                'metascore': self._extract_metascore(driver),
                'cast': self._extract_cast(driver)
            }
            
            self.logger.info(f"Extraído: {movie_data['title']}")
            return movie_data
            
        except Exception as e:
            self.logger.error(f"Error extrayendo {movie_url}: {e}")
            return {}
    
    def _extract_text_with_fallbacks(self, driver: webdriver.Chrome, 
                                   selectors: List[tuple]) -> str:
        """Extraer texto usando múltiples selectores de fallback"""
        for locator in selectors:
            try:
                element = driver.find_element(*locator)
                text = element.text.strip()
                if text:
                    return text
            except NoSuchElementException:
                continue
        return 'N/A'
    
    def _extract_duration(self, driver: webdriver.Chrome) -> str:
        """Extraer duración con múltiples estrategias"""
        duration_selectors = [
            (By.CSS_SELECTOR, '[data-testid="title-techspec_runtime"]'),
            (By.CSS_SELECTOR, 'time[datetime]'),
            (By.XPATH, "//time[contains(@datetime, 'PT')]")
        ]
        return self._extract_text_with_fallbacks(driver, duration_selectors)
    
    def _extract_metascore(self, driver: webdriver.Chrome) -> str:
        """Extraer Metascore"""
        metascore_selectors = [
            (By.CSS_SELECTOR, '[data-testid="meta-score"]'),
            (By.CSS_SELECTOR, '.metacriticScore span'),
            (By.XPATH, "//div[contains(@class, 'metacriticScore')]//span")
        ]
        return self._extract_text_with_fallbacks(driver, metascore_selectors)
    
    def _extract_cast(self, driver: webdriver.Chrome) -> str:
        """Extraer elenco principal"""
        try:
            cast_selectors = [
                (By.CSS_SELECTOR, '[data-testid="title-cast-item"] a'),
                (By.CSS_SELECTOR, '.cast_list .primary_photo + td a')
            ]
            
            for locator in cast_selectors:
                try:
                    elements = driver.find_elements(*locator)[:3]  # Top 3
                    if elements:
                        cast_names = [elem.text.strip() for elem in elements if elem.text.strip()]
                        return ', '.join(cast_names)
                except NoSuchElementException:
                    continue
            
            return 'N/A'
        except Exception:
            return 'N/A'
    
    def scrape_single_movie(self, movie_url: str) -> Dict:
        """Scraper de película individual para threading"""
        driver = self.get_driver()
        
        try:
            movie_data = self.extract_movie_data_robust(driver, movie_url)
            
            # Delay aleatorio para parecer humano
            time.sleep(random.uniform(1, 3))
            
            return movie_data
        except Exception as e:
            self.logger.error(f"Error en thread para {movie_url}: {e}")
            return {}
    
    def scrape_top_movies_concurrent(self, limit: int = 10) -> List[Dict]:
        """Scraper principal con control de concurrencia usando ThreadPoolExecutor"""
        movies = []
        
        # Obtener URLs principales
        main_driver = self.create_driver()
        
        try:
            main_driver.get("https://www.imdb.com/chart/top/")
            
            # Manejar CAPTCHA si aparece
            self.handle_captcha_detection(main_driver)
            
            # Esperar elementos de película
            self.wait_for_element_with_retries(main_driver, (By.CSS_SELECTOR, '.cli-item'))
            
            # Extraer URLs
            movie_elements = main_driver.find_elements(By.CSS_SELECTOR, '.cli-item .cli-title a')
            movie_urls = []
            
            for element in movie_elements[:limit]:
                href = element.get_attribute('href')
                if href:
                    movie_urls.append(f"https://www.imdb.com{href}")
            
            self.logger.info(f"Encontradas {len(movie_urls)} URLs")
            
        finally:
            main_driver.quit()
        
        # Procesar con ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Enviar tasks
            future_to_url = {
                executor.submit(self.scrape_single_movie, url): url 
                for url in movie_urls
            }
            
            # Recoger resultados
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    movie_data = future.result()
                    if movie_data:
                        movies.append(movie_data)
                except Exception as e:
                    self.logger.error(f"Error procesando {url}: {e}")
        
        # Cleanup drivers
        self._cleanup_drivers()
        
        self.logger.info(f"Scraping completado: {len(movies)} películas")
        return movies
    
    def _cleanup_drivers(self):
        """Limpiar drivers de todos los threads"""
        if hasattr(self.local_data, 'driver'):
            try:
                self.local_data.driver.quit()
            except:
                pass

# Función principal
def main():
    """Ejecutar scraper Selenium"""
    print("🔧 Iniciando Selenium IMDb Scraper...")
    
    scraper = SeleniumIMDbScraper(headless=True, max_workers=2)
    movies = scraper.scrape_top_movies_concurrent(limit=10)
    
    # Guardar resultados
    os.makedirs('data/exports', exist_ok=True)
    with open('data/exports/selenium_movies.json', 'w') as f:
        json.dump(movies, f, indent=2)
    
    print(f"✅ Extraídas {len(movies)} películas con Selenium")
    
    # Mostrar ejemplo de resultado
    if movies:
        print(f"🎬 Ejemplo: {movies[0]['title']} ({movies[0]['year']}) - {movies[0]['rating']}")

if __name__ == "__main__":
    main()
