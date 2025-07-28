#!/usr/bin/env python3
"""
Script para probar el selector cli-title que detecta 50 películas
"""

import requests
from parsel import Selector

def test_cli_title_selector():
    # URL de la página top 250
    url = "https://www.imdb.com/chart/top/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    response = requests.get(url, headers=headers)
    selector = Selector(text=response.text)
    
    # Probar el selector que encuentra 50 elementos
    elements = selector.css('div[class*="cli-title"]')
    print(f"🎬 Encontrados {len(elements)} elementos con 'cli-title'")
    
    # Analizar la estructura
    movies_found = 0
    for i, element in enumerate(elements):
        # Buscar enlaces a películas
        link = element.css('a[href*="/title/"]::attr(href)').get()
        title = element.css('h3::text').get() or element.css('a::text').get()
        
        if link and title:
            movies_found += 1
            if movies_found <= 10:  # Mostrar solo las primeras 10
                print(f"  {movies_found:2d}. {title:<40} -> {link}")
    
    print(f"\n✅ Total de películas válidas encontradas: {movies_found}")
    
    # Probar selector alternativo más específico
    print(f"\n🔍 Probando selectores más específicos:")
    
    alt_selectors = [
        'li.ipc-metadata-list-summary-item a[href*="/title/"]',
        'div[class*="cli-title"] a[href*="/title/"]',
        'li.ipc-metadata-list-summary-item .ipc-title-link-wrapper',
        'div[class*="cli-title"] .ipc-title-link-wrapper'
    ]
    
    for selector_str in alt_selectors:
        results = selector.css(selector_str)
        print(f"  {selector_str:<50} -> {len(results)} enlaces")

if __name__ == "__main__":
    test_cli_title_selector()
