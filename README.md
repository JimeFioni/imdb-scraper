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

# Crear entorno virtual e instalar dependencias
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Verificar instalación
./verify_system.sh
```

## 💻 Uso Básico

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar scraper completo (Top 250)
scrapy crawl top_movies

# Ejecutar muestra rápida (10 películas)  
scrapy crawl top_movies -s CLOSESPIDER_ITEMCOUNT=10

# Verificar sistema antes de ejecutar
./verify_system.sh
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
├── 🕷️ Core Scrapy
│   ├── spiders/top_movies.py      ✅ Spider principal - Extrae datos de IMDb Top 250
│   ├── items.py                   ✅ Definición items - Estructura de datos extraídos
│   ├── pipelines.py               ✅ Pipelines básicos - Procesamiento y validación
│   ├── database_pipeline.py       ✅ Pipeline SQLite - Persistencia en base local
│   ├── postgresql_pipeline.py     ✅ Pipeline PostgreSQL - Persistencia avanzada
│   ├── middlewares.py             ✅ Middlewares complementarios - User-agents, delays, resiliencia
│   ├── proxy_middleware.py        ✅ Middleware proxies - Rotación automática de IPs
│   ├── proxy_manager.py           ✅ Gestor de proxies - Lógica de rotación y validación
│   ├── selector_factory.py        ✅ Patrón Factory - Extracción modular de datos
│   └── settings.py                ✅ Configuración - Settings globales de Scrapy
│
├── ⚙️ Configuración
│   ├── config/proxies.json        ✅ Config proxies - Lista de proxies, TOR y VPN
│   └── config/database/schema.sql ✅ Schema SQL - Modelo relacional PostgreSQL
│
├── 📊 Datos y Exports
│   └── data/exports/*.csv         ✅ Múltiples CSVs - Películas extraídas en diferentes formatos
│
├── 🛠️ Scripts de Setup
│   ├── verify_system.sh           ✅ Verificación sistema - Valida dependencias y configuración
│   ├── setup_proxy_system.sh      ✅ Setup proxies/TOR - Instalación automática de TOR
│   ├── setup_postgres_local.sh    ✅ Setup PostgreSQL - Configuración base de datos local
│   └── setup_docker.sh            ✅ Setup Docker - Containerización con PostgreSQL
│
├── 📚 Documentación
│   ├── README.md                  ✅ Guía principal - Este archivo
│   ├── docs/sql/advanced_queries.sql ✅ Consultas SQL - Análisis avanzado de datos
│   ├── docs/PROXY_ARCHITECTURE.md ✅ Arquitectura proxies - Documentación técnica del sistema
│   ├── CONTRIBUTING.md            ✅ Guía colaboradores - Instrucciones para contribuir
│   └── CHANGELOG.md               ✅ Registro cambios - Historial de versiones
│
└── 🔧 Configuración del Proyecto
    ├── requirements.txt            ✅ Dependencias - Paquetes Python requeridos
    ├── scrapy.cfg                  ✅ Config Scrapy - Configuración del framework
    └── .gitignore                  ✅ Archivos ignorados - Control de versiones
```

## 🛠️ Tecnologías

- **Python 3.8+** - Lenguaje principal
- **Scrapy** - Framework de scraping principal  
- **Selenium/Playwright** - Implementaciones comparativas
- **PostgreSQL/SQLite** - Almacenamiento de datos
- **Docker** - Containerización y despliegue

## 🔧 Scripts Disponibles

```bash
# Verificar configuración del sistema
./verify_system.sh

# Configurar PostgreSQL local (opcional)
./setup_postgres_local.sh

# Configurar Docker con PostgreSQL (opcional)
./setup_docker.sh

# Configurar sistema de proxies
./setup_proxy_system.sh
```

> **📝 Nota**: Por defecto, el scraper usa SQLite + PostgreSQL si está disponible. PostgreSQL está configurado y habilitado, pero si no está disponible, continuará solo con SQLite sin errores.

## 📖 Documentación

- [**Comparación Técnica Completa**](docs/IMDB_TECHNICAL_COMPARISON.md) - Análisis detallado de herramientas
- [**Guía de Colaboradores**](CONTRIBUTING.md) - Información para contribuir

## 🤝 Para Colaboradores

¿Quieres contribuir? ¡Excelente! 

1. Lee [CONTRIBUTING.md](CONTRIBUTING.md) para instrucciones detalladas
2. Crea un issue usando el template de colaborador
3. ¡Comienza a colaborar!

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
