# Scrapy settings for imdb_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "imdb_scraper"

SPIDER_MODULES = ["imdb_scraper.spiders"]
NEWSPIDER_MODULE = "imdb_scraper.spiders"

ADDONS = {}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "imdb_scraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Concurrency and throttling settings
CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 3  # Aumentado para evitar bloqueos con proxies
RANDOMIZE_DOWNLOAD_DELAY = 1.0  # Más variación para parecer más humano
DOWNLOAD_TIMEOUT = 30  # Timeout específico para conexiones con proxy

# Retry settings with exponential backoff
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]
RETRY_PRIORITY_ADJUST = -1

# AutoThrottle with exponential backoff
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 30
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = False

# Exponential backoff factor
BACKOFF_FACTOR = 2.0

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "imdb_scraper.middlewares.ImdbScraperSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # Middleware de proxies ORIGINAL integrado con proxy_manager.py
    "imdb_scraper.proxy_middleware.ProxyRotationMiddleware": 350,
    "imdb_scraper.proxy_middleware.TorRotationMiddleware": 351,
    
    # Middlewares personalizados
    "imdb_scraper.middlewares.RandomUserAgentMiddleware": 400,
    "imdb_scraper.middlewares.RandomDelayMiddleware": 450,
    "imdb_scraper.middlewares.NetworkResilienceMiddleware": 500,
    
    # Sistema de proxies consolidado usando proxy_middleware.py + proxy_manager.py
    
    # Deshabilitar retry por defecto (usa el personalizado del proxy_middleware)
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": None,
    
    # Middleware base
    "imdb_scraper.middlewares.ImdbScraperDownloaderMiddleware": 543,
}

# ===============================================
# CONFIGURACIÓN AVANZADA DE PROXIES Y RED
# ===============================================

# Sistema de proxies rotativos avanzado
PROXY_ROTATION_ENABLED = True  # HABILITADO para pruebas
PROXY_CONFIG_FILE = 'config/proxies.json'
PROXY_IP_VERIFICATION = True  # Verificar IP en cada rotación
PROXY_FALLBACK_ENABLED = True  # Fallback a conexión directa si todos fallan

# Configuración de rotación automática
REQUESTS_PER_PROXY = 5  # Rotar cada 5 requests
PROXY_RETRY_ATTEMPTS = 3
PROXY_HEALTH_CHECK_INTERVAL = 300  # 5 minutos

# Configuración de TOR (Actualizada)
TOR_ROTATION_ENABLED = True  # HABILITADO para pruebas
TOR_ROTATION_INTERVAL = 8  # Rotar identidad cada 8 requests
TOR_CONTROL_PORT = 9051
TOR_SOCKS_PORT = 9050
TOR_HTTP_PORT = 8118
TOR_CONTROL_PASSWORD = ''

# Configuración de VPN automática
VPN_ROTATION_ENABLED = False  # Habilitar para usar VPN con Docker
VPN_DOCKER_IMAGE = 'qmcgaw/gluetun'
VPN_TARGET_COUNTRIES = ['US', 'UK', 'CA', 'DE']

# URLs de verificación de IP
IP_CHECK_URLS = [
    'https://httpbin.org/ip',
    'https://api.ipify.org?format=json',
    'https://jsonip.com'
]

# Configuración de proxy fallback
PROXY_FALLBACK_ENABLED = True
PROXY_FALLBACK_TO_DIRECT = True  # Usar conexión directa si todos los proxies fallan

# Timeouts específicos para proxies
PROXY_CONNECT_TIMEOUT = 30
PROXY_READ_TIMEOUT = 60

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "imdb_scraper.pipelines.ImdbScraperPipeline": 300,
    "imdb_scraper.database_pipeline.DatabasePipeline": 400,
    "imdb_scraper.postgresql_pipeline.PostgreSQLPipeline": 450,  # Habilitado - PostgreSQL configurado
    "imdb_scraper.pipelines.CsvExportPipeline": 500,
}

# ===============================================
# CONFIGURACIÓN POSTGRESQL
# ===============================================
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_DB = "imdb_scraper_db"
POSTGRES_USER = "imdb_user"
POSTGRES_PASSWORD = "imdb_secure_2024"

# ===============================================
# CONFIGURACIÓN LOGGING AVANZADO
# ===============================================
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'

# Logs específicos
LOG_FILE = '../logs/scrapy.log'

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8"
