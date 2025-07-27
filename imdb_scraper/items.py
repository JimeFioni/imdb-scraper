# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


import scrapy


class ImdbScraperItem(scrapy.Item):
    titulo = scrapy.Field()
    anio = scrapy.Field()
    calificacion = scrapy.Field()
    duracion = scrapy.Field()
    metascore = scrapy.Field()
    actores = scrapy.Field()  # Lista con al menos 3 actores
    ranking = scrapy.Field()  # Posición en el top 250

