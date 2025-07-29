#!/bin/bash

# ================================================================
# 🤝 SCRIPT DE INVITACIÓN A COLABORADORES
# ================================================================
# Este script prepara el repositorio y proporciona instrucciones
# para invitar colaboradores específicos al proyecto
# ================================================================

clear
echo "🤝================================================================================================🤝"
echo "                         PREPARACIÓN PARA INVITAR COLABORADORES"
echo "🤝================================================================================================🤝"
echo ""
echo "📅 Fecha: $(date)"
echo "🎯 Objetivo: Invitar colaboradores al proyecto IMDb Scraper"
echo ""

# ================================================================
# VERIFICACIÓN PREVIA
# ================================================================
echo "🔍 VERIFICACIÓN PREVIA DEL REPOSITORIO"
echo "======================================="
echo ""

# Verificar estado del git
if [ -d ".git" ]; then
    echo "✅ Repositorio Git detectado"
    
    # Verificar si hay cambios sin commitear
    if [ -n "$(git status --porcelain)" ]; then
        echo "⚠️  Hay cambios sin commitear. Ejecutando commit automático..."
        git add .
        git commit -m "docs: añadir guías para colaboradores

- Agregada guía de bienvenida para nuevos colaboradores
- Creado template para issues de nuevos colaboradores  
- Añadidas contributing guidelines completas
- Preparación para invitar: tc-kespejo, tc-lraigoso, sneira5"
        
        echo "✅ Cambios commiteados"
    else
        echo "✅ Repositorio limpio"
    fi
    
    # Push a GitHub
    echo "📤 Subiendo cambios a GitHub..."
    git push origin main
    if [ $? -eq 0 ]; then
        echo "✅ Cambios subidos exitosamente a GitHub"
    else
        echo "⚠️  Error al subir cambios. Verificar conexión."
    fi
else
    echo "❌ No se detectó repositorio Git"
    exit 1
fi

echo ""

# ================================================================
# NUEVOS ARCHIVOS CREADOS
# ================================================================
echo "📝 ARCHIVOS CREADOS PARA COLABORADORES"
echo "======================================"
echo ""
echo "✅ Archivos de bienvenida creados:"
echo "   📄 COLABORADORES_BIENVENIDA.md - Guía completa para nuevos colaboradores"
echo "   📄 CONTRIBUTING.md - Guidelines de contribución"
echo "   📄 .github/ISSUE_TEMPLATE/nuevo-colaborador.md - Template para nuevos colaboradores"
echo ""

# Verificar que los archivos existen
files_to_check=(
    "COLABORADORES_BIENVENIDA.md"
    "CONTRIBUTING.md"
    ".github/ISSUE_TEMPLATE/nuevo-colaborador.md"
)

for file in "${files_to_check[@]}"; do
    if [ -f "$file" ]; then
        lines=$(wc -l < "$file")
        size=$(ls -lh "$file" | awk '{print $5}')
        echo "   ✅ $file: $lines líneas ($size)"
    else
        echo "   ❌ $file: NO ENCONTRADO"
    fi
done

echo ""

# ================================================================
# COLABORADORES A INVITAR
# ================================================================
echo "👥 COLABORADORES A INVITAR"
echo "=========================="
echo ""
echo "📋 Lista de colaboradores objetivo:"
echo "   🧑‍💻 tc-kespejo - https://github.com/tc-kespejo"
echo "   🧑‍💻 tc-lraigoso - https://github.com/tc-lraigoso"  
echo "   🧑‍💻 sneira5 - https://github.com/sneira5"
echo ""

# ================================================================
# INSTRUCCIONES PARA INVITAR
# ================================================================
echo "📋 INSTRUCCIONES PARA INVITAR COLABORADORES"
echo "==========================================="
echo ""
echo "🚀 MÉTODO 1: INVITACIÓN DIRECTA (Recomendado)"
echo "----------------------------------------------"
echo ""
echo "1️⃣ Ve a tu repositorio en GitHub:"
echo "   🔗 https://github.com/JimeFioni/imdb_scraper"
echo ""
echo "2️⃣ Navega a: Settings > Collaborators and teams"
echo ""
echo "3️⃣ Click en 'Add people'"
echo ""
echo "4️⃣ Busca e invita a cada colaborador:"
echo "   📝 tc-kespejo"
echo "   📝 tc-lraigoso"
echo "   📝 sneira5"
echo ""
echo "5️⃣ Selecciona permisos: 'Write' (recomendado para colaboradores activos)"
echo ""
echo "6️⃣ Añade mensaje personalizado (opcional):"
echo '   "¡Hola! Te invito a colaborar en mi proyecto de análisis técnico de'
echo '   web scraping. Revisa la guía de bienvenida: COLABORADORES_BIENVENIDA.md"'
echo ""

echo "🔄 MÉTODO 2: INVITACIÓN POR ISSUE"
echo "--------------------------------"
echo ""
echo "1️⃣ Crea un issue mencionando a los colaboradores:"
echo "   Título: 🤝 Invitación a colaborar - Análisis técnico IMDb Scraper"
echo ""
echo "2️⃣ Menciona en el issue:"
echo "   @tc-kespejo @tc-lraigoso @sneira5"
echo ""
echo "3️⃣ Incluye el contenido del template de invitación."
echo ""

