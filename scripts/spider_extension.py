
def get_top_50_urls(self):
    """Método para obtener URLs de las top 50 películas"""
    base_url = "https://www.imdb.com/title/"
    movie_ids = ['tt0111161', 'tt0068646', 'tt0468569', 'tt0071562', 'tt0050083', 'tt0167260', 'tt0108052', 'tt0110912', 'tt0120737', 'tt0060196', 'tt0109830', 'tt0167261', 'tt0137523', 'tt1375666', 'tt0080684', 'tt0133093', 'tt0099685', 'tt0816692', 'tt0073486', 'tt0114369', 'tt0038650', 'tt0102926', 'tt0047478', 'tt0120815', 'tt0120689', 'tt0317248', 'tt0034583', 'tt0095327', 'tt0120586', 'tt0054215', 'tt0078788', 'tt0095765', 'tt0253474', 'tt0405094', 'tt0027977', 'tt0064116', 'tt0078748', 'tt0021749', 'tt0025316', 'tt0103064', 'tt0056058', 'tt0086190', 'tt0031679', 'tt0082971', 'tt0070735', 'tt0057012', 'tt0088763', 'tt0172495', 'tt0110413', 'tt0062622']
    
    urls = []
    for i, movie_id in enumerate(movie_ids, 1):
        url = f"{base_url}{movie_id}/"
        urls.append((url, i))
    
    return urls

def parse_extended(self, response):
    """Método alternativo que procesa las 50 películas directamente"""
    self.logger.info("🚀 Usando método extendido para 50 películas")
    
    movie_urls = self.get_top_50_urls()
    
    for url, rank in movie_urls:
        self.logger.info(f"🎬 Procesando película {rank}: {url}")
        yield scrapy.Request(
            url, 
            callback=self.parse_detail,
            meta={'rank': rank}
        )
