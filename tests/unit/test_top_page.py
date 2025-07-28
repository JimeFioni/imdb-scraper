#!/usr/bin/env python3
"""
Script para probar selectores en la página principal de IMDb Top 250
"""

import requests
from parsel import Selector

def test_top_page_selectors():
    # URL de la página top 250
    url = "https://www.imdb.com/chart/top/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    print(f"🔍 Probando selectores en: {url}")
    
    response = requests.get(url, headers=headers)
    selector = Selector(text=response.text)
    
    print("\n📊 SELECTORES PARA PELÍCULAS:")
    movie_selectors = [
        'li.ipc-metadata-list-summary-item',
        'td.titleColumn',
        'li.titleColumn',
        'div.titleColumn', 
        'h3.titleColumn',
        'li[class*="metadata-list-summary-item"]',
        'li[class*="list-summary-item"]',
        'div[class*="cli-title"]'
    ]
    
    for selector_str in movie_selectors:
        results = selector.css(selector_str)
        print(f"  {selector_str:<50} -> {len(results)} elementos")
        
        # Si encontramos elementos, probar a extraer algunos títulos
        if len(results) > 0:
            print(f"    Primeros 5 títulos:")
            for i, item in enumerate(results[:5]):
                # Probar diferentes selectores para el título
                title = (
                    item.css('h3.ipc-title__text::text').get() or
                    item.css('a::text').get() or
                    item.css('h3::text').get() or
                    'No title found'
                )
                print(f"      {i+1}. {title}")
    
    print(f"\n📄 Guardando HTML para inspección manual...")
    with open('top_page_debug.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    print("✅ Archivo guardado como: top_page_debug.html")

if __name__ == "__main__":
    test_top_page_selectors()
