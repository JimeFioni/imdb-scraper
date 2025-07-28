#!/usr/bin/env python3
"""
Benchmark simplificado centrado en Scrapy con métricas reales
Incluye comparación teórica con Selenium y Playwright
"""

import subprocess
import time
import psutil
import json
import os
import logging
from typing import Dict, List
import sys
from datetime import datetime

class ScrapyBenchmark:
    """Benchmark de rendimiento de Scrapy con comparación teórica"""
    
    def __init__(self):
        self.results = {}
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        logger = logging.getLogger('scrapy_benchmark')
        logger.setLevel(logging.INFO)
        
        os.makedirs('logs', exist_ok=True)
        handler = logging.FileHandler('logs/scrapy_benchmark.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    def measure_system_resources(self) -> Dict:
        """Medir recursos del sistema"""
        process = psutil.Process()
        return {
            'memory_mb': process.memory_info().rss / 1024 / 1024,
            'cpu_percent': process.cpu_percent(),
            'system_memory_percent': psutil.virtual_memory().percent,
            'system_cpu_percent': psutil.cpu_percent(interval=1)
        }
    
    def run_scrapy_test(self, item_limit: int = 50) -> Dict:
        """Ejecutar test de rendimiento de Scrapy"""
        self.logger.info(f"🚀 Iniciando benchmark Scrapy con {item_limit} items...")
        
        # Medición inicial
        resources_before = self.measure_system_resources()
        start_time = time.time()
        
        try:
            # Ejecutar Scrapy con límite
            cmd = [
                'scrapy', 'crawl', 'top_movies',
                '-s', f'CLOSESPIDER_ITEMCOUNT={item_limit}',
                '-s', 'LOG_LEVEL=WARNING',
                '-o', f'benchmark_output_{item_limit}.csv'
            ]
            
            result = subprocess.run(
                cmd, 
                cwd='.', 
                capture_output=True, 
                text=True, 
                timeout=120
            )
            
            end_time = time.time()
            resources_after = self.measure_system_resources()
            
            execution_time = end_time - start_time
            memory_used = resources_after['memory_mb'] - resources_before['memory_mb']
            
            # Verificar archivo de salida
            output_file = f'benchmark_output_{item_limit}.csv'
            items_scraped = 0
            
            if os.path.exists(output_file):
                with open(output_file, 'r') as f:
                    items_scraped = max(0, len(f.readlines()) - 1)  # -1 para header
                os.remove(output_file)  # Limpiar
            
            metrics = {
                'tool': 'scrapy',
                'items_target': item_limit,
                'items_scraped': items_scraped,
                'execution_time_seconds': round(execution_time, 2),
                'memory_used_mb': round(memory_used, 2),
                'items_per_second': round(items_scraped / execution_time, 2) if execution_time > 0 else 0,
                'memory_efficiency': round(items_scraped / max(memory_used, 1), 2),
                'success_rate': round((items_scraped / item_limit) * 100, 2) if item_limit > 0 else 0,
                'stdout': result.stdout if result.returncode != 0 else "",
                'stderr': result.stderr if result.returncode != 0 else "",
                'return_code': result.returncode
            }
            
            self.logger.info(f"✅ Scrapy completado: {items_scraped}/{item_limit} items en {execution_time:.2f}s")
            return metrics
            
        except subprocess.TimeoutExpired:
            self.logger.error("❌ Scrapy timeout después de 120 segundos")
            return {
                'tool': 'scrapy',
                'items_target': item_limit,
                'error': 'timeout',
                'execution_time_seconds': 120
            }
        except Exception as e:
            self.logger.error(f"❌ Error ejecutando Scrapy: {e}")
            return {
                'tool': 'scrapy',
                'items_target': item_limit,
                'error': str(e)
            }
    
    def generate_theoretical_comparison(self, scrapy_metrics: Dict) -> Dict:
        """Generar comparación teórica basada en características conocidas"""
        
        # Multiplicadores basados en características reales de cada herramienta
        multipliers = {
            'selenium': {
                'time': 3.5,  # Selenium es ~3.5x más lento
                'memory': 4.0,  # ~4x más memoria por el navegador
                'cpu': 2.8,  # Mayor uso de CPU
                'reliability': 0.85  # Menor tasa de éxito por timeouts
            },
            'playwright': {
                'time': 2.2,  # Playwright es ~2.2x más lento que Scrapy
                'memory': 2.5,  # ~2.5x más memoria
                'cpu': 2.0,  # Moderado uso de CPU
                'reliability': 0.92  # Buena tasa de éxito
            }
        }
        
        comparison = {
            'scrapy_actual': scrapy_metrics,
            'theoretical_comparison': {}
        }
        
        for tool, mult in multipliers.items():
            comparison['theoretical_comparison'][tool] = {
                'tool': tool,
                'items_target': scrapy_metrics.get('items_target', 0),
                'estimated_items_scraped': int(scrapy_metrics.get('items_scraped', 0) * mult['reliability']),
                'estimated_execution_time': round(scrapy_metrics.get('execution_time_seconds', 0) * mult['time'], 2),
                'estimated_memory_mb': round(scrapy_metrics.get('memory_used_mb', 0) * mult['memory'], 2),
                'estimated_items_per_second': round(scrapy_metrics.get('items_per_second', 0) / mult['time'], 2),
                'estimated_success_rate': round(scrapy_metrics.get('success_rate', 0) * mult['reliability'], 2),
                'characteristics': self._get_tool_characteristics(tool)
            }
        
        return comparison
    
    def _get_tool_characteristics(self, tool: str) -> Dict:
        """Obtener características técnicas de cada herramienta"""
        characteristics = {
            'scrapy': {
                'architecture': 'HTTP requests + lxml parsing',
                'javascript_support': 'No',
                'concurrency': 'Asyncio (nativo)',
                'resource_usage': 'Muy bajo',
                'anti_detection': 'Básico (headers, proxies)',
                'learning_curve': 'Media',
                'best_for': 'Sitios estáticos, alto volumen'
            },
            'selenium': {
                'architecture': 'Real browser automation',
                'javascript_support': 'Completo',
                'concurrency': 'Threading/multiprocessing',
                'resource_usage': 'Alto',
                'anti_detection': 'Bueno (real browser)',
                'learning_curve': 'Fácil',
                'best_for': 'JS pesado, interacciones complejas'
            },
            'playwright': {
                'architecture': 'Modern browser automation',
                'javascript_support': 'Completo',
                'concurrency': 'Asyncio (nativo)',
                'resource_usage': 'Medio',
                'anti_detection': 'Excelente (stealth)',
                'learning_curve': 'Media',
                'best_for': 'JS moderno, SPAs, anti-bot avanzado'
            }
        }
        
        return characteristics.get(tool, {})
    
    def run_complete_benchmark(self) -> Dict:
        """Ejecutar benchmark completo con múltiples tamaños"""
        self.logger.info("🔬 INICIANDO BENCHMARK COMPLETO")
        self.logger.info("=" * 50)
        
        test_sizes = [10, 25, 50]
        results = {
            'timestamp': datetime.now().isoformat(),
            'system_info': {
                'platform': sys.platform,
                'python_version': sys.version,
                'total_memory_gb': round(psutil.virtual_memory().total / 1024 / 1024 / 1024, 2),
                'cpu_count': psutil.cpu_count()
            },
            'tests': []
        }
        
        for size in test_sizes:
            self.logger.info(f"\n📊 Test con {size} items")
            scrapy_result = self.run_scrapy_test(size)
            comparison = self.generate_theoretical_comparison(scrapy_result)
            
            results['tests'].append({
                'test_size': size,
                'results': comparison
            })
        
        # Guardar resultados
        output_file = f'benchmark_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        self.logger.info(f"📝 Resultados guardados en: {output_file}")
        
        # Generar resumen
        self._generate_summary(results)
        
        return results
    
    def _generate_summary(self, results: Dict):
        """Generar resumen de resultados"""
        self.logger.info("\n" + "=" * 60)
        self.logger.info("📊 RESUMEN DE BENCHMARK")
        self.logger.info("=" * 60)
        
        for test in results['tests']:
            size = test['test_size']
            scrapy = test['results']['scrapy_actual']
            
            self.logger.info(f"\n🎯 Test con {size} items:")
            self.logger.info(f"   Scrapy: {scrapy.get('items_scraped', 0)} items en {scrapy.get('execution_time_seconds', 0)}s")
            self.logger.info(f"   Memoria: {scrapy.get('memory_used_mb', 0):.1f}MB")
            self.logger.info(f"   Velocidad: {scrapy.get('items_per_second', 0):.1f} items/s")
            
            # Comparación teórica
            for tool_name, metrics in test['results']['theoretical_comparison'].items():
                self.logger.info(f"   {tool_name.title()} (estimado): {metrics['estimated_execution_time']}s, {metrics['estimated_memory_mb']:.1f}MB")


if __name__ == '__main__':
    benchmark = ScrapyBenchmark()
    results = benchmark.run_complete_benchmark()
    
    print("\n🎉 Benchmark completado. Revisa los archivos de log y JSON para más detalles.")
