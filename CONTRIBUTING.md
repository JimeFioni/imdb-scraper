# 🤝 CONTRIBUTING - Guía de Contribución

## 🎉 ¡Gracias por tu interés en contribuir!

Este proyecto es un **análisis técnico comparativo profesional** de herramientas de web scraping (Scrapy vs Selenium vs Playwright) aplicado a IMDb. Valoramos todas las contribuciones que ayuden a mejorar el proyecto.

---

## 🚀 INICIO RÁPIDO

### 1️⃣ **Fork y Configuración**
```bash
# Fork en GitHub, luego:
git clone https://github.com/[TU-USERNAME]/imdb_scraper.git
cd imdb_scraper

# Configurar upstream
git remote add upstream https://github.com/JimeFioni/imdb_scraper.git

# Instalar dependencias
./setup.sh
source venv/bin/activate
```

### 2️⃣ **Ejecutar Demo**
```bash
# Verificar que todo funcione
./demo_completo_colaboradores.sh
```

### 3️⃣ **Elegir una Tarea**
Ve a [Issues](https://github.com/JimeFioni/imdb_scraper/issues) y elige una tarea con:
- 🟢 `good-first-issue` para principiantes
- 🟡 `help-wanted` para contribuciones intermedias
- 🔴 `enhancement` para nuevas características

---

## 📋 TIPOS DE CONTRIBUCIONES

### 🐛 **Bug Reports**
- Usa el template de bug report
- Incluye pasos para reproducir
- Especifica tu entorno (OS, Python version, etc.)
- Adjunta logs si es posible

### 💡 **Feature Requests**
- Describe el problema que resuelve
- Propón una solución específica
- Considera el impacto en el rendimiento
- Mantén coherencia con el objetivo del proyecto

### 📝 **Documentación**
- Corrige errores tipográficos
- Mejora explicaciones
- Añade ejemplos
- Traduce contenido
- Crea tutoriales

### 🧪 **Tests**
- Añade tests para nuevo código
- Mejora coverage existente
- Tests de integración
- Benchmarks de rendimiento

### 🔧 **Código**
- Sigue las convenciones existentes
- Incluye tests
- Actualiza documentación
- Optimiza rendimiento cuando sea posible

---

## 🛠️ WORKFLOW DE DESARROLLO

### 1️⃣ **Crear Branch**
```bash
# Sincronizar con upstream
git fetch upstream
git checkout main
git merge upstream/main

# Crear nueva rama
git checkout -b feature/nombre-descriptivo
# o
git checkout -b fix/nombre-del-bug
```

### 2️⃣ **Hacer Cambios**
```bash
# Realizar cambios
# Ejecutar tests
python -m pytest tests/

# Verificar scraper
scrapy crawl top_movies -s CLOSESPIDER_ITEMCOUNT=3
```

### 3️⃣ **Commit**
```bash
git add .
git commit -m "tipo: descripción clara

- Detalle 1
- Detalle 2

Fixes #123"
```

**Tipos de commit:**
- `feat:` nueva funcionalidad
- `fix:` corrección de bug
- `docs:` cambios en documentación
- `style:` formato, sin cambios de lógica
- `refactor:` refactoring de código
- `test:` añadir o modificar tests
- `perf:` mejora de rendimiento

### 4️⃣ **Pull Request**
```bash
git push origin feature/nombre-descriptivo
```

Luego crea PR en GitHub con:
- Título descriptivo
- Descripción detallada
- Referencias a issues relacionados
- Screenshots si aplica

---

## 📏 ESTÁNDARES DE CÓDIGO

### 🐍 **Python Style**
```python
# Seguir PEP 8
# Usar type hints cuando sea posible
def extract_movie_data(response: scrapy.Response) -> Dict[str, Any]:
    """Extract movie information from IMDb page.
    
    Args:
        response: Scrapy response object
        
    Returns:
        Dictionary with movie data
    """
    pass

# Constantes en MAYÚSCULAS
DEFAULT_DELAY = 1
MAX_RETRIES = 3

# Documentar funciones complejas
class ProxyRotator:
    """Manages proxy rotation for web scraping."""
    pass
```

### 📁 **Estructura de Archivos**
```
nueva_funcionalidad/
├── __init__.py
├── main_module.py          # Lógica principal
├── utils.py               # Utilidades
├── tests/
│   ├── __init__.py
│   ├── test_main_module.py
│   └── test_utils.py
└── README.md              # Documentación específica
```

### 🧪 **Tests**
```python
import pytest
from imdb_scraper.new_module import NewClass

class TestNewClass:
    def setup_method(self):
        self.instance = NewClass()
    
    def test_functionality(self):
        result = self.instance.method()
        assert result == expected_value
    
    def test_error_handling(self):
        with pytest.raises(ValueError):
            self.instance.method_with_error()
```

---

## 🎯 ÁREAS DE CONTRIBUCIÓN PRIORITARIAS

### 🔬 **Análisis Técnico**
- Ampliar comparaciones con otras herramientas
- Nuevos benchmarks y métricas
- Análisis de diferentes tipos de sitios web
- Estudios de rendimiento en diferentes condiciones

### 🛡️ **Sistema de Proxies**
- Nuevos proveedores de proxies
- Algoritmos de rotación mejorados
- Detección automática de proxies bloqueados
- Integración con servicios de VPN

### 📊 **Análisis de Datos**
- Nuevas consultas SQL analíticas
- Visualizaciones de datos
- Reportes automatizados
- Integración con herramientas de BI

### 🚀 **Escalabilidad**
- Paralelización mejorada
- Distribución de carga
- Caching inteligente
- Optimización de memoria

---

## ✅ CHECKLIST ANTES DEL PR

### 🧪 **Testing**
- [ ] Tests pasan localmente
- [ ] Nuevo código tiene tests
- [ ] Coverage no disminuye
- [ ] Scraper funciona con cambios

### 📝 **Documentación**
- [ ] README actualizado si es necesario
- [ ] Docstrings añadidos/actualizados
- [ ] CHANGELOG.md actualizado
- [ ] Comentarios en código complejo

### 🔧 **Código**
- [ ] Sigue convenciones del proyecto
- [ ] No hay código comentado
- [ ] No hay prints de debug
- [ ] Variables tienen nombres descriptivos

### 📊 **Rendimiento**
- [ ] No introduce regresiones de rendimiento
- [ ] Considera uso de memoria
- [ ] Optimiza consultas SQL si aplica

---

## 🚫 QUÉ NO HACER

### ❌ **Cambios No Deseados**
- No cambiar la arquitectura core sin discusión previa
- No añadir dependencias pesadas innecesariamente
- No modificar configuración de proxies sin justificación
- No cambiar el objetivo principal del proyecto

### ❌ **Código Problemático**
- No hacer commits directos a main
- No incluir archivos personales (.env, .vscode/settings.json)
- No hardcodear valores sensibles
- No ignorar warnings de seguridad

### ❌ **Documentación**
- No eliminar documentación existente sin reemplazar
- No usar lenguaje técnico sin explicar
- No dejar enlaces rotos

---

## 🎖️ RECONOCIMIENTOS

### 🌟 **Niveles de Contribución**
- **⭐ Contributor**: Primera contribución aceptada
- **🌟 Active Contributor**: 5+ contribuciones
- **💫 Core Contributor**: 15+ contribuciones + mentoring
- **🏆 Maintainer**: Responsabilidad del proyecto

### 🏅 **Hall of Fame**
Los mejores contribuidores serán reconocidos en:
- README principal
- Sección especial en docs
- Menciones en redes sociales
- Recomendaciones en LinkedIn

---

## 💬 COMUNICACIÓN

### 📞 **Canales**
- 🐛 **Issues**: Bugs, features, preguntas
- 💬 **Discussions**: Ideas, propuestas, ayuda
- 📧 **Email**: jimenafioni@gmail.com (temas urgentes)
- 📝 **PR Comments**: Review de código

### ⏰ **Tiempo de Respuesta**
- Issues: 24-48 horas
- PRs: 2-3 días
- Emails: 1-2 días

### 🌍 **Idiomas**
- Español (principal)
- English (aceptado)
- Português (básico)

---

## 📖 RECURSOS ÚTILES

### 📚 **Documentación del Proyecto**
- [`README.md`](README.md) - Documentación principal
- [`COLABORADORES_BIENVENIDA.md`](COLABORADORES_BIENVENIDA.md) - Guía para nuevos
- [`docs/IMDB_TECHNICAL_COMPARISON.md`](docs/IMDB_TECHNICAL_COMPARISON.md) - Análisis técnico

### 🛠️ **Herramientas Externas**
- [Scrapy Documentation](https://docs.scrapy.org/)
- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [Playwright Documentation](https://playwright.dev/python/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

### 🎓 **Aprendizaje**
- [Web Scraping Best Practices](https://blog.apify.com/web-scraping-best-practices/)
- [Python Style Guide](https://pep8.org/)
- [Git Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)

---

## ❓ PREGUNTAS FRECUENTES

### Q: **¿Puedo trabajar en múltiples issues a la vez?**
A: Preferimos que se enfoquen en uno a la vez para evitar conflictos.

### Q: **¿Qué pasa si mi PR no es aceptado?**
A: Proporcionaremos feedback constructivo. Raramente rechazamos sin oportunidad de mejora.

### Q: **¿Puedo añadir nuevas dependencias?**
A: Sí, pero justifica por qué es necesaria y considera el impacto en el tamaño del proyecto.

### Q: **¿Cómo reporto un problema de seguridad?**
A: Envía un email privado a jimenafioni@gmail.com en lugar de crear un issue público.

---

## 🎉 ¡GRACIAS POR CONTRIBUIR!

Cada contribución, grande o pequeña, hace que este proyecto sea mejor. ¡Esperamos trabajar contigo!

---

**🤝 Happy Contributing!**  
**Mantenido por:** [@JimeFioni](https://github.com/JimeFioni)  
**Última actualización:** 29 de julio de 2025
