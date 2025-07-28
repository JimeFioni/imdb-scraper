# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import os
from itemadapter import ItemAdapter


class ImdbScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Limpiar datos
        if adapter.get('titulo'):
            adapter['titulo'] = adapter['titulo'].strip()
        
        if adapter.get('calificacion'):
            # Limpiar calificación para que sea un número
            adapter['calificacion'] = adapter['calificacion'].replace(',', '.')
        
        if adapter.get('actores') and isinstance(adapter['actores'], list):
            # Convertir lista de actores a string separado por comas
            adapter['actores'] = ', '.join(adapter['actores'])
        
        return item


class CsvExportPipeline:
    def open_spider(self, spider):
        # Obtener el directorio raíz del proyecto (un nivel arriba)
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        exports_dir = os.path.join(project_root, 'data', 'exports')
        
        # Asegurar que existe el directorio data/exports
        os.makedirs(exports_dir, exist_ok=True)
        
        # Crear archivo CSV en la carpeta data/exports
        csv_path = os.path.join(exports_dir, 'peliculas.csv')
        self.file = open(csv_path, 'w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)
        
        # Escribir headers
        self.writer.writerow([
            'Ranking', 'Título', 'Año', 'Calificación', 
            'Duración (min)', 'Metascore', 'Actores Principales'
        ])
    
    def close_spider(self, spider):
        self.file.close()
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Escribir fila al CSV
        self.writer.writerow([
            adapter.get('ranking', ''),
            adapter.get('titulo', ''),
            adapter.get('anio', ''),
            adapter.get('calificacion', ''),
            adapter.get('duracion', ''),
            adapter.get('metascore', ''),
            adapter.get('actores', '')
        ])
        
        return item
