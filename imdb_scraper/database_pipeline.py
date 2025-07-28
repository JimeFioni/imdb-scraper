import sqlite3
import os
from itemadapter import ItemAdapter


class DatabasePipeline:
    """Pipeline para guardar datos en base de datos SQLite"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def open_spider(self, spider):
        # Obtener el directorio raíz del proyecto (un nivel arriba)
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        exports_dir = os.path.join(project_root, 'data', 'exports')
        
        # Asegurar que existe el directorio data/exports
        os.makedirs(exports_dir, exist_ok=True)
        
        # Conectar a la base de datos
        db_path = os.path.join(exports_dir, 'peliculas.db')
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        
        # Crear tabla si no existe
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS peliculas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ranking INTEGER,
                titulo TEXT NOT NULL,
                anio TEXT,
                calificacion REAL,
                duracion TEXT,
                metascore INTEGER,
                actores TEXT,
                fecha_scraping TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Limpiar datos anteriores del mismo scraping
        self.cursor.execute('DELETE FROM peliculas WHERE DATE(fecha_scraping) = DATE("now")')
        self.connection.commit()
        
        spider.logger.info("🗄️ Base de datos SQLite inicializada")
    
    def close_spider(self, spider):
        if self.connection:
            self.connection.close()
            spider.logger.info("🗄️ Conexión a base de datos cerrada")
    
    def process_item(self, item, spider):
        try:
            adapter = ItemAdapter(item)
            
            # Preparar datos
            metascore = None
            if adapter.get('metascore') and adapter.get('metascore').isdigit():
                metascore = int(adapter.get('metascore'))
            
            calificacion = None
            if adapter.get('calificacion'):
                try:
                    calificacion = float(adapter.get('calificacion').replace(',', '.'))
                except (ValueError, AttributeError):
                    pass
            
            # Insertar en base de datos
            self.cursor.execute('''
                INSERT INTO peliculas (ranking, titulo, anio, calificacion, duracion, metascore, actores)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                adapter.get('ranking'),
                adapter.get('titulo'),
                adapter.get('anio'),
                calificacion,
                adapter.get('duracion'),
                metascore,
                adapter.get('actores')
            ))
            
            self.connection.commit()
            spider.logger.info(f"💾 Guardado en BD: {adapter.get('titulo')}")
            
        except Exception as e:
            spider.logger.error(f"❌ Error guardando en BD: {e}")
        
        return item
