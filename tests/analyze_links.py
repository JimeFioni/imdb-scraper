#!/usr/bin/env python3
"""
Script para analizar los enlaces duplicados
"""

import requests
from parsel import Selector

def analyze_duplicate_links():
    url = "https://www.imdb.com/chart/top/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    response = requests.get(url, headers=headers)
    selector = Selector(text=response.text)
    
    # Obtener todos los enlaces
    links = selector.css('li.ipc-metadata-list-summary-item a[href*="/title/"]::attr(href)').getall()
    
    print(f"🔍 Total de enlaces encontrados: {len(links)}")
    
    # Analizar duplicados
    unique_links = []
    seen = set()
    
    for i, link in enumerate(links):
        clean_link = link.split('?')[0]  # Remover parámetros de query
        movie_id = clean_link.split('/')[-2] if '/title/' in clean_link else clean_link
        
        if movie_id not in seen:
            seen.add(movie_id)
            unique_links.append(clean_link)
            if len(unique_links) <= 10:
                print(f"  {len(unique_links):2d}. {movie_id} -> {clean_link}")
        else:
            if len(unique_links) <= 10:
                print(f"     Duplicado: {movie_id}")
    
    print(f"\n✅ Enlaces únicos: {len(unique_links)}")
    
    # Probar selector más específico
    print(f"\n🔍 Probando selector con primer enlace por elemento:")
    items = selector.css('li.ipc-metadata-list-summary-item')
    unique_count = 0
    
    for item in items:
        first_link = item.css('a[href*="/title/"]::attr(href)').get()
        if first_link:
            unique_count += 1
            if unique_count <= 10:
                movie_id = first_link.split('/')[-2] if '/title/' in first_link else 'unknown'
                print(f"  {unique_count:2d}. {movie_id} -> {first_link.split('?')[0]}")
    
    print(f"\n✅ Con selector específico: {unique_count} películas")

if __name__ == "__main__":
    analyze_duplicate_links()
