# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
import time
import logging

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

logger = logging.getLogger(__name__)


class ImdbScraperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    async def process_start(self, start):
        # Called with an async iterator over the spider start() method or the
        # maching method of an earlier spider middleware.
        async for item_or_request in start:
            yield item_or_request

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class ImdbScraperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class RandomUserAgentMiddleware:
    """Middleware para rotar User-Agents aleatoriamente"""
    
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36'
        ]
    
    def process_request(self, request, spider):
        """Asigna un User-Agent aleatorio a cada request"""
        ua = random.choice(self.user_agents)
        request.headers['User-Agent'] = ua
        
        logger.debug(f"🤖 User-Agent asignado: {ua[:50]}...")
        return None


class RandomDelayMiddleware:
    """Middleware para añadir delays aleatorios entre requests"""
    
    def __init__(self):
        self.min_delay = 1.0
        self.max_delay = 3.0
    
    def process_request(self, request, spider):
        """Añade delay aleatorio antes del request"""
        delay = random.uniform(self.min_delay, self.max_delay)
        
        logger.debug(f"⏱️ Delay aleatorio: {delay:.2f}s antes de {request.url}")
        time.sleep(delay)
        
        return None


class NetworkResilienceMiddleware:
    """Middleware para mejorar la resiliencia de red"""
    
    def __init__(self):
        self.retry_http_codes = [500, 502, 503, 504, 408, 429]
        self.max_retries = 3
        
    def process_response(self, request, response, spider):
        """Maneja respuestas con códigos de error específicos"""
        if response.status in self.retry_http_codes:
            retries = request.meta.get('retry_times', 0)
            
            if retries < self.max_retries:
                retry_delay = (2 ** retries) + random.uniform(0, 1)
                
                logger.warning(
                    f"⚠️ HTTP {response.status} - Reintento #{retries + 1} "
                    f"en {retry_delay:.2f}s para {request.url}"
                )
                
                time.sleep(retry_delay)
                
                # Crear nueva request con contador de reintentos
                retry_req = request.copy()
                retry_req.meta['retry_times'] = retries + 1
                retry_req.dont_filter = True
                
                return retry_req
            else:
                logger.error(
                    f"❌ Máximo reintentos alcanzado para {request.url} "
                    f"(HTTP {response.status})"
                )
        
        return response
    
    def process_exception(self, request, exception, spider):
        """Maneja excepciones de red"""
        retries = request.meta.get('retry_times', 0)
        
        if retries < self.max_retries:
            retry_delay = (2 ** retries) + random.uniform(0, 1)
            
            logger.warning(
                f"⚠️ Excepción {type(exception).__name__} - "
                f"Reintento #{retries + 1} en {retry_delay:.2f}s"
            )
            
            time.sleep(retry_delay)
            
            retry_req = request.copy()
            retry_req.meta['retry_times'] = retries + 1
            retry_req.dont_filter = True
            
            return retry_req
        
        logger.error(f"❌ Máximo reintentos por excepción: {exception}")
        return None
