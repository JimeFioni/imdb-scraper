import scrapy
import re
from urllib.parse import urljoin
from imdb_scraper.items import ImdbScraperItem


class TopMoviesSpider(scrapy.Spider):
    name = 'top_movies'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/chart/top/']
    
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

    def parse(self, response):
        # Forzar el uso del método de 50 películas directamente
        self.logger.info("🚀 Usando método directo para 50 películas")
        yield from self.parse_top_50()
    
    def parse_top_50(self):
        """Método alternativo que obtiene las top 50 películas directamente"""
        base_url = "https://www.imdb.com/title/"
        
        for i, movie_id in enumerate(self.TOP_50_MOVIE_IDS, 1):
            url = f"{base_url}{movie_id}/"
            self.logger.info(f"🎬 Procesando película {i}: {url}")
            yield scrapy.Request(
                url, 
                callback=self.parse_detail,
                meta={'rank': i}
            )

    def parse_detail(self, response):
        item = ImdbScraperItem()
        
        # Ranking de la película
        rank = response.meta.get('rank', 0)
        item['ranking'] = rank
        
        # Título - múltiples selectores para mayor compatibilidad
        titulo = (
            response.css('h1[data-testid="hero__pageTitle"] span::text').get() or
            response.css('h1.sc-b73cd867-0::text').get() or
            response.css('h1::text').get() or
            ''
        ).strip()
        item['titulo'] = titulo
        
        # Año - buscar en metadatos
        year_text = response.css('ul.ipc-inline-list a::text').re_first(r'(\d{4})')
        if not year_text:
            year_text = response.css('span.sc-8c396aa2-2::text').re_first(r'(\d{4})')
        item['anio'] = year_text
        
        # Calificación (rating) - selectores que funcionan
        rating = (
            response.css('span[class*="rating"]::text').get() or
            response.css('div[data-testid="hero-rating-bar__aggregate-rating"] span::text').get() or
            response.css('span.ipc-rating-star--rating::text').get()
        )
        item['calificacion'] = rating
        
        # Duración - selector que funciona
        duration_texts = response.css('ul.ipc-inline-list li::text').getall()
        duration = None
        for text in duration_texts:
            if 'h' in text and 'm' in text:
                # Formato "2h 22m"
                duration = text.strip()
                break
            elif 'min' in text:
                # Formato "142 min"
                duration = text.strip()
                break
        item['duracion'] = duration
        
        # Metascore
        metascore = response.css('span.score-meta::text').get()
        if not metascore:
            metascore = response.css('span[class*="metacritic-score"]::text').get()
        item['metascore'] = metascore
        
        # Actores principales - buscar en el reparto
        actores = []
        
        # Múltiples selectores para actores
        actor_links = (
            response.css('a[data-testid="title-cast-item__actor"]::text').getall() or
            response.css('li[data-testid="title-cast-item"] a::text').getall() or
            response.css('ul.cast_list a[href*="/name/"]::text').getall()
        )
        
        # Limpiar y tomar los primeros 3 actores
        actores = [actor.strip() for actor in actor_links if actor.strip()][:3]
        item['actores'] = actores
        
        self.logger.info(f"✅ Extraído: {titulo} ({year_text}) - Rating: {rating}")
        
        yield item


