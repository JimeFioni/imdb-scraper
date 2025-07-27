# 🎬 IMDb Top Movies Scraper

[![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Scrapy](https://img.shields.io/badge/scrapy-2.13%2B-green?style=for-the-badge&logo=scrapy&logoColor=white)](https://scrapy.org/)
[![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/JimeFioni/imdb-scraper?style=for-the-badge&logo=github)](https://github.com/JimeFioni/imdb-scraper/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/JimeFioni/imdb-scraper?style=for-the-badge&logo=github)](https://github.com/JimeFioni/imdb-scraper/network)
[![Issues](https://img.shields.io/github/issues/JimeFioni/imdb-scraper?style=for-the-badge&logo=github)](https://github.com/JimeFioni/imdb-scraper/issues)

[![Data Output](https://img.shields.io/badge/output-CSV-orange?style=for-the-badge&logo=microsoftexcel)](output/)
[![Movies](https://img.shields.io/badge/movies-50%20Top%20IMDb-red?style=for-the-badge&logo=imdb)](https://www.imdb.com/chart/top/)
[![Status](https://img.shields.io/badge/status-active-brightgreen?style=for-the-badge)](README.md)
[![Maintained](https://img.shields.io/badge/maintained-yes-green?style=for-the-badge)](README.md)

> **Un scraper completo y robusto para extraer información de las mejores películas de IMDb con una estructura organizada y fácil de mantener.**

## ✅ Funcionalidades

El scraper extrae la siguiente información de cada película:

- **Ranking**: Posición en el top de IMDb
- **Título**: Nombre de la película
- **Año**: Año de lanzamiento
- **Calificación**: Rating de IMDb (ej: 9.3)
- **Duración**: Duración en formato "2h 22m"
- **Metascore**: Puntuación de Metacritic (si está disponible)
- **Actores Principales**: Los 3 actores principales

## 🛠️ Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| ![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white) | 3.8+ | Lenguaje principal |
| ![Scrapy](https://img.shields.io/badge/Scrapy-2.13%2B-green?logo=scrapy&logoColor=white) | 2.13+ | Framework de web scraping |
| ![Requests](https://img.shields.io/badge/Requests-latest-yellow?logo=python&logoColor=white) | Latest | HTTP requests |
| ![CSV](https://img.shields.io/badge/CSV-Built--in-orange?logo=microsoftexcel&logoColor=white) | Built-in | Exportación de datos |

## 📊 Estadísticas del Proyecto

- 🎬 **50 películas** extraídas del Top de IMDb
- 📄 **7 campos de datos** por película
- 🔧 **27 archivos** en el proyecto
- 🧪 **10 scripts de testing** incluidos
- ⚡ **100% funcional** y testeado

## 📁 Estructura del Proyecto

```
imdb_scraper/
├── 📄 scrapy.cfg                    # Configuración de Scrapy
├── 📄 requirements.txt              # Dependencias Python
├── 📄 .gitignore                   # Archivos a ignorar en Git
├── 📄 README.md                    # Esta documentación
├── 📁 imdb_scraper/               # Código principal del scraper
│   ├── spiders/
│   │   └── top_movies.py          # Spider principal
│   ├── items.py                   # Definición de items
│   ├── pipelines.py              # Pipelines de procesamiento
│   └── settings.py               # Configuración del proyecto
├── 📁 scripts/                    # Scripts ejecutables
│   ├── run_scraper.sh            # Script principal para ejecutar
│   ├── run_scraper.py            # Versión Python del script
│   └── spider_extension.py       # Extensiones adicionales
├── 📁 output/                     # Archivos de salida
│   └── peliculas.csv             # Datos extraídos (generado)
├── 📁 tests/                      # Scripts de testing y debug
│   ├── README.md                 # Documentación de tests
│   ├── test_*.py                 # Scripts de testing
│   ├── analyze_*.py              # Scripts de análisis
│   └── *.html                    # Archivos de debug
└── 📁 venv/                       # Entorno virtual (creado localmente)
```

## 🚀 Instalación Rápida

[![Quick Start](https://img.shields.io/badge/Quick%20Start-3%20Steps-brightgreen?style=for-the-badge&logo=rocket)](README.md)

### 🔧 Opción 1: Instalación Automática
```bash
# Clonar repositorio
git clone https://github.com/JimeFioni/imdb-scraper.git
cd imdb-scraper

# Ejecutar (instala automáticamente dependencias)
./run.sh
```

### ⚡ Opción 2: Instalación Manual
```bash
# 1. Clonar repositorio
git clone https://github.com/JimeFioni/imdb-scraper.git
cd imdb-scraper

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar scraper
./scripts/run_scraper.sh
```

## 🎯 Uso

### [![Run](https://img.shields.io/badge/Ejecutar-Script-blue?style=flat-square&logo=play)](scripts/run_scraper.sh) Método Recomendado:
```bash
./run.sh
```

### [![Manual](https://img.shields.io/badge/Modo-Manual-orange?style=flat-square&logo=terminal)](README.md) Comando Directo:
```bash
source venv/bin/activate
scrapy crawl top_movies -L INFO
```

## 📄 Resultado

El scraper genera un archivo `output/peliculas.csv` con todas las películas extraídas en formato CSV.

### Ejemplo de datos extraídos:
```csv
Ranking,Título,Año,Calificación,Duración (min),Metascore,Actores Principales
1,The Shawshank Redemption,1994,9.3,2h 22m,82,"Tim Robbins, Morgan Freeman, Bob Gunton"
2,The Godfather,1972,9.2,2h 55m,100,"Marlon Brando, Al Pacino, James Caan"
3,The Dark Knight,2008,9.1,2h 32m,85,"Christian Bale, Heath Ledger, Aaron Eckhart"
```
## 🛠️ Instalación y Configuración

### 1. Clonar o descargar el proyecto
```bash
git clone <repository-url>
cd imdb_scraper
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar el scraper
```bash
./scripts/run_scraper.sh
```

## ⚙️ Configuración Técnica

### Configuraciones importantes del scraper:
- **Delay entre requests**: 2 segundos + aleatorio (0.5s)
- **Concurrent requests**: 1 (para evitar bloqueos)
- **AutoThrottle**: Habilitado para ajuste automático
- **Retry**: 3 intentos en caso de error
- **User-Agent**: Mozilla/5.0 (simula navegador real)

### Selectores CSS utilizados:
- **Título**: `h1[data-testid="hero__pageTitle"] span::text`
- **Calificación**: `span[class*="rating"]::text`
- **Duración**: `ul.ipc-inline-list li::text` (busca formato "Xh Ym")
- **Actores**: `a[data-testid="title-cast-item__actor"]::text`

## 🧪 Testing y Debug

El proyecto incluye varios scripts de testing en la carpeta `tests/`:
- Scripts para probar selectores CSS
- Herramientas de análisis de páginas
- Archivos de debug HTML
- Ver `tests/README.md` para más detalles

## 🔧 Solución de problemas

### Si no funciona:
1. Verificar que el entorno virtual esté activado
2. Instalar dependencias: `pip install -r requirements.txt`
3. Verificar la conexión a internet
4. Si IMDb cambia su estructura, usar los scripts en `tests/` para actualizar selectores

### Archivos de salida:
- `output/peliculas.csv` - Datos principales extraídos
- Logs de Scrapy en la consola para debugging

## 📝 Notas de Desarrollo

- El scraper utiliza una lista fija de 50 IDs de películas para garantizar consistencia
- Los selectores CSS están diseñados con múltiples fallbacks para mayor robustez
- El pipeline de exportación maneja automáticamente la codificación UTF-8
- La estructura está organizada para facilitar mantenimiento y testing

## 🤝 Contribuciones

[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen?style=for-the-badge&logo=github)](CONTRIBUTING.md)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge&logo=git)](README.md)

Para contribuir al proyecto:
1. 🍴 Fork el repositorio
2. 🌟 Crea una rama para tu feature: `git checkout -b feature/nueva-caracteristica`
3. 🧪 Usa los scripts de testing para validar cambios
4. 💾 Haz commit de tus cambios: `git commit -m 'Agregar nueva característica'`
5. 📤 Push a la rama: `git push origin feature/nueva-caracteristica`
6. 🔄 Crea un Pull Request

## � Estadísticas del Repositorio

[![GitHub repo size](https://img.shields.io/github/repo-size/JimeFioni/imdb-scraper?style=flat-square&logo=github)](README.md)
[![GitHub code size](https://img.shields.io/github/languages/code-size/JimeFioni/imdb-scraper?style=flat-square&logo=python)](README.md)
[![Lines of code](https://img.shields.io/tokei/lines/github/JimeFioni/imdb-scraper?style=flat-square&logo=codelines)](README.md)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/JimeFioni/imdb-scraper?style=flat-square&logo=git)](README.md)

## ⭐ Soporte

Si este proyecto te fue útil, ¡considera darle una estrella! ⭐

[![GitHub stars](https://img.shields.io/github/stars/JimeFioni/imdb-scraper?style=social)](https://github.com/JimeFioni/imdb-scraper/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/JimeFioni/imdb-scraper?style=social)](https://github.com/JimeFioni/imdb-scraper/network)

## 📄 Licencia

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge&logo=opensourceinitiative)](LICENSE)

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🚀 Próximas Características

- [ ] [![Feature](https://img.shields.io/badge/Feature-En%20desarrollo-blue?style=flat-square)](README.md) Soporte para más de 50 películas
- [ ] [![Feature](https://img.shields.io/badge/Feature-Planeado-green?style=flat-square)](README.md) Exportación a JSON y XML
- [ ] [![Feature](https://img.shields.io/badge/Feature-Planeado-green?style=flat-square)](README.md) Base de datos SQLite
- [ ] [![Feature](https://img.shields.io/badge/Feature-Planeado-green?style=flat-square)](README.md) GUI para configuración
- [ ] [![Feature](https://img.shields.io/badge/Feature-Planeado-green?style=flat-square)](README.md) Docker support

---

<p align="center">
  <strong>🎬 Hecho con ❤️ por <a href="https://github.com/JimeFioni">JimeFioni</a></strong>
</p>

<p align="center">
  <a href="#-imdb-top-movies-scraper">⬆️ Volver arriba</a>
</p>

### Para obtener más películas:
Cambiar el límite en `top_movies.py` línea 28:
```python
for i, row in enumerate(rows[:100]):  # Cambiar 50 por el número deseado
```

## 📊 Estadísticas del último scraping

- ✅ **25 películas extraídas** exitosamente
- ⏱️ **~50 segundos** de duración total
- 🎯 **100% de éxito** en extracción de datos
- 📈 **~30 películas/minuto** velocidad promedio

## 🎉 ¡Listo para usar!

El scraper está completamente funcional y listo para extraer datos de IMDb de manera ética y responsable.
