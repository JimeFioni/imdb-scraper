import scrapy
import re
from urllib.parse import urljoin
from imdb_scraper.items import ImdbScraperItem
from imdb_scraper.selector_factory import DataExtractor


class TopMoviesSpider(scrapy.Spider):
    name = 'top_movies'
    allowed_domains = ['imdb.com']
    # Remover start_urls y usar start_requests en su lugar
    
    # Custom headers y cookies
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        },
        'COOKIES_ENABLED': True,
        'COOKIES_DEBUG': True,
    }
    
    def start_requests(self):
        """Iniciar directamente con el método de 50 películas"""
        self.logger.info("🚀 Iniciando scraping directo de películas")
        yield from self.parse_top_50()
    
    # Top 50 movie IDs para método alternativo
    TOP_50_MOVIE_IDS = [
        'tt0111161', 'tt0068646', 'tt0468569', 'tt0071562', 'tt0050083',
        'tt0167260', 'tt0108052', 'tt0110912', 'tt0120737', 'tt0060196',
        'tt0109830', 'tt0167261', 'tt0137523', 'tt1375666', 'tt0080684',
        'tt0133093', 'tt0099685', 'tt0816692', 'tt0073486', 'tt0114369',
        'tt0038650', 'tt0102926', 'tt0047478', 'tt0120815', 'tt0120689',
        'tt0317248', 'tt0034583', 'tt0095327', 'tt0120586', 'tt0054215',
        'tt0078788', 'tt0095765', 'tt0253474', 'tt0405094', 'tt0027977',
        'tt0064116', 'tt0078748', 'tt0021749', 'tt0025316', 'tt0103064',
        'tt0056058', 'tt0086190', 'tt0031679', 'tt0082971', 'tt0070735',
        'tt0057012', 'tt0088763', 'tt0172495', 'tt0110413', 'tt0062622'
    ]

    def parse_top_50(self):
        """Método alternativo que obtiene las top 50 películas directamente"""
        base_url = "https://www.imdb.com/title/"
        
        # Usar todas las 50 películas
        for i, movie_id in enumerate(self.TOP_50_MOVIE_IDS, 1):
            url = f"{base_url}{movie_id}/"
            self.logger.info(f"🎬 Procesando película {i}: {url}")
            
            # Headers más convincentes para evitar bloqueos
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://www.imdb.com/chart/top/',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
            }
            
            yield scrapy.Request(
                url, 
                callback=self.parse_detail,
                headers=headers,
                meta={'rank': i},
                dont_filter=True
            )

    def parse_detail(self, response):
        """Extrae datos de una película usando el patrón Factory"""
        try:
            item = ImdbScraperItem()
            
            # Ranking de la película
            rank = response.meta.get('rank', 0)
            item['ranking'] = rank
            
            # Usar el Factory Pattern para extraer datos
            extractor = DataExtractor(response)
            data = extractor.extract_all_data()
            
            # Asignar datos extraídos con validación
            item['titulo'] = self._validate_string(data.get('titulo', ''))
            item['anio'] = self._validate_year(data.get('anio'))
            item['calificacion'] = self._validate_rating(data.get('calificacion'))
            item['duracion'] = self._validate_string(data.get('duracion'))
            item['metascore'] = self._validate_metascore(data.get('metascore'))
            item['actores'] = self._validate_actors(data.get('actores', []))
            
            self.logger.info(f"✅ Extraído: {item['titulo']} ({item['anio']}) - Rating: {item['calificacion']}")
            
            yield item
            
        except Exception as e:
            self.logger.error(f"❌ Error procesando {response.url}: {str(e)}")
            # Yield item vacío para mantener estadísticas
            yield ImdbScraperItem()
    
    def _validate_string(self, value):
        """Valida y limpia strings"""
        try:
            return str(value).strip() if value else ''
        except Exception:
            return ''
    
    def _validate_year(self, value):
        """Valida año"""
        try:
            if value and str(value).isdigit() and 1900 <= int(value) <= 2030:
                return value
            return None
        except Exception:
            return None
    
    def _validate_rating(self, value):
        """Valida rating"""
        try:
            if value:
                rating = float(str(value).replace(',', '.'))
                if 0 <= rating <= 10:
                    return str(rating)
            return None
        except Exception:
            return None
    
    def _validate_metascore(self, value):
        """Valida metascore"""
        try:
            if value and str(value).isdigit():
                score = int(value)
                if 0 <= score <= 100:
                    return str(score)
            return None
        except Exception:
            return None
    
    def _validate_actors(self, actors_list):
        """Valida lista de actores"""
        try:
            if isinstance(actors_list, list) and actors_list:
                # Filtrar actores válidos y tomar los primeros 3
                valid_actors = [actor.strip() for actor in actors_list if actor and actor.strip()][:3]
                return valid_actors if valid_actors else []
            return []
        except Exception:
            return []