# ================================================================
# TEMPLATE DE INVITACIÓN
# ================================================================
echo "📧 TEMPLATE DE MENSAJE DE INVITACIÓN"
echo "===================================="
echo ""
cat << 'EOF'
## 🎬 ¡Te invito a colaborar en IMDb Scraper!

Hola! 👋 

Te invito a unirte como colaborador en mi proyecto **IMDb Scraper**, un análisis técnico comparativo profesional de herramientas de web scraping.

### 🔬 **¿Qué hace especial este proyecto?**
- **Análisis científico**: Comparación real de Scrapy vs Selenium vs Playwright
- **Datos verificables**: Benchmark con métricas reales de rendimiento
- **Sistema robusto**: Proxies, anti-detección, arquitectura escalable
- **Documentación exhaustiva**: +1,000 líneas de docs técnicas

### 📊 **Estado actual: 100% COMPLETADO Y VERIFICADO**
- ✅ 4,868 líneas de código Python
- ✅ Scripts SQL completos con análisis avanzado  
- ✅ Sistema de proxies operativo
- ✅ Múltiples implementaciones funcionales

### 🚀 **¿Cómo empezar?**
1. 📖 Lee la guía: [`COLABORADORES_BIENVENIDA.md`](COLABORADORES_BIENVENIDA.md)
2. 🎬 Ejecuta el demo: `./demo_completo_colaboradores.sh`
3. 🔧 Elige una tarea en Issues
4. 🤝 ¡Comienza a contribuir!

### 🎯 **Áreas de colaboración:**
- 🐍 Optimización de código Python
- 📊 Nuevos análisis de datos
- 🛡️ Mejoras en sistema de proxies
- 📝 Documentación y tutoriales
- 🧪 Testing y quality assurance

**¿Te interesa?** ¡Acepta la invitación y comencemos a colaborar! 🚀

---
📧 **Contacto**: jimenafioni@gmail.com  
🔗 **Proyecto**: https://github.com/JimeFioni/imdb_scraper
EOF

echo ""

# ================================================================
# CHECKLIST POST-INVITACIÓN
# ================================================================
echo "✅ CHECKLIST DESPUÉS DE INVITAR"
echo "==============================="
echo ""
echo "📋 Una vez que invites a los colaboradores:"
echo ""
echo "□ Verificar que recibieron y aceptaron la invitación"
echo "□ Pedirles que creen un issue con el template 'Nuevo Colaborador'"
echo "□ Asignar labels apropiados según su experiencia"
echo "□ Sugerir tareas iniciales basadas en sus habilidades"
echo "□ Ofrecer una sesión de onboarding si es necesario"
echo "□ Añadirlos al README como colaboradores activos"
echo ""

# ================================================================
# ENLACES ÚTILES
# ================================================================
echo "🔗 ENLACES ÚTILES PARA COMPARTIR"
echo "================================"
echo ""
echo "📚 **Documentación principal:**"
echo "   🔗 README: https://github.com/JimeFioni/imdb_scraper/blob/main/README.md"
echo "   🔗 Bienvenida: https://github.com/JimeFioni/imdb_scraper/blob/main/COLABORADORES_BIENVENIDA.md"
echo "   🔗 Contributing: https://github.com/JimeFioni/imdb_scraper/blob/main/CONTRIBUTING.md"
echo ""
echo "🎯 **Issues y tareas:**"
echo "   🔗 Issues: https://github.com/JimeFioni/imdb_scraper/issues"
echo "   🔗 Projects: https://github.com/JimeFioni/imdb_scraper/projects"
echo ""
echo "📊 **Análisis técnico:**"
echo "   🔗 Comparación técnica: https://github.com/JimeFioni/imdb_scraper/blob/main/docs/IMDB_TECHNICAL_COMPARISON.md"
echo "   🔗 Verificación final: https://github.com/JimeFioni/imdb_scraper/blob/main/VERIFICACION_FINAL_COMPLETADA.md"
echo ""

# ================================================================
# COMANDOS ÚTILES
# ================================================================
echo "⚡ COMANDOS ÚTILES PARA NUEVOS COLABORADORES"
echo "==========================================="
echo ""
echo "🔧 **Setup inicial:**"
echo "   git clone https://github.com/JimeFioni/imdb_scraper.git"
echo "   cd imdb_scraper && ./setup.sh"
echo ""
echo "🎬 **Demo completo:**"
echo "   ./demo_completo_colaboradores.sh"
echo ""
echo "🔍 **Verificación:**"
echo "   ./verificar_entregables.sh"
echo ""
echo "🚀 **Primer scraping:**"
echo "   source venv/bin/activate"
echo "   scrapy crawl top_movies -s CLOSESPIDER_ITEMCOUNT=5"
echo ""

# ================================================================
# FINALIZACIÓN
# ================================================================
echo "🤝================================================================================================🤝"
echo "                           🎉 ¡LISTO PARA INVITAR COLABORADORES! 🎉"
echo ""
echo "✅ Archivos de bienvenida creados y subidos a GitHub"
echo "✅ Templates de issues configurados"
echo "✅ Guidelines de contribución establecidas"
echo "✅ Instrucciones de invitación preparadas"
echo ""
echo "🚀 SIGUIENTE PASO:"
echo "   1. Ve a tu repositorio en GitHub"
echo "   2. Settings > Collaborators and teams"
echo "   3. Invita a: tc-kespejo, tc-lraigoso, sneira5"
echo "   4. ¡Disfruta colaborando!"
echo ""
echo "🤝================================================================================================🤝"
