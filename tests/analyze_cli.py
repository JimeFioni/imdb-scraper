#!/usr/bin/env python3
"""
Script para analizar los 50 elementos cli-title
"""

import requests
from parsel import Selector

def analyze_cli_title():
    url = "https://www.imdb.com/chart/top/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    response = requests.get(url, headers=headers)
    selector = Selector(text=response.text)
    
    # Obtener los 50 elementos cli-title
    cli_elements = selector.css('div[class*="cli-title"]')
    print(f"🔍 Analizando {len(cli_elements)} elementos cli-title")
    
    movies = []
    for i, element in enumerate(cli_elements):
        # Buscar enlace
        link = element.css('a[href*="/title/"]::attr(href)').get()
        
        # Buscar título
        title = (
            element.css('h3::text').get() or
            element.css('a::text').get() or
            element.css('::text').get()
        )
        
        if link and title:
            movie_id = link.split('/title/')[-1].split('/')[0] if '/title/' in link else None
            movies.append({
                'index': i + 1,
                'title': title.strip(),
                'link': link,
                'movie_id': movie_id
            })
    
    print(f"\n✅ Películas válidas encontradas: {len(movies)}")
    
    # Mostrar las primeras 10 y últimas 5
    print(f"\n📝 Primeras 10 películas:")
    for movie in movies[:10]:
        print(f"  {movie['index']:2d}. {movie['title']:<40} ({movie['movie_id']})")
    
    if len(movies) > 15:
        print(f"\n📝 Últimas 5 películas:")
        for movie in movies[-5:]:
            print(f"  {movie['index']:2d}. {movie['title']:<40} ({movie['movie_id']})")
    
    # Verificar si hay duplicados
    unique_ids = set()
    duplicates = []
    for movie in movies:
        if movie['movie_id'] in unique_ids:
            duplicates.append(movie['movie_id'])
        else:
            unique_ids.add(movie['movie_id'])
    
    print(f"\n🔍 Análisis de duplicados:")
    print(f"  Total de películas: {len(movies)}")
    print(f"  IDs únicos: {len(unique_ids)}")
    print(f"  Duplicados: {len(duplicates)}")
    
    return list(unique_ids)

if __name__ == "__main__":
    movie_ids = analyze_cli_title()
    print(f"\n🎯 IDs únicos para scraping: {len(movie_ids)}")
