# 🧪 Tests y Scripts de Debug

Esta carpeta contiene todos los archivos utilizados para testing, debugging y análisis durante el desarrollo del scraper.

## 📁 Archivos incluidos:

### 🔍 Scripts de Testing de Selectores
- `test_selectors.py` - Prueba selectores CSS en páginas individuales
- `test_top_page.py` - Analiza la página principal del top 250
- `test_cli_title.py` - Prueba extracción de datos de títulos específicos
- `test_urls.py` - Valida URLs y accesibilidad

### 📊 Scripts de Análisis
- `analyze_links.py` - Analiza enlaces encontrados en las páginas
- `analyze_cli.py` - Análisis de línea de comandos
- `check_page.py` - Verificación general de páginas
- `check_scripts.py` - Verificación de scripts y funcionamiento

### 🔧 Herramientas de Generación
- `generate_top50.py` - Genera lista de IDs de las top 50 películas

### 🐛 Archivos de Debug
- `*.html` - Archivos HTML guardados para debugging offline

## 🚀 Cómo usar estos scripts:

La mayoría de estos scripts se pueden ejecutar directamente desde la carpeta tests:

```bash
cd tests
python test_selectors.py
python analyze_links.py
# etc...
```

**Nota:** Algunos scripts pueden requerir que el entorno virtual esté activado y las dependencias instaladas.

## ⚠️ Importante
Estos archivos son herramientas de desarrollo y debugging. No son necesarios para el funcionamiento normal del scraper.
