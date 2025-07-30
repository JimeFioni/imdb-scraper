import psycopg2
import psycopg2.extras
import re
import os
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class PostgreSQLPipeline:
    """Pipeline avanzado para PostgreSQL con modelo relacional completo"""
    
    def __init__(self, postgres_host, postgres_port, postgres_db, postgres_user, postgres_password):
        self.postgres_host = postgres_host
        self.postgres_port = postgres_port
        self.postgres_db = postgres_db
        self.postgres_user = postgres_user
        self.postgres_password = postgres_password
        self.connection = None
        self.cursor = None
        self.items_processed = 0
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            postgres_host=crawler.settings.get("POSTGRES_HOST", "localhost"),
            postgres_port=crawler.settings.get("POSTGRES_PORT", 5432),
            postgres_db=crawler.settings.get("POSTGRES_DB", "imdb_scraper_db"),
            postgres_user=crawler.settings.get("POSTGRES_USER", "imdb_user"),
            postgres_password=crawler.settings.get("POSTGRES_PASSWORD", "imdb_secure_2024"),
        )
    
    def open_spider(self, spider):
        """Conectar a PostgreSQL y preparar tablas"""
        try:
            # Intentar conexión
            self.connection = psycopg2.connect(
                host=self.postgres_host,
                port=self.postgres_port,
                database=self.postgres_db,
                user=self.postgres_user,
                password=self.postgres_password,
                cursor_factory=psycopg2.extras.RealDictCursor
            )
            self.cursor = self.connection.cursor()
            
            # Verificar que las tablas existen
            self._verify_database_schema(spider)
            
            # Limpiar datos del scraping actual
            self._clean_current_session_data(spider)
            
            spider.logger.info("🐘 PostgreSQL conectado exitosamente")
            
        except Exception as e:
            spider.logger.warning(f"⚠️ PostgreSQL no disponible: {e}")
            spider.logger.info("📝 Continuando solo con SQLite...")
            self.connection = None
            self.cursor = None
            
            spider.logger.info(f"🐘 PostgreSQL conectado: {self.postgres_host}:{self.postgres_port}/{self.postgres_db}")
            
        except psycopg2.OperationalError as e:
            spider.logger.warning(f"⚠️  PostgreSQL no disponible: {e}")
            spider.logger.warning("� Para usar PostgreSQL, ejecuta: cd database && docker-compose up -d")
            self.connection = None
            self.cursor = None
        except Exception as e:
            spider.logger.error(f"❌ Error conectando a PostgreSQL: {e}")
            self.connection = None
            self.cursor = None
    
    def close_spider(self, spider):
        """Cerrar conexión y ejecutar análisis final"""
        if self.connection:
            try:
                # Refrescar vistas materializadas
                self._refresh_materialized_views(spider)
                
                # Ejecutar análisis estadístico final
                self._execute_final_analysis(spider)
                
                self.connection.close()
                spider.logger.info(f"🐘 PostgreSQL: {self.items_processed} elementos procesados - Conexión cerrada")
            except Exception as e:
                spider.logger.error(f"❌ Error cerrando PostgreSQL: {e}")
    
    def process_item(self, item, spider):
        """Procesar item y guardar en PostgreSQL"""
        if not self.connection:
            # Si no hay conexión PostgreSQL, continuar sin error
            return item
            
        try:
            adapter = ItemAdapter(item)
            
            # Validar item
            if not adapter.get('titulo'):
                raise DropItem(f"Item sin título: {item}")
            
            # Insertar película
            pelicula_id = self._insert_pelicula(adapter, spider)
            
            # Insertar actores
            self._insert_actores(pelicula_id, adapter, spider)
            
            self.connection.commit()
            self.items_processed += 1
            spider.logger.info(f"💾 PostgreSQL: {adapter.get('titulo')} → ID {pelicula_id}")
            
        except Exception as e:
            self.connection.rollback()
            spider.logger.error(f"❌ Error PostgreSQL: {e}")
            # No hacer DropItem para permitir que otros pipelines funcionen
        
        return item
    
    def _verify_database_schema(self, spider):
        """Verificar que el esquema de la base de datos está correcto"""
        try:
            # Verificar tabla peliculas
            self.cursor.execute("""
                SELECT column_name FROM information_schema.columns 
                WHERE table_name = 'peliculas' AND table_schema = 'public'
            """)
            columns = [row[0] for row in self.cursor.fetchall()]
            
            required_columns = ['id', 'titulo', 'anio', 'calificacion', 'duracion_minutos', 'metascore', 'ranking']
            missing_columns = [col for col in required_columns if col not in columns]
            
            if missing_columns:
                spider.logger.warning(f"⚠️  Columnas faltantes en PostgreSQL: {missing_columns}")
                spider.logger.warning("💡 Ejecuta: cd database && docker-compose down && docker-compose up -d")
            else:
                spider.logger.info("✅ Esquema PostgreSQL verificado correctamente")
                
        except Exception as e:
            spider.logger.warning(f"⚠️  No se pudo verificar esquema: {e}")
    
    def _clean_current_session_data(self, spider):
        """Limpiar datos del scraping actual"""
        try:
            # Limpiar datos del día actual
            self.cursor.execute("""
                DELETE FROM actores 
                WHERE pelicula_id IN (
                    SELECT id FROM peliculas 
                    WHERE DATE(fecha_scraping) = CURRENT_DATE
                )
            """)
            deleted_actores = self.cursor.rowcount
            
            self.cursor.execute("DELETE FROM peliculas WHERE DATE(fecha_scraping) = CURRENT_DATE")
            deleted_peliculas = self.cursor.rowcount
            
            self.connection.commit()
            
            if deleted_peliculas > 0 or deleted_actores > 0:
                spider.logger.info(f"🗑️  Limpieza PostgreSQL: {deleted_peliculas} películas, {deleted_actores} actores")
                
        except Exception as e:
            spider.logger.warning(f"⚠️  Error limpiando datos: {e}")
    
    def _refresh_materialized_views(self, spider):
        """Refrescar vistas materializadas"""
        try:
            self.cursor.execute("SELECT refresh_materialized_views()")
            result = self.cursor.fetchone()[0]
            spider.logger.info(f"🔄 {result}")
        except Exception as e:
            spider.logger.warning(f"⚠️  Error refrescando vistas: {e}")
    
    def _insert_pelicula(self, adapter, spider):
        """Insertar película y retornar ID"""
        try:
            # Convertir duración a minutos
            duracion_minutos = self._parse_duration_to_minutes(adapter.get('duracion'))
            
            # Preparar datos
            titulo = adapter.get('titulo', '').strip()
            anio = self._safe_int(adapter.get('anio'))
            calificacion = self._safe_float(adapter.get('calificacion'))
            duracion_texto = adapter.get('duracion', '').strip()
            metascore = self._safe_int(adapter.get('metascore'))
            ranking = self._safe_int(adapter.get('ranking', 0))
            
            # SQL con UPSERT para evitar duplicados
            sql = """
            INSERT INTO peliculas (titulo, anio, calificacion, duracion_minutos, duracion_texto, metascore, ranking)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (titulo, anio) 
            DO UPDATE SET 
                calificacion = EXCLUDED.calificacion,
                duracion_minutos = EXCLUDED.duracion_minutos,
                duracion_texto = EXCLUDED.duracion_texto,
                metascore = EXCLUDED.metascore,
                ranking = EXCLUDED.ranking,
                fecha_actualizacion = CURRENT_TIMESTAMP
            RETURNING id;
            """
            
            self.cursor.execute(sql, (titulo, anio, calificacion, duracion_minutos, duracion_texto, metascore, ranking))
            pelicula_id = self.cursor.fetchone()[0]
            
            return pelicula_id
            
        except Exception as e:
            spider.logger.error(f"Error insertando película: {e}")
            raise
    
    def _insert_actores(self, pelicula_id, adapter, spider):
        """Insertar actores de la película"""
        try:
            actores = adapter.get('actores', [])
            
            if isinstance(actores, str):
                # Si es string, separar por comas
                actores = [actor.strip() for actor in actores.split(',') if actor.strip()]
            
            # Limpiar actores existentes de esta película
            self.cursor.execute("DELETE FROM actores WHERE pelicula_id = %s", (pelicula_id,))
            
            # Insertar nuevos actores (máximo 3)
            for posicion, nombre in enumerate(actores[:3], 1):
                if nombre and nombre.strip():
                    sql = """
                    INSERT INTO actores (pelicula_id, nombre, posicion)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (pelicula_id, posicion) DO NOTHING;
                    """
                    self.cursor.execute(sql, (pelicula_id, nombre.strip(), posicion))
            
        except Exception as e:
            spider.logger.error(f"Error insertando actores: {e}")
            raise
    
    def _parse_duration_to_minutes(self, duration_text):
        """Convertir texto de duración a minutos"""
        if not duration_text:
            return None
        
        try:
            # Buscar patrones como "2h 22m", "142 min", etc.
            hours_match = re.search(r'(\d+)h', duration_text)
            minutes_match = re.search(r'(\d+)m', duration_text)
            total_minutes_match = re.search(r'(\d+)\s*min', duration_text)
            
            if hours_match or minutes_match:
                hours = int(hours_match.group(1)) if hours_match else 0
                minutes = int(minutes_match.group(1)) if minutes_match else 0
                return hours * 60 + minutes
            elif total_minutes_match:
                return int(total_minutes_match.group(1))
            
            return None
            
        except Exception:
            return None
    
    def _safe_int(self, value):
        """Convertir a entero de forma segura"""
        try:
            if value is None or value == '':
                return None
            return int(float(str(value)))
        except (ValueError, TypeError):
            return None
    
    def _safe_float(self, value):
        """Convertir a float de forma segura"""
        try:
            if value is None or value == '':
                return None
            return float(str(value).replace(',', '.'))
        except (ValueError, TypeError):
            return None
    
    def _execute_final_analysis(self, spider):
        """Ejecutar análisis estadístico final"""
        try:
            # Contar registros insertados
            self.cursor.execute("SELECT COUNT(*) FROM peliculas WHERE DATE(fecha_scraping) = CURRENT_DATE")
            peliculas_count = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM actores WHERE DATE(fecha_creacion) = CURRENT_DATE")
            actores_count = self.cursor.fetchone()[0]
            
            # Ejecutar análisis de correlación
            self.cursor.execute("SELECT * FROM analyze_rating_correlation()")
            correlacion = self.cursor.fetchone()
            
            spider.logger.info(f"""
📊 ANÁLISIS POSTGRESQL COMPLETO:
   • Películas procesadas: {peliculas_count}
   • Actores registrados: {actores_count}
   • Correlación IMDb/Metascore: {correlacion[2] if correlacion else 'N/A'}
   • Diferencia promedio: {correlacion[4] if correlacion else 'N/A'}
            """)
            
        except Exception as e:
            spider.logger.warning(f"⚠️  Error en análisis final: {e}")
