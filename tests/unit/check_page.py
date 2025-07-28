#!/usr/bin/env python3
"""
Script para revisar si hay más películas en la página
"""

import requests
from parsel import Selector

def check_full_page():
    url = "https://www.imdb.com/chart/top/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    response = requests.get(url, headers=headers)
    selector = Selector(text=response.text)
    
    print(f"🔍 Analizando la página completa: {url}")
    
    # Buscar todos los elementos de película posibles
    selectors_to_try = [
        'li.ipc-metadata-list-summary-item',
        'tr',
        'td.titleColumn',
        'div[class*="title"]',
        'a[href*="/title/tt"]'
    ]
    
    for selector_str in selectors_to_try:
        elements = selector.css(selector_str)
        print(f"  {selector_str:<40} -> {len(elements)} elementos")
    
    # Buscar indicadores de paginación o carga
    pagination_selectors = [
        'button[class*="load"]',
        'button[class*="more"]', 
        'a[class*="next"]',
        'div[class*="pagination"]',
        'span[class*="page"]'
    ]
    
    print(f"\n📄 Buscando controles de paginación:")
    for selector_str in pagination_selectors:
        elements = selector.css(selector_str)
        if elements:
            print(f"  ✅ {selector_str}: {len(elements)} elementos")
            for elem in elements[:3]:
                text = elem.css('::text').get() or elem.css('::attr(title)').get() or 'Sin texto'
                print(f"     -> {text}")
        else:
            print(f"  ❌ {selector_str}: No encontrado")
    
    # Buscar si hay información sobre total de películas
    print(f"\n🔢 Buscando información de total:")
    total_indicators = selector.css('*::text').re(r'.*(\d+).*movies?.*|.*total.*(\d+).*|.*showing.*(\d+).*')
    for indicator in total_indicators[:5]:
        print(f"  -> {indicator}")
    
    # Verificar si la página actual muestra solo las primeras 25 o 50
    movie_numbers = selector.css('*::text').re(r'^(\d+)\.$')
    print(f"\n🎬 Números de películas encontrados: {movie_numbers[:10]} {'...' if len(movie_numbers) > 10 else ''}")
    if movie_numbers:
        print(f"     Último número: {max([int(x) for x in movie_numbers if x.isdigit()])}")

if __name__ == "__main__":
    check_full_page()
