# 🎬 IMDb Top Movies Scraper Profesional

[![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Scrapy](https://img.shields.io/badge/scrapy-2.13%2B-green?style=for-the-badge&logo=scrapy&logoColor=white)](https://scrapy.org/)
[![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)](LICENSE)
[![Proxy Support](https://img.shields.io/badge/proxy-rotation-orange?style=for-the-badge&logo=security)](config/proxies.json)
[![Anti-Bot](https://img.shields.io/badge/anti--bot-evasion-red?style=for-the-badge&logo=shield)](imdb_scraper/proxy_middleware.py)
[![Benchmark](https://img.shields.io/badge/benchmark-included-purple?style=for-the-badge&logo=speedtest)](benchmark/)

[![Data Output](https://img.shields.io/badge/output-CSV%20%26%20SQLite%20%26%20PostgreSQL-orange?style=for-the-badge&logo=database)](data/exports/)
[![Docker](https://img.shields.io/badge/docker-VPN%20ready-blue?style=for-the-badge&logo=docker&logoColor=white)](config/docker/)
[![Movies](https://img.shields.io/badge/movies-Top%20250%20IMDb-red?style=for-the-badge&logo=imdb)](https://www.imdb.com/chart/top/)
[![Technical](https://img.shields.io/badge/comparison-Scrapy%20vs%20Selenium%20vs%20Playwright-green?style=for-the-badge&logo=comparison)](docs/IMDB_TECHNICAL_COMPARISON.md)

> **Sistema profesional de web scraping para IMDb Top 250 con arquitectura robusta, sistema avanzado de proxies, análisis técnico comparativo y múltiples formatos de salida. Incluye comparación detallada con Selenium y Playwright.**

## 🌟 Características Principales

### 🚀 **Core Features**
- **Web Scraping Profesional**: Extracción optimizada de IMDb Top 250
- **Sistema de Proxies Avanzado**: Rotación automática, fallback y validación
- **Anti-Bot Evasion**: Headers dinámicos, rate limiting inteligente
- **Múltiples Formatos**: CSV, SQLite, PostgreSQL con esquemas optimizados
- **Monitoreo en Tiempo Real**: Logs detallados y estadísticas de rendimiento

### 📊 **Análisis Técnico Incluido**
- **Comparación Scrapy vs Selenium vs Playwright**: Análisis completo con benchmarks reales
- **Implementaciones de Ejemplo**: Código funcional para las tres herramientas
- **Métricas de Rendimiento**: Datos reales de velocidad, memoria y eficiencia
- **Guías de Configuración**: Setup anti-detección para cada herramienta

### 🛡️ **Seguridad y Robustez**
- **Proxy Management**: Soporte TOR, VPN, proxies comerciales y gratuitos
- **Error Handling**: Sistema robusto de reintentos y fallbacks
- **Rate Limiting**: Respeto automático de límites del servidor
- **Verificación Automática**: Scripts de diagnóstico y validación

## 🚀 Inicio Rápido (30 segundos)

### 🍎 **macOS / Linux:**
```bash
git clone https://github.com/JimeFioni/imdb-scraper.git
cd imdb-scraper
./run.sh
```

### 🪟 **Windows:**
```bash
git clone https://github.com/JimeFioni/imdb-scraper.git
cd imdb-scraper
# Abrir Git Bash y ejecutar:
./run.sh
```

**¡Eso es todo!** El script configurará automáticamente el entorno virtual, instalará dependencias y ejecutará el scraper. Los datos se guardarán en `data/exports/peliculas.csv` y `data/exports/peliculas.db`.

### 🔍 **Verificación del Sistema:**
```bash
./verify_system.sh  # Diagnóstico completo del sistema
```

---

## 📁 Estructura del Proyecto

```
imdb_scraper/
├── 🕷️  imdb_scraper/           # Core del scraper Scrapy
│   ├── spiders/
│   │   └── top_movies.py       # Spider principal optimizado
│   ├── proxy_manager.py        # Sistema avanzado de proxies
│   ├── proxy_middleware.py     # Middleware de rotación
│   └── settings.py             # Configuración profesional
│
├── 📊 benchmark/               # Análisis de rendimiento
│   ├── scrapy_benchmark.py     # Benchmark con datos reales
│   └── performance_comparison.py
│
├── 💡 examples/                # Implementaciones comparativas
│   ├── selenium_scraper_advanced.py   # Selenium con anti-detección
│   ├── playwright_scraper_advanced.py # Playwright con stealth
│   └── imdb_configurations.py         # Configuraciones específicas
│
├── 🛡️  config/                 # Configuraciones
│   ├── proxies.json           # Config de proxies (TOR, VPN, comerciales)
│   └── docker/                # Docker Compose para VPN
│
├── 📖 docs/                   # Documentación técnica
│   ├── IMDB_TECHNICAL_COMPARISON.md  # Comparación completa
│   └── sql/                   # Guías SQL
│
├── 🔧 scripts/               # Scripts de utilidad
│   ├── install_comparison_deps.sh    # Instalación de Selenium/Playwright
│   └── run_technical_comparison.sh   # Demo comparativo
│
├── 📈 data/exports/          # Archivos generados
├── 📝 logs/                  # Sistema de logging
└── 🚀 Scripts principales    # run.sh, verify_system.sh, etc.
```

---

## ✅ Compatibilidad y Requisitos

### 🖥️ **Sistemas Operativos Soportados:**

| Sistema | Versión | Soporte | Notas |
|---------|---------|---------|-------|
| 🍎 **macOS** | 10.15+ | ✅ Completo | Todos los scripts funcionan |
| 🪟 **Windows 10/11** | | ✅ Completo | Usar Git Bash para scripts |
| 🪟 **Windows (CMD/PS)** | | ⚠️ Limitado | Solo comandos Python directos |
| 🐧 **Ubuntu** | 18.04+ | ✅ Completo | Todos los scripts funcionan |
| 🐧 **Debian** | 10+ | ✅ Completo | Todos los scripts funcionan |
| 🐧 **CentOS/RHEL** | 7+ | ✅ Completo | Todos los scripts funcionan |

### 🐍 **Versiones de Python:**

| Versión | Soporte | Estado |
|---------|---------|--------|
| Python 3.13 | ✅ | Totalmente testado |
| Python 3.12 | ✅ | Totalmente testado |
| Python 3.11 | ✅ | Totalmente testado |
| Python 3.10 | ✅ | Totalmente testado |
| Python 3.9 | ✅ | Totalmente testado |
| Python 3.8 | ✅ | Versión mínima |
| Python 3.7 | ❌ | No soportado |

### 📦 **Dependencias Principales:**

```txt
scrapy>=2.11.0              # Framework de web scraping
psycopg2-binary>=2.9.5      # Conector PostgreSQL
pandas>=2.0.0               # Análisis de datos
fake-useragent>=1.4.0       # User agents aleatorios
python-dotenv>=1.0.0        # Variables de entorno
```

### 🛠️ **Herramientas Opcionales:**

| Herramienta | Propósito | Instalación |
|-------------|-----------|-------------|
| 🐳 **Docker** | PostgreSQL containerizado | [Docker Desktop](https://www.docker.com/products/docker-desktop/) |
| 🐘 **PostgreSQL** | Base de datos local | [PostgreSQL.org](https://www.postgresql.org/download/) |
| 🍺 **Homebrew** | Gestor de paquetes (macOS) | [brew.sh](https://brew.sh/) |
| 📝 **Git** | Control de versiones | [git-scm.com](https://git-scm.com/) |

### 🚀 **Rendimiento Esperado:**

| Métrica | Valor | Descripción |
|---------|-------|-------------|
| ⏱️ **Tiempo de ejecución** | 2-3 minutos | 50 películas completas |
| 🎯 **Tasa de éxito** | >95% | Datos extraídos exitosamente |
| 💾 **Memoria RAM** | <100MB | Uso durante ejecución |
| 💿 **Espacio en disco** | <50MB | Proyecto completo |
| 🌐 **Conexión requerida** | Estable | Para acceso a IMDb |

### 🎬 Extracción de Datos
El scraper extrae la siguiente información de cada película:

- **Ranking**: Posición en el top de IMDb
- **Título**: Nombre de la película
- **Año**: Año de lanzamiento
- **Calificación**: Rating de IMDb (ej: 9.3)
- **Duración**: Duración en formato "2h 22m"
- **Metascore**: Puntuación de Metacritic (si está disponible)
- **Actores Principales**: Los 3 actores principales

### 🗄️ Persistencia de Datos
- **CSV**: Exportación tradicional para análisis con Excel/Google Sheets
- **SQLite**: Base de datos ligera para consultas rápidas
- **PostgreSQL**: Base de datos relacional completa con modelo normalizado
- **Modelo Relacional**: Tablas separadas para películas, actores, décadas y géneros

### 📊 Análisis SQL Avanzado
- **Consultas Estadísticas**: Promedios, desviaciones estándar, percentiles
- **Análisis Temporal**: Evolución por décadas y años
- **Correlación de Ratings**: Comparación IMDb vs Metascore
- **Window Functions**: Análisis de ventanas deslizantes y rankings
- **Procedimientos Almacenados**: Funciones personalizadas para análisis
- **Vistas Materializadas**: Optimización de consultas frecuentes

## 🛠️ Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| ![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white) | 3.8+ | Lenguaje principal |
| ![Scrapy](https://img.shields.io/badge/Scrapy-2.13%2B-green?logo=scrapy&logoColor=white) | 2.13+ | Framework de web scraping |
| ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-blue?logo=postgresql&logoColor=white) | 15+ | Base de datos relacional |
| ![SQLite](https://img.shields.io/badge/SQLite-3-blue?logo=sqlite&logoColor=white) | 3.x | Base de datos ligera |
| ![Docker](https://img.shields.io/badge/Docker-Latest-blue?logo=docker&logoColor=white) | Latest | Contenedorización de PostgreSQL |
| ![CSV](https://img.shields.io/badge/CSV-Built--in-orange?logo=microsoftexcel&logoColor=white) | Built-in | Exportación de datos |
| ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-blue?logo=postgresql&logoColor=white) | 15+ | Base de datos relacional |
| ![Docker](https://img.shields.io/badge/Docker-supported-blue?logo=docker&logoColor=white) | - | Contenerización y despliegue |

## 📊 Estadísticas del Proyecto

- 🎬 **50 películas** extraídas del Top de IMDb
- 📄 **7 campos de datos** por película
- �️ **3 formatos de salida**: CSV, SQLite, PostgreSQL
- 🔧 **Modelo relacional** completo con 5 tablas
- 📊 **20+ consultas SQL** avanzadas incluidas
- 🧪 **10 scripts de testing** incluidos
- ⚡ **100% funcional** y testeado
- 🐳 **Docker Ready** para PostgreSQL

## 📁 Estructura del Proyecto

```
imdb_scraper/
├── 📄 run.sh                          # Script principal de ejecución
├── 📄 README.md                       # Documentación principal  
├── 📄 LICENSE                         # Licencia del proyecto
├── 📄 .gitignore                      # Archivos ignorados por Git
│
├── 🎬 imdb_scraper/                   # Código fuente principal
│   ├── spiders/top_movies.py          # Spider principal IMDb
│   ├── pipelines.py                   # Pipelines de procesamiento
│   ├── postgresql_pipeline.py         # Pipeline PostgreSQL avanzado
│   ├── selector_factory.py            # Factory Pattern para selectores
│   └── settings.py                    # Configuración Scrapy
│
├── ⚙️ config/                         # Configuraciones centralizadas
│   ├── requirements.txt               # Dependencias Python
│   ├── project.yml                    # Configuración principal
│   ├── scrapy/scrapy.cfg              # Configuración Scrapy
│   ├── database/schema.sql            # Esquema PostgreSQL
│   └── docker/docker-compose.yml      # Configuración Docker
│
├── 💾 data/                           # Datos del proyecto
│   ├── raw/                           # Datos crudos (HTML, etc.)
│   ├── processed/                     # Datos procesados
│   ├── exports/                       # Archivos de salida (CSV, etc.)
│   └── backups/                       # Respaldos de datos
│
├── 📚 docs/                           # Documentación completa
│   ├── PROJECT_STRUCTURE.md           # Estructura del proyecto
│   ├── IMPLEMENTATION_SUMMARY.md      # Resumen de implementación
│   └── sql/SQL_ANALYSIS_GUIDE.md      # Guía de análisis SQL
│
├── 🛠️ tools/                          # Scripts y herramientas
│   ├── run_scraper.sh                 # Ejecutar scraper
│   ├── setup/setup_postgresql.sh      # Configurar PostgreSQL
│   ├── analysis/analyze_data.sh       # Análisis SQL interactivo
│   └── maintenance/test_complete.sh   # Suite de pruebas
│
├── 🧪 tests/                          # Pruebas del sistema
│   ├── unit/                          # Pruebas unitarias
│   └── integration/                   # Pruebas de integración
│
└── 📊 logs/                           # Archivos de log
    └── scrapy.log                     # Logs detallados
```
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
├── 📁 database/                   # Archivos relacionados a la base de datos
│   ├── docker-compose.yml         # Configuración de Docker
│   └── init_db.sql               # Script de inicialización de base de datos
└── 📁 venv/                       # Entorno virtual (creado localmente)
```

## 🚀 Instalación y Configuración

[![Quick Start](https://img.shields.io/badge/Quick%20Start-3%20Steps-brightgreen?style=for-the-badge&logo=rocket)](README.md)

### � Requisitos Previos

| Sistema | Requisitos |
|---------|------------|
| **🍎 macOS** | Python 3.8+, Git, Terminal |
| **🪟 Windows** | Python 3.8+, Git, PowerShell/CMD |
| **🐧 Linux** | Python 3.8+, Git, Bash |

### 🔧 Instalación Automática (Recomendada)

#### 🍎 **macOS / Linux:**
```bash
# 1. Clonar repositorio
git clone https://github.com/JimeFioni/imdb-scraper.git
cd imdb-scraper

# 2. Ejecutar (todo automático)
./run.sh
```

#### 🪟 **Windows (PowerShell):**
```powershell
# 1. Clonar repositorio
git clone https://github.com/JimeFioni/imdb-scraper.git
cd imdb-scraper

# 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate

# 3. Instalar dependencias
pip install -r config/requirements.txt

# 4. Ejecutar scraper
python -m scrapy crawl top_movies -s ITEM_PIPELINES='{"imdb_scraper.pipelines.CsvExportPipeline": 300}'
```

#### 🪟 **Windows (Git Bash):**
```bash
# 1. Clonar repositorio
git clone https://github.com/JimeFioni/imdb-scraper.git
cd imdb-scraper

# 2. Usar script de activación
./activate_venv.sh

# 3. Ejecutar scraper
./run_scraper_with_venv.sh
```

### ⚡ Instalación Manual

#### 🍎 **macOS / Linux:**
```bash
# 1. Clonar repositorio
git clone https://github.com/JimeFioni/imdb-scraper.git
cd imdb-scraper

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependencias
pip install -r config/requirements.txt

# 4. Ejecutar scraper
./run_scraper_with_venv.sh
```

#### 🪟 **Windows:**
```cmd
:: 1. Clonar repositorio
git clone https://github.com/JimeFioni/imdb-scraper.git
cd imdb-scraper

:: 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate.bat

:: 3. Instalar dependencias
pip install -r config\requirements.txt

:: 4. Ejecutar scraper
cd imdb_scraper
scrapy crawl top_movies
```

## 🎯 Uso del Sistema

### 🚀 **Método Recomendado (Menú Interactivo):**

#### 🍎 **macOS / Linux:**
```bash
./run.sh
```

#### 🪟 **Windows (Git Bash):**
```bash
./run.sh
```

#### 🪟 **Windows (PowerShell/CMD):**
```powershell
# Activar entorno virtual
venv\Scripts\activate

# Ejecutar scraper directamente
cd imdb_scraper
scrapy crawl top_movies
```

### 🎛️ **Scripts Disponibles:**

| Script | Descripción | macOS/Linux | Windows |
|--------|-------------|-------------|---------|
| `run.sh` | **Menú principal** | `./run.sh` | Git Bash: `./run.sh` |
| `run_scraper_with_venv.sh` | **Scraper completo** | `./run_scraper_with_venv.sh` | Git Bash: `./run_scraper_with_venv.sh` |
| `run_postgres_scraper.sh` | **Solo PostgreSQL** | `./run_postgres_scraper.sh` | Git Bash: `./run_postgres_scraper.sh` |
| `activate_venv.sh` | **Activar entorno** | `./activate_venv.sh` | Git Bash: `./activate_venv.sh` |
| `setup_postgres_local.sh` | **Configurar PostgreSQL** | `./setup_postgres_local.sh` | Git Bash: `./setup_postgres_local.sh` |

### 🐍 **Comando Directo Python:**

#### Todos los sistemas:
```bash
# 1. Activar entorno virtual
# macOS/Linux: source venv/bin/activate
# Windows: venv\Scripts\activate

# 2. Ejecutar scraper
cd imdb_scraper
scrapy crawl top_movies -L INFO

# 3. Ver resultados
# macOS/Linux: cat ../data/exports/peliculas.csv
# Windows: type ..\data\exports\peliculas.csv
```

### 🔧 **Configuración PostgreSQL:**

#### 🍎 **macOS (con Homebrew):**
```bash
# Instalar PostgreSQL
brew install postgresql@15

# Configurar automáticamente
./setup_postgres_local.sh

# Ejecutar con PostgreSQL
./run_postgres_scraper.sh
```

#### 🪟 **Windows:**
```powershell
# 1. Descargar PostgreSQL desde: https://www.postgresql.org/download/windows/
# 2. Instalar con configuración predeterminada
# 3. Crear base de datos manualmente o usar Docker

# Usar Docker (recomendado para Windows)
docker-compose up -d

# Ejecutar scraper
python -m scrapy crawl top_movies
```

#### 🐳 **Docker (Todos los sistemas):**
```bash
# Configurar PostgreSQL con Docker
./setup_docker.sh

# O manualmente:
docker-compose up -d
```

---

## 🆕 Nuevas Características Añadidas (Enero 2025)

### 🔬 **Análisis Técnico Comparativo**
- **Comparación Scrapy vs Selenium vs Playwright**: Documento técnico completo con benchmarks reales
- **Implementaciones Funcionales**: Ejemplos prácticos de las tres herramientas configuradas para IMDb
- **Métricas de Rendimiento**: Datos reales de velocidad (0.27 items/s Scrapy vs 0.07 items/s Selenium)
- **Recomendaciones Técnicas**: Justificación basada en datos para elección de herramienta

### 🛡️ **Sistema Avanzado de Proxies**
- **Rotación Automática**: Cambio inteligente entre proxies con fallback
- **Soporte Múltiple**: TOR, VPN, proxies comerciales y gratuitos
- **Validación en Tiempo Real**: Verificación automática de conectividad
- **Configuración Docker**: Setup VPN con docker-compose incluido

### 📊 **Benchmarking y Monitoreo**
- **Benchmark Automático**: Scripts de medición de rendimiento
- **Análisis de Memoria**: Medición precisa de uso de recursos
- **Logging Avanzado**: Sistema de logs rotativos con niveles
- **Verificación del Sistema**: Diagnóstico automático completo

### 🎯 **Configuraciones Específicas para IMDb**
- **Selectores Optimizados**: CSS selectors específicos para estructura de IMDb
- **Rate Limiting Inteligente**: Respeto automático de límites del servidor
- **Headers Dinámicos**: Rotación de user-agents y headers
- **Error Handling**: Sistema robusto de manejo de errores y reintentos

### 📖 **Documentación Técnica**
- **Guía Completa de Comparación**: `docs/IMDB_TECHNICAL_COMPARISON.md`
- **Ejemplos Prácticos**: Código funcional para Selenium y Playwright
- **Scripts de Instalación**: Setup automático de dependencias opcionales
- **Troubleshooting**: Guía completa de resolución de problemas

---

## 🎬 Análisis Técnico: ¿Por qué Scrapy para IMDb?

### 📊 **Datos Reales del Benchmark**

| Herramienta | Tiempo (10 items) | Memoria | Items/segundo | Eficiencia |
|-------------|-------------------|---------|---------------|------------|
| **Scrapy** | 41s | 5MB | 0.27/s | ⭐⭐⭐⭐⭐ |
| **Selenium** | 143s (est.) | 150MB | 0.07/s | ⭐⭐ |
| **Playwright** | 90s (est.) | 80MB | 0.11/s | ⭐⭐⭐⭐ |

### 🎯 **¿Por qué Scrapy es Óptimo para IMDb?**

1. **Contenido Estático**: IMDb Top 250 no requiere JavaScript
2. **Eficiencia de Recursos**: 3.5x más rápido que Selenium
3. **Arquitectura HTTP**: Perfecta para contenido server-side rendered
4. **Escalabilidad**: Maneja 250 items sin problemas
5. **Mantenimiento**: Código más simple y estable

### 🔄 **¿Cuándo Usar Selenium/Playwright?**

```python
# Casos donde otras herramientas son mejores:
SELENIUM_CASES = [
    "JavaScript crítico (SPAs)",
    "Interacciones complejas (clicks, forms)",
    "Debugging visual necesario",
    "Login/autenticación requerida"
]

PLAYWRIGHT_CASES = [
    "Anti-bot detection intensivo",
    "Aplicaciones modernas con JS",
    "Concurrencia asyncio requerida",
    "APIs modernas de navegador"
]
```

**Ver análisis completo**: [`docs/IMDB_TECHNICAL_COMPARISON.md`](docs/IMDB_TECHNICAL_COMPARISON.md)

---

## 🌐 Sistema Avanzado de Proxies y Control de Red

### 🚀 **Funcionalidades del Sistema de Proxies**

El proyecto incluye un **sistema avanzado de proxies** que permite:

- ✅ **Rotación automática de IPs** para evitar bloqueos
- ✅ **Integración con TOR** para anonimato máximo
- ✅ **Soporte VPN** vía Docker con healthcheck
- ✅ **Fallback inteligente** a conexión directa
- ✅ **Validación automática** de proxies
- ✅ **Logging detallado** de IPs usadas por request
- ✅ **Estadísticas en tiempo real** de rotación

### ⚙️ **Configuración de Proxies**

#### 1. **Configuración Básica**

Editar el archivo `config/proxies.json`:

```json
{
  "proxies": [
    {
      "host": "proxy1.example.com",
      "port": 8080,
      "username": "tu_usuario",
      "password": "tu_password",
      "protocol": "http",
      "country": "US",
      "provider": "ProxyProvider1"
    },
    {
      "host": "proxy2.example.com",
      "port": 3128,
      "username": "usuario2",
      "password": "password2",
      "protocol": "http",
      "country": "UK",
      "provider": "ProxyProvider2"
    },
    {
      "host": "127.0.0.1",
      "port": 9050,
      "protocol": "socks5",
      "country": "TOR"
    }
  ]
}
```

#### 2. **Activar Rotación de Proxies**

En `imdb_scraper/settings.py`:

```python
# Habilitar rotación de proxies
PROXY_ROTATION_ENABLED = True  # Cambiar a True

# Configuración avanzada
PROXY_RETRY_TIMES = 3
PROXY_ROTATION_INTERVAL = 10  # Rotar cada 10 requests
```

### 🐳 **Configuración con Docker (TOR + VPN)**

#### 1. **Setup Automático**

```bash
# Configuración interactiva completa
./setup_proxy_network.sh
```

#### 2. **Setup Manual VPN**

```bash
# Configurar variables de entorno
export VPN_USER="tu_usuario_vpn"
export VPN_PASSWORD="tu_password_vpn"

# Iniciar infraestructura VPN + TOR
cd config/docker
docker-compose -f docker-compose-vpn.yml up -d

# Verificar estado
docker ps
```

#### 3. **Verificar Conexión VPN/TOR**

```bash
# Verificar IP a través de TOR
curl --socks5 127.0.0.1:9050 https://httpbin.org/ip

# Verificar IP a través de VPN
curl --proxy 127.0.0.1:8888 https://httpbin.org/ip
```

### 🔧 **Comandos de Gestión**

#### **Verificar Sistema Completo**

```bash
# Verificación automática de todo el sistema
./verify_system.sh
```

#### **Probar Proxies Manualmente**

```bash
# Activar entorno virtual
source venv/bin/activate

# Probar proxy manager
python -c "
from imdb_scraper.proxy_manager import ProxyRotator
proxy_manager = ProxyRotator()

# Ver IP actual
print(f'IP directa: {proxy_manager.get_current_ip()}')

# Probar todos los proxies configurados
for proxy in proxy_manager.proxies:
    if proxy_manager.test_proxy(proxy):
        print(f'✅ {proxy.host}:{proxy.port} - Funcionando')
    else:
        print(f'❌ {proxy.host}:{proxy.port} - No funciona')

# Ver estadísticas
stats = proxy_manager.get_stats()
print(f'Total proxies: {stats[\"total_proxies\"]}')
print(f'Proxies activos: {stats[\"active_proxies\"]}')
"
```

#### **Ejecutar Scraper con Proxies**

```bash
# Método 1: Script automático
./run.sh
# Seleccionar opción 4: "Scraper con rotación de proxies"

# Método 2: Comando directo
source venv/bin/activate
scrapy crawl top_movies -s PROXY_ROTATION_ENABLED=True
```

### 📊 **Monitoreo y Logs**

#### **Ver Logs de Proxies**

```bash
# Logs en tiempo real
tail -f logs/proxy_manager.log

# Estadísticas guardadas
cat logs/proxy_stats.json
```

#### **Ejemplo de Logs de Rotación**

```
2025-07-28 19:30:15 - proxy_manager - INFO: Request exitoso usando proxy proxy1.example.com:8080, IP: 192.168.1.100
2025-07-28 19:30:18 - proxy_manager - INFO: Request exitoso usando proxy proxy2.example.com:3128, IP: 10.0.0.50
2025-07-28 19:30:21 - proxy_manager - INFO: Request exitoso usando proxy 127.0.0.1:9050, IP: 185.220.101.42
```

#### **Ver Estadísticas de IPs**

```bash
# Ver últimas IPs usadas
python -c "
from imdb_scraper.proxy_manager import ProxyRotator
import json

proxy_manager = ProxyRotator()
stats = proxy_manager.get_stats()

print('🌐 Últimas IPs utilizadas:')
for record in stats['ip_history'][-5:]:
    print(f\"  {record['timestamp']}: {record['ip_used']} via {record['proxy']}\")

print(f\"\\n📊 Total IPs únicas: {stats['unique_ips_used']}\")
print(f\"📈 Total requests: {stats['total_requests']}\")
"
```

### 🛡️ **Proveedores de Proxies Recomendados**

#### **Proxies Premium (Recomendados para producción)**

| Proveedor | Tipo | Precio (aprox.) | Calidad | Soporte |
|-----------|------|-----------------|---------|---------|
| **ProxyMesh** | Rotating | $20-100/mes | ⭐⭐⭐⭐⭐ | 24/7 |
| **Smartproxy** | Residential | $75-500/mes | ⭐⭐⭐⭐⭐ | 24/7 |
| **Bright Data** | Enterprise | $500+/mes | ⭐⭐⭐⭐⭐ | 24/7 |
| **Storm Proxies** | Datacenter | $50-200/mes | ⭐⭐⭐⭐ | Business hours |

#### **Proxies Gratuitos (Solo para testing)**

| Tipo | Fiabilidad | Velocidad | Anonimato |
|------|------------|-----------|-----------|
| **TOR** | Media | Lenta | Máximo |
| **Proxies públicos** | Baja | Variable | Bajo |
| **VPN gratuitas** | Baja | Lenta | Medio |

### 🔍 **Solución de Problemas de Proxies**

#### **Errores Comunes**

```bash
# Error: "ProxyConfig.__init__() got an unexpected keyword argument"
# Solución: Verificar formato de config/proxies.json

# Error: "Connection timeout"
# Solución: Verificar conectividad del proxy
curl --proxy http://usuario:password@proxy.example.com:8080 https://httpbin.org/ip

# Error: "All proxies failed"
# Solución: Usar fallback a conexión directa
grep "PROXY_FALLBACK_TO_DIRECT = True" imdb_scraper/settings.py
```

#### **Debugging de Proxies**

```bash
# Modo debug detallado
export SCRAPY_DEBUG=1
scrapy crawl top_movies -s LOG_LEVEL=DEBUG -s PROXY_ROTATION_ENABLED=True

# Ver tráfico de red
tcpdump -i en0 host proxy.example.com
```

### 📈 **Optimización de Rendimiento**

#### **Configuración para Alto Volumen**

```python
# En settings.py
CONCURRENT_REQUESTS = 8              # Aumentar concurrencia
DOWNLOAD_DELAY = 1                   # Reducir delay
PROXY_ROTATION_INTERVAL = 5          # Rotar más frecuentemente
RETRY_TIMES = 5                      # Más reintentos
```

#### **Configuración Conservadora (Anti-bloqueo)**

```python
# En settings.py  
CONCURRENT_REQUESTS = 1              # Minimal concurrency
DOWNLOAD_DELAY = 3                   # Delay más largo
RANDOMIZE_DOWNLOAD_DELAY = 2.0       # Más variación
PROXY_ROTATION_INTERVAL = 15         # Rotar menos frecuentemente
```

---

## 🔬 Scripts de Análisis y Benchmarking

### 📊 **Scripts de Comparación Técnica**

#### **Ejecutar Comparación Completa**
```bash
# Instalar dependencias para comparación (Selenium, Playwright)
./scripts/install_comparison_deps.sh

# Ejecutar comparación técnica completa
./scripts/run_technical_comparison.sh

# Ver resultados del análisis
./scripts/show_technical_comparison.sh
```

#### **Benchmark Individual de Scrapy**
```bash
# Ejecutar benchmark con diferentes tamaños
python benchmark/scrapy_benchmark.py

# Ver resultados en logs/scrapy_benchmark.log
tail -f logs/scrapy_benchmark.log
```

#### **Ejemplos Prácticos**
```bash
# Probar Selenium (requiere instalación previa)
python examples/selenium_scraper_advanced.py --limit 5 --headless

# Probar Playwright (requiere instalación previa)  
python examples/playwright_scraper_advanced.py --limit 5 --headless

# Ver configuraciones específicas para IMDb
python examples/imdb_configurations.py
```

### 🔍 **Scripts de Verificación y Diagnóstico**

#### **Verificación Completa del Sistema**
```bash
# Ejecutar diagnóstico completo
./verify_system.sh

# Verificar solo proxies
python -c "
from imdb_scraper.proxy_manager import ProxyRotator
proxy_manager = ProxyRotator()
print(f'✅ Sistema de proxies: {len(proxy_manager.proxies)} configurados')
print(f'🌐 IP actual: {proxy_manager.get_current_ip()}')
"
```

#### **Diagnóstico Completo del Entorno**
```bash
# Script completo de diagnóstico
./diagnostico_completo.sh

# Verificar solo dependencias de Python
python -c "
import sys
packages = ['scrapy', 'requests', 'beautifulsoup4']
for pkg in packages:
    try:
        __import__(pkg)
        print(f'✅ {pkg}')
    except ImportError:
        print(f'❌ {pkg} - No instalado')
"
```

### 📈 **Análisis de Resultados**

#### **Ver Métricas de Rendimiento**
```bash
# Analizar archivos de benchmark generados
ls -la benchmark_results_*.json

# Ver estadísticas de la última ejecución
python -c "
import json
import glob

files = glob.glob('benchmark_results_*.json')
if files:
    with open(max(files), 'r') as f:
        data = json.load(f)
    
    print('📊 ÚLTIMOS RESULTADOS:')
    for test in data['tests']:
        size = test['test_size']
        scrapy = test['results']['scrapy_actual']
        print(f'   {size} items: {scrapy[\"execution_time_seconds\"]}s, {scrapy[\"items_per_second\"]} items/s')
"
```

---

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

## 🔧 Solución de Problemas

### 🍎 **Problemas comunes en macOS:**

#### Python no encontrado:
```bash
# Instalar Python con Homebrew
brew install python3

# O usar python3 directamente
python3 -m venv venv
```

#### Permisos de ejecución:
```bash
# Dar permisos a los scripts
chmod +x *.sh
```

#### PostgreSQL no funciona:
```bash
# Instalar PostgreSQL
brew install postgresql@15

# Iniciar servicio
brew services start postgresql@15
```

### 🪟 **Problemas comunes en Windows:**

#### Scripts .sh no funcionan en CMD/PowerShell:
```powershell
# Solución 1: Usar Git Bash (recomendado)
# Descargar Git para Windows: https://git-scm.com/download/win

# Solución 2: Ejecutar comando directo
venv\Scripts\activate
cd imdb_scraper
scrapy crawl top_movies
```

#### Python no encontrado:
```cmd
:: Instalar Python desde: https://www.python.org/downloads/
:: Asegurar que esté en PATH durante la instalación
```

#### Error de codificación:
```powershell
# Configurar codificación UTF-8
$env:PYTHONIOENCODING="utf-8"
chcp 65001
```

#### PostgreSQL complejo en Windows:
```powershell
# Usar Docker (más fácil)
docker-compose up -d

# O instalar PostgreSQL desde:
# https://www.postgresql.org/download/windows/
```

### 🐧 **Problemas comunes en Linux:**

#### Dependencias del sistema:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-venv python3-pip git

# CentOS/RHEL
sudo yum install python3 python3-venv python3-pip git

# Arch Linux
sudo pacman -S python python-venv python-pip git
```

#### PostgreSQL en Linux:
```bash
# Ubuntu/Debian
sudo apt install postgresql postgresql-contrib

# CentOS/RHEL
sudo yum install postgresql postgresql-server

# Configurar
sudo -u postgres createuser imdb_user
sudo -u postgres createdb imdb_scraper_db
```

### ⚠️ **Problemas generales:**

#### Si no funciona nada:
1. **Verificar Python:** `python --version` o `python3 --version`
2. **Verificar Git:** `git --version`
3. **Recrear entorno virtual:** `rm -rf venv && python -m venv venv`
4. **Reinstalar dependencias:** `pip install -r config/requirements.txt`
5. **Usar modo diagnóstico:** `./diagnostico_completo.sh`

#### Si IMDb cambia la estructura:
```bash
# Ejecutar diagnósticos
./diagnostico_completo.sh

# Ver logs detallados
tail -f logs/scrapy.log

# Probar selectores manualmente en tests/
```

#### Archivos de salida no se generan:
```bash
# Verificar permisos de escritura
ls -la data/exports/

# Crear directorios manualmente
mkdir -p data/exports logs

# Verificar espacio en disco
df -h .
```

### 📧 **Obtener Ayuda:**

Si sigues teniendo problemas:
1. 🔍 Ejecuta `./diagnostico_completo.sh` y comparte el resultado
2. 📋 Incluye tu sistema operativo y versión de Python
3. 📝 Describe exactamente qué error obtienes
4. 🐛 Abre un issue en GitHub con la información completa

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

## 🐘 PostgreSQL - Base de Datos Relacional

### 🚀 Configuración Automática con Docker

[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Docker%20Ready-blue?style=for-the-badge&logo=docker)](config/docker/docker-compose.yml)

```bash
# Configuración automática completa
./tools/setup/setup_postgresql.sh
```

Este script realiza:
- ✅ Verificación de Docker
- 🐳 Configuración de PostgreSQL + pgAdmin
- 🗄️ Creación del modelo relacional
- 🔧 Verificación de conexión
- 📊 Ejecución opcional del scraper

### 📊 Modelo Relacional

```sql
-- Estructura de tablas principales
peliculas (id, titulo, anio, calificacion, duracion_minutos, metascore, ranking)
actores (id, pelicula_id, nombre, posicion)
decadas (id, decada, nombre, descripcion)
generos (id, nombre, descripcion)
pelicula_generos (pelicula_id, genero_id)
```

### 🔍 Análisis SQL Avanzado

```bash
# Ejecutar análisis interactivo
./tools/analysis/analyze_data.sh
```

**Consultas incluidas:**
1. **Análisis Temporal**: Top 5 décadas con mayor duración promedio
2. **Estadísticas**: Desviación estándar de calificaciones por año
3. **Comparativo**: Diferencias entre IMDb y Metascore
4. **Window Functions**: Rankings y promedios móviles
5. **Actores**: Análisis de frecuencia y correlaciones
6. **Vistas Materializadas**: Consultas optimizadas

### 🌐 Interfaz Web (pgAdmin)
- **URL**: http://localhost:8080
- **Usuario**: admin@imdb-scraper.local
- **Contraseña**: admin123

### 🔧 Conexión Directa
```bash
# Consola SQL directa
docker-compose exec postgres psql -U imdb_user -d imdb_scraper_db

# Variables de conexión
Host: localhost
Puerto: 5432
Base de datos: imdb_scraper_db
Usuario: imdb_user
Contraseña: imdb_secure_2024
```

---

## � Documentación Técnica Completa

### 📖 **Documentos Incluidos**

| Documento | Descripción | Contenido |
|-----------|-------------|-----------|
| [`docs/IMDB_TECHNICAL_COMPARISON.md`](docs/IMDB_TECHNICAL_COMPARISON.md) | **Comparación Técnica Completa** | Análisis Scrapy vs Selenium vs Playwright |
| [`docs/sql/SQL_ANALYSIS_GUIDE.md`](docs/sql/SQL_ANALYSIS_GUIDE.md) | **Guía de Análisis SQL** | Consultas avanzadas y optimización |
| [`config/proxies.json`](config/proxies.json) | **Configuración de Proxies** | Formato y ejemplos de configuración |
| [`logs/`](logs/) | **Sistema de Logging** | Logs detallados del sistema |

### 🔍 **Análisis Técnico Específico para IMDb**

#### **¿Por qué Scrapy es la mejor opción para IMDb Top 250?**

1. **Contenido Estático**: IMDb Top 250 es HTML server-side rendered
2. **Eficiencia**: 0.27 items/segundo con solo 5MB de memoria
3. **Escalabilidad**: Maneja 250 items sin problemas de rendimiento
4. **Mantenimiento**: Código más simple y estable que alternativas

#### **Métricas Reales (Benchmark ejecutado)**
```
Scrapy:     41s para 10 items | 5MB RAM    | 0.27 items/s
Selenium:   143s estimado     | 150MB RAM  | 0.07 items/s  
Playwright: 90s estimado      | 80MB RAM   | 0.11 items/s
```

### 🛠️ **Herramientas y Scripts Avanzados**

#### **Sistema de Proxies**
- Rotación automática de IPs
- Soporte TOR, VPN y proxies comerciales
- Validación en tiempo real
- Fallback inteligente

#### **Benchmarking**
- Medición automática de rendimiento
- Comparación entre herramientas
- Análisis de memoria y CPU
- Reportes detallados

#### **Verificación**
- Diagnóstico completo del sistema
- Validación de dependencias
- Verificación de configuraciones
- Tests de conectividad

---

## 🚀 Próximos Pasos y Extensiones

### 📈 **Posibles Mejoras**

1. **Scraping Avanzado**: Agregar reviews, ratings de usuarios, trailers
2. **Machine Learning**: Análisis de sentimientos de reviews
3. **API REST**: Endpoint para consultar datos extraídos
4. **Dashboard**: Interfaz web para visualización de datos
5. **Alertas**: Notificaciones de nuevas películas en Top 250

### 🔄 **Integración con Otras Herramientas**

```bash
# Integración con Apache Airflow para scheduling
# Integración con Tableau/PowerBI para visualización
# Exportación a formatos adicionales (JSON, Parquet)
# API GraphQL para consultas complejas
```

---

## 🤝 Contribuir

### 🐛 **Reportar Problemas**

Si encuentras algún problema:

1. **Verifica** que hayas seguido todos los pasos de instalación
2. **Ejecuta** `./verify_system.sh` para diagnóstico
3. **Revisa** los logs en `logs/` para errores específicos
4. **Crea** un issue en GitHub con:
   - Sistema operativo y versión
   - Versión de Python
   - Output completo del error
   - Archivos de log relevantes

### 💡 **Contribuciones**

¡Las contribuciones son bienvenidas! Áreas de interés:

- **Optimización de rendimiento**: Mejoras en velocidad de scraping
- **Nuevos selectores**: Adaptaciones a cambios en IMDb
- **Documentación**: Mejoras en guías y ejemplos
- **Testing**: Pruebas automatizadas adicionales
- **Herramientas**: Scripts de utilidad adicionales

### 🔄 **Proceso de Contribución**

1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit con mensajes descriptivos
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

---

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT** - ver [LICENSE](LICENSE) para detalles.

### ⚖️ **Uso Responsable**

Este scraper está diseñado para:
- ✅ **Uso educativo** y de aprendizaje
- ✅ **Análisis de datos** público de IMDb
- ✅ **Respeto de robots.txt** y rate limiting
- ✅ **Cumplimiento de términos** de servicio

**⚠️ Importante**: Úsalo de manera responsable y respeta los términos de servicio de IMDb.

---

## 👨‍💻 Autor

**Desarrollado por [Tu Nombre]**

- 📧 Email: tu.email@ejemplo.com
- 🌐 GitHub: [@tu-usuario](https://github.com/tu-usuario)
- 💼 LinkedIn: [Tu Perfil](https://linkedin.com/in/tu-perfil)

---

## ⭐ ¿Te Gustó el Proyecto?

Si este proyecto te resultó útil:

- ⭐ **Dale una estrella** en GitHub
- 🔄 **Compártelo** con otros desarrolladores
- 🐛 **Reporta bugs** si encuentras alguno
- 💡 **Sugiere mejoras** en los issues
- 🤝 **Contribuye** con código o documentación

---

## 🎯 Resumen de Funcionalidades

✅ **Web Scraping Profesional** con Scrapy optimizado para IMDb  
✅ **Sistema Avanzado de Proxies** con rotación y fallback  
✅ **Análisis Técnico Comparativo** Scrapy vs Selenium vs Playwright  
✅ **Múltiples Formatos de Salida** CSV, SQLite, PostgreSQL  
✅ **Benchmarking y Métricas** de rendimiento en tiempo real  
✅ **Configuración Anti-Detección** headers dinámicos y rate limiting  
✅ **Scripts de Verificación** diagnóstico automático completo  
✅ **Documentación Técnica** análisis detallado y guías  
✅ **Docker Support** para VPN y base de datos  
✅ **Logging Avanzado** sistema de logs rotativos  

**🎬 ¡Disfruta explorando los datos de las mejores películas de IMDb!**
