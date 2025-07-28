#!/usr/bin/env python3
"""
Script para generar las URLs de las películas faltantes del top 50
"""

# Top 50 movies según IMDb (IDs conocidos)
TOP_50_MOVIE_IDS = [
    'tt0111161',  # 1. The Shawshank Redemption
    'tt0068646',  # 2. The Godfather
    'tt0468569',  # 3. The Dark Knight
    'tt0071562',  # 4. The Godfather Part II
    'tt0050083',  # 5. 12 Angry Men
    'tt0167260',  # 6. The Lord of the Rings: The Return of the King
    'tt0108052',  # 7. Schindler's List
    'tt0110912',  # 8. Pulp Fiction
    'tt0120737',  # 9. The Lord of the Rings: The Fellowship of the Ring
    'tt0060196',  # 10. The Good, the Bad and the Ugly
    'tt0109830',  # 11. Forrest Gump
    'tt0167261',  # 12. The Lord of the Rings: The Two Towers
    'tt0137523',  # 13. Fight Club
    'tt1375666',  # 14. Inception
    'tt0080684',  # 15. Star Wars: Episode V - The Empire Strikes Back
    'tt0133093',  # 16. The Matrix
    'tt0099685',  # 17. Goodfellas
    'tt0816692',  # 18. Interstellar
    'tt0073486',  # 19. One Flew Over the Cuckoo's Nest
    'tt0114369',  # 20. Se7en
    'tt0038650',  # 21. It's a Wonderful Life
    'tt0102926',  # 22. The Silence of the Lambs
    'tt0047478',  # 23. Seven Samurai
    'tt0120815',  # 24. Saving Private Ryan
    'tt0120689',  # 25. The Green Mile
    'tt0317248',  # 26. City of God
    'tt0034583',  # 27. Casablanca
    'tt0095327',  # 28. Grave of the Fireflies
    'tt0120586',  # 29. American Beauty
    'tt0054215',  # 30. Psycho
    'tt0078788',  # 31. Apocalypse Now
    'tt0095765',  # 32. Cinema Paradiso
    'tt0253474',  # 33. The Pianist
    'tt0405094',  # 34. The Lives of Others
    'tt0027977',  # 35. Modern Times
    'tt0064116',  # 36. Once Upon a Time in the West
    'tt0078748',  # 37. Alien
    'tt0021749',  # 38. City Lights
    'tt0025316',  # 39. It Happened One Night
    'tt0103064',  # 40. Terminator 2: Judgment Day
    'tt0056058',  # 41. Dr. Strangelove
    'tt0086190',  # 42. Scarface
    'tt0031679',  # 43. Gone with the Wind
    'tt0082971',  # 44. Raiders of the Lost Ark
    'tt0070735',  # 45. The Sting
    'tt0057012',  # 46. 8½
    'tt0088763',  # 47. Back to the Future
    'tt0172495',  # 48. Gladiator
    'tt0110413',  # 49. Léon: The Professional
    'tt0062622',  # 50. 2001: A Space Odyssey
]

def create_extended_spider():
    """Crear configuración para spider extendido"""
    
    print("🎬 Configuración para obtener 50 películas del Top IMDb")
    print("=" * 60)
    
    print(f"📊 Total de películas configuradas: {len(TOP_50_MOVIE_IDS)}")
    
    # Crear el método que se puede agregar al spider
    spider_extension = f'''
def get_top_50_urls(self):
    """Método para obtener URLs de las top 50 películas"""
    base_url = "https://www.imdb.com/title/"
    movie_ids = {TOP_50_MOVIE_IDS}
    
    urls = []
    for i, movie_id in enumerate(movie_ids, 1):
        url = f"{{base_url}}{{movie_id}}/"
        urls.append((url, i))
    
    return urls

def parse_extended(self, response):
    """Método alternativo que procesa las 50 películas directamente"""
    self.logger.info("🚀 Usando método extendido para 50 películas")
    
    movie_urls = self.get_top_50_urls()
    
    for url, rank in movie_urls:
        self.logger.info(f"🎬 Procesando película {{rank}}: {{url}}")
        yield scrapy.Request(
            url, 
            callback=self.parse_detail,
            meta={{'rank': rank}}
        )
'''
    
    print("\n📝 Código generado para el spider:")
    print("   - Método get_top_50_urls()")
    print("   - Método parse_extended()")
    print("   - Lista de 50 IDs de películas")
    
    return spider_extension

if __name__ == "__main__":
    extension = create_extended_spider()
    
    print(f"\n💡 Para usar este método:")
    print(f"   1. Agregar los métodos al spider")
    print(f"   2. Cambiar start_urls para usar parse_extended")
    print(f"   3. O mantener el método actual para las 25 disponibles")
    
    # Guardar la extensión en un archivo
    with open('spider_extension.py', 'w', encoding='utf-8') as f:
        f.write(extension)
    
    print(f"\n✅ Extensión guardada en: spider_extension.py")
