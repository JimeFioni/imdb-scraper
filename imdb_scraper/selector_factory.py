"""
Patrón Factory para crear selectores de datos de películas
Permite manejar diferentes versiones de la página de IMDb de manera modular
"""

from abc import ABC, abstractmethod
import re


class SelectorStrategy(ABC):
    """Estrategia abstracta para selección de datos"""
    
    @abstractmethod
    def extract_title(self, response):
        pass
    
    @abstractmethod
    def extract_year(self, response):
        pass
    
    @abstractmethod
    def extract_rating(self, response):
        pass
    
    @abstractmethod
    def extract_duration(self, response):
        pass
    
    @abstractmethod
    def extract_metascore(self, response):
        pass
    
    @abstractmethod
    def extract_actors(self, response):
        pass


class ModernIMDbSelector(SelectorStrategy):
    """Selector para la versión moderna de IMDb (2024+)"""
    
    def extract_title(self, response):
        return (
            response.css('h1[data-testid="hero__pageTitle"] span::text').get() or
            response.css('h1.sc-b73cd867-0::text').get() or
            response.css('h1::text').get() or
            ''
        ).strip()
    
    def extract_year(self, response):
        year_text = response.css('ul.ipc-inline-list a::text').re_first(r'(\d{4})')
        if not year_text:
            year_text = response.css('span.sc-8c396aa2-2::text').re_first(r'(\d{4})')
        return year_text
    
    def extract_rating(self, response):
        return (
            response.css('span[class*="rating"]::text').get() or
            response.css('div[data-testid="hero-rating-bar__aggregate-rating"] span::text').get() or
            response.css('span.ipc-rating-star--rating::text').get()
        )
    
    def extract_duration(self, response):
        duration_texts = response.css('ul.ipc-inline-list li::text').getall()
        for text in duration_texts:
            if 'h' in text and 'm' in text:
                return text.strip()
            elif 'min' in text:
                return text.strip()
        return None
    
    def extract_metascore(self, response):
        return (
            response.css('span.score-meta::text').get() or
            response.css('span[class*="metacritic-score"]::text').get()
        )
    
    def extract_actors(self, response):
        actor_links = (
            response.css('a[data-testid="title-cast-item__actor"]::text').getall() or
            response.css('li[data-testid="title-cast-item"] a::text').getall() or
            response.css('ul.cast_list a[href*="/name/"]::text').getall()
        )
        return [actor.strip() for actor in actor_links if actor.strip()][:3]


class LegacyIMDbSelector(SelectorStrategy):
    """Selector para versión legacy de IMDb (fallback)"""
    
    def extract_title(self, response):
        return (
            response.css('h1.header::text').get() or
            response.css('.title_wrapper h1::text').get() or
            response.css('h1::text').get() or
            ''
        ).strip()
    
    def extract_year(self, response):
        return response.css('h1 .nobr::text').re_first(r'(\d{4})')
    
    def extract_rating(self, response):
        return response.css('.ratingValue span::text').get()
    
    def extract_duration(self, response):
        duration = response.css('.subtext time::text').get()
        return duration.strip() if duration else None
    
    def extract_metascore(self, response):
        return response.css('.metacriticScore span::text').get()
    
    def extract_actors(self, response):
        actors = response.css('.cast_list .primary_photo+ td a::text').getall()
        return [actor.strip() for actor in actors if actor.strip()][:3]


class SelectorFactory:
    """Factory para crear selectores apropiados según la página"""
    
    @staticmethod
    def create_selector(response):
        """
        Crea el selector apropiado basado en la estructura de la página
        
        Args:
            response: Respuesta de Scrapy
            
        Returns:
            SelectorStrategy: Instancia del selector apropiado
        """
        try:
            # Detectar si es la versión moderna checkeando elementos específicos
            if response.css('h1[data-testid="hero__pageTitle"]'):
                return ModernIMDbSelector()
            elif response.css('.ratingValue'):
                return LegacyIMDbSelector()
            else:
                # Default a moderno
                return ModernIMDbSelector()
        except Exception:
            # En caso de error, usar moderno por defecto
            return ModernIMDbSelector()


class DataExtractor:
    """Extractor de datos que utiliza el patrón Factory"""
    
    def __init__(self, response):
        self.response = response
        self.selector = SelectorFactory.create_selector(response)
    
    def extract_all_data(self):
        """Extrae todos los datos de la película usando el selector apropiado"""
        try:
            return {
                'titulo': self.selector.extract_title(self.response),
                'anio': self.selector.extract_year(self.response),
                'calificacion': self.selector.extract_rating(self.response),
                'duracion': self.selector.extract_duration(self.response),
                'metascore': self.selector.extract_metascore(self.response),
                'actores': self.selector.extract_actors(self.response)
            }
        except Exception as e:
            return {
                'titulo': '',
                'anio': None,
                'calificacion': None,
                'duracion': None,
                'metascore': None,
                'actores': []
            }
