#!/usr/bin/env python3
"""
Script para probar diferentes URLs de IMDb Top 250
"""

import requests
from parsel import Selector

def test_different_urls():
    urls_to_try = [
        "https://www.imdb.com/chart/top/",
        "https://www.imdb.com/chart/top/?ref_=nv_mv_250",
        "https://www.imdb.com/chart/top250/",
        "https://m.imdb.com/chart/top/",
        "https://www.imdb.com/chart/top?sort=ir,desc&mode=simple&page=1"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    for url in urls_to_try:
        try:
            print(f"\n🔍 Probando: {url}")
            response = requests.get(url, headers=headers)
            selector = Selector(text=response.text)
            
            # Contar elementos de película
            items = selector.css('li.ipc-metadata-list-summary-item')
            links = selector.css('a[href*="/title/tt"]')
            
            print(f"  📊 Status: {response.status_code}")
            print(f"  🎬 Items de película: {len(items)}")
            print(f"  🔗 Enlaces de película: {len(links)}")
            
            # Buscar títulos para verificar contenido
            titles = []
            for item in items[:5]:
                title = item.css('h3.ipc-title__text::text').get() or "No title"
                titles.append(title)
            
            if titles:
                print(f"  📝 Primeros títulos:")
                for i, title in enumerate(titles, 1):
                    print(f"     {i}. {title}")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")

if __name__ == "__main__":
    test_different_urls()
