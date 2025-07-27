#!/usr/bin/env python3
"""
Script para probar selectores CSS en una página de IMDb
"""

import requests
from parsel import Selector

def test_selectors():
    # URL de prueba - The Shawshank Redemption
    url = "https://www.imdb.com/title/tt0111161/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    print(f"🔍 Probando selectores en: {url}")
    
    response = requests.get(url, headers=headers)
    selector = Selector(text=response.text)
    
    print("\n📊 CALIFICACIONES:")
    rating_selectors = [
        'span[data-testid="hero-rating-bar__aggregate-rating__score"]::text',
        'span.sc-7ab21ed2-1::text',
        'span[class*="rating"]::text',
        'div[data-testid="hero-rating-bar__aggregate-rating"] span::text',
        'span.ipc-rating-star--rating::text',
        '[data-testid="hero-rating-bar__aggregate-rating__score"] span::text'
    ]
    
    for selector_str in rating_selectors:
        result = selector.css(selector_str).get()
        print(f"  {selector_str:<60} -> {result}")
    
    print("\n⏱️ DURACIÓN:")
    duration_selectors = [
        'li[data-testid="title-techspec_runtime"] span::text',
        'ul[data-testid="hero-title-block__metadata"] li::text',
        'span.ipc-metadata-list-item__list-content-item::text',
        'ul.ipc-inline-list li::text',
        'li.ipc-metadata-list-item::text'
    ]
    
    for selector_str in duration_selectors:
        results = selector.css(selector_str).getall()
        duration_found = None
        for result in results:
            if 'min' in result or any(char.isdigit() for char in result):
                duration_found = result
                break
        print(f"  {selector_str:<60} -> {duration_found}")
    
    print("\n🎭 ACTORES:")
    actor_selectors = [
        'a[data-testid="title-cast-item__actor"]::text',
        'li[data-testid="title-cast-item"] a::text',
        'a[href*="/name/nm"]::text'
    ]
    
    for selector_str in actor_selectors:
        results = selector.css(selector_str).getall()[:3]
        print(f"  {selector_str:<60} -> {results}")

if __name__ == "__main__":
    test_selectors()
