# 🎬 IMDb Scraper

[![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Scrapy](https://img.shields.io/badge/scrapy-2.13%2B-green?style=flat-square&logo=scrapy)](https://scrapy.org/)
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)

> **Web scraper profesional para extraer datos del IMDb Top 250. Incluye análisis comparativo de herramientas de scraping y sistema robusto de proxies.**

## ✨ Características Principales

- 🚀 **Scrapy optimizado** para scraping eficiente de IMDb
- 🛡️ **Sistema de proxies** con rotación automática de IPs
- 📊 **Análisis comparativo** Scrapy vs Selenium vs Playwright  
- 💾 **Múltiples formatos** CSV, SQLite, PostgreSQL
- 🔍 **Anti-detección** headers dinámicos y rate limiting

## 🚀 Instalación Rápida

```bash
git clone https://github.com/JimeFioni/imdb-scraper.git
cd imdb-scraper
./setup.sh
```

## 💻 Uso Básico

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar scraper (Top 250 completo)
scrapy crawl top_movies

# Ejecutar muestra rápida (5 películas)  
scrapy crawl top_movies -s CLOSESPIDER_ITEMCOUNT=5
```

## 📊 Datos Extraídos

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **Ranking** | Posición en Top 250 | 1, 2, 3... |
| **Título** | Nombre de la película | "The Shawshank Redemption" |
| **Año** | Año de lanzamiento | 1994 |
| **Calificación** | Rating IMDb | 9.3 |
| **Duración** | Tiempo de película | "2h 22m" |
| **Metascore** | Puntuación Metacritic | 82 |
| **Actores** | Actores principales | "Tim Robbins, Morgan Freeman..." |

## 🏗️ Estructura del Proyecto

```
imdb_scraper/
├── imdb_scraper/              # Core del scraper Scrapy
│   ├── spiders/top_movies.py  # Spider principal
│   ├── proxy_manager.py       # Sistema de proxies
│   └── settings.py            # Configuración
├── examples/                  # Implementaciones comparativas
├── config/                    # Configuraciones y proxies
├── docs/                      # Documentación técnica
└── data/exports/              # Archivos CSV generados
```

## 🛠️ Tecnologías

- **Python 3.8+** - Lenguaje principal
- **Scrapy** - Framework de scraping principal  
- **Selenium/Playwright** - Implementaciones comparativas
- **PostgreSQL/SQLite** - Almacenamiento de datos
- **Docker** - Containerización y despliegue

## 📖 Documentación

- [**Comparación Técnica Completa**](docs/IMDB_TECHNICAL_COMPARISON.md) - Análisis detallado de herramientas
- [**Guía de Colaboradores**](COLABORADORES_BIENVENIDA.md) - Información para contribuir
- [**Verificación del Proyecto**](VERIFICACION_FINAL_COMPLETADA.md) - Estado del proyecto

## 🤝 Para Colaboradores

¿Quieres contribuir? ¡Excelente! 

1. Revisa [COLABORADORES_BIENVENIDA.md](COLABORADORES_BIENVENIDA.md) 
2. Lee [CONTRIBUTING.md](CONTRIBUTING.md)
3. Crea un issue de presentación usando el template
4. ¡Comienza a colaborar!

## 🎯 Resultados de Ejemplo

```csv
ranking,titulo,anio,calificacion,duracion,metascore,actores
1,"The Shawshank Redemption",1994,9.3,"2h 22m",82,"Tim Robbins, Morgan Freeman, Bob Gunton"
2,"The Godfather",1972,9.2,"2h 55m",100,"Marlon Brando, Al Pacino, James Caan"
3,"The Dark Knight",2008,9.0,"2h 32m",84,"Christian Bale, Heath Ledger, Aaron Eckhart"
```

## 🚀 Uso Responsable

- ✅ **Análisis de datos público** de IMDb
- ✅ **Respeto de robots.txt** y rate limiting  
- ✅ **Cumplimiento de términos** de servicio

**⚠️ Importante**: Úsalo de manera responsable y respeta los términos de servicio de IMDb.

## 👨‍💻 Autor

**Desarrollado por Jime Fioni**

- 📧 Email: jimenafioni@gmail.com
- 🌐 GitHub: [@JimeFioni](https://github.com/JimeFioni)
- 💼 LinkedIn: [Jimena Fioni](https://linkedin.com/in/jimena-fioni/)

---

## ⭐ ¿Te Gustó el Proyecto?

Si este proyecto te resultó útil:

- ⭐ **Dale una estrella** en GitHub  
- 🐛 **Reporta bugs** si encuentras alguno
- 💡 **Sugiere mejoras** en los issues
- 🤝 **Contribuye** con código o documentación

**🎬 ¡Disfruta explorando los datos de las mejores películas de IMDb!**
