#!/usr/bin/env python3
"""
Script para ejecutar el scraper de IMDb Top 250
"""

import subprocess
import sys
import os

def run_scraper():
    """Ejecuta el scraper de películas de IMDb"""
    
    print("🎬 Iniciando scraper de IMDb Top 250...")
    print("=" * 50)
    
    try:
        # Cambiar al directorio del proyecto
        os.chdir('/Users/Jime/Desktop/imdb_scraper')
        
        # Ejecutar el spider
        result = subprocess.run([
            'scrapy', 'crawl', 'top_movies',
            '-L', 'INFO'  # Nivel de logging
        ], capture_output=True, text=True)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ Scraping completado exitosamente!")
            print("📄 Archivo generado: peliculas.csv")
            
            # Verificar si el archivo se creó
            if os.path.exists('peliculas.csv'):
                # Contar líneas
                with open('peliculas.csv', 'r', encoding='utf-8') as f:
                    lines = len(f.readlines())
                print(f"📊 Se extrajeron {lines - 1} películas (excluyendo header)")
            else:
                print("⚠️ No se encontró el archivo peliculas.csv")
        else:
            print(f"❌ Error en el scraping. Código de salida: {result.returncode}")
            
    except FileNotFoundError:
        print("❌ Error: Scrapy no está instalado o no está en el PATH")
        print("Instala Scrapy con: pip install scrapy")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    run_scraper()
