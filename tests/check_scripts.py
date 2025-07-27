#!/usr/bin/env python3
"""
Script para verificar si podemos obtener más películas con scroll/paginación
"""

import requests
from parsel import Selector
import time

def check_for_more_movies():
    # Intentar con diferentes User-Agents y headers
    headers_desktop = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    url = "https://www.imdb.com/chart/top/"
    
    print(f"🔍 Verificando con headers mejorados...")
    
    session = requests.Session()
    response = session.get(url, headers=headers_desktop)
    selector = Selector(text=response.text)
    
    print(f"📊 Status: {response.status_code}")
    
    # Buscar todos los posibles contenedores de películas
    all_movie_containers = [
        selector.css('li.ipc-metadata-list-summary-item'),
        selector.css('div[class*="titleColumn"]'),
        selector.css('div[data-testid*="title"]'),
        selector.css('div[class*="cli-title"]')
    ]
    
    print(f"\n🎬 Contenedores encontrados:")
    for i, containers in enumerate(all_movie_containers):
        print(f"  Opción {i+1}: {len(containers)} elementos")
    
    # Buscar scripts que puedan contener datos JSON
    scripts = selector.css('script[type="application/ld+json"]::text').getall()
    script_data = selector.css('script:contains("titleListType")::text').getall()
    
    print(f"\n📜 Scripts con datos:")
    print(f"  JSON-LD scripts: {len(scripts)}")
    print(f"  Scripts con titleListType: {len(script_data)}")
    
    # Buscar en el contenido de scripts por datos de películas
    for script in script_data[:1]:  # Solo el primero para no saturar
        if 'tt0' in script:  # IMDb IDs start with tt
            import re
            movie_ids = re.findall(r'tt\d{7,8}', script)
            print(f"  IDs de películas en script: {len(set(movie_ids))}")
            if len(set(movie_ids)) > 25:
                print(f"    Primeros 10: {list(set(movie_ids))[:10]}")
                print(f"    ✅ ¡Encontrado script con más de 25 películas!")
                return list(set(movie_ids))
    
    return None

if __name__ == "__main__":
    movie_ids = check_for_more_movies()
    if movie_ids:
        print(f"\n🎉 Solución encontrada: {len(movie_ids)} películas en total")
    else:
        print(f"\n🤔 La página parece limitada a 25 películas actualmente")
