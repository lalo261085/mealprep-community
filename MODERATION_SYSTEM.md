# 🤖 Sistema de Moderación Automática - MealPrep Community

## 📋 Resumen

Se ha implementado un sistema completo de moderación automática para el repositorio de comunidad de MealPrep que incluye:

- ✅ **GitHub Actions** para moderación automática
- ✅ **Script de moderación** avanzado en Python
- ✅ **Templates de issues** para moderación manual
- ✅ **Sistema de validación** integrado
- ✅ **Pruebas automatizadas** del sistema

## 🏗️ Arquitectura del Sistema

### 1. GitHub Actions Workflow
**Archivo**: `.github/workflows/moderate-recipes.yml`

**Funcionalidades**:
- Se ejecuta automáticamente en cada push/PR
- Valida archivos JSON
- Ejecuta moderación automática
- Verifica estructura de recetas
- Detecta contenido inapropiado
- Actualiza metadatos automáticamente
- Genera reportes de moderación

### 2. Script de Moderación
**Archivo**: `scripts/moderate_recipes.py`

**Características**:
- Validación de campos obligatorios
- Verificación de contenido inapropiado
- Validación de nombres y categorías
- Sistema de puntuación de calidad (0-100)
- Detección de ingredientes problemáticos
- Generación de reportes detallados

### 3. Templates de Issues
**Archivos**: 
- `.github/ISSUE_TEMPLATE/recipe-moderation.yml`
- `.github/ISSUE_TEMPLATE/feature-request.yml`

**Funcionalidades**:
- Formularios estructurados para reportar problemas
- Categorización automática de issues
- Campos obligatorios y opcionales
- Confirmaciones de usuario

## 🔍 Criterios de Moderación

### ✅ Validaciones Automáticas

1. **Estructura de Datos**:
   - Campos obligatorios presentes (`name`, `servings`, `category`, `ingredients`)
   - Tipos de datos correctos
   - JSON válido

2. **Contenido Apropiado**:
   - Sin palabras inapropiadas
   - Nombres de recetas válidos (3-100 caracteres)
   - Categorías apropiadas (2-50 caracteres)

3. **Ingredientes**:
   - Al menos un ingrediente
   - Cada ingrediente debe tener nombre
   - Máximo 50 ingredientes por receta

4. **Calidad**:
   - Puntuación mínima basada en completitud
   - Bonificaciones por detalles adicionales

### ⚠️ Advertencias (No Bloquean Aprobación)

- Número de porciones muy alto (>100)
- Notas muy largas (>500 caracteres)
- Muchos ingredientes (>50)

### ❌ Problemas Críticos (Bloquean Aprobación)

- Campos obligatorios faltantes
- Contenido inapropiado
- Nombres muy cortos o muy largos
- Ingredientes sin nombre
- Servings inválidos

## 📊 Sistema de Puntuación

**Puntuación Base**: 100 puntos

**Penalizaciones**:
- Issues críticos: -20 puntos cada uno
- Warnings: -5 puntos cada uno

**Bonificaciones**:
- Notas presentes: +5 puntos
- 3+ ingredientes: +5 puntos
- Categoría específica: +5 puntos

**Rangos**:
- 90-100: Excelente
- 80-89: Bueno
- 70-79: Aceptable
- 60-69: Regular
- 0-59: Pobre

## 🚀 Cómo Usar el Sistema

### Para Desarrolladores

1. **Configurar Repositorio**:
   ```bash
   python3 scripts/setup_community_repo.py
   ```

2. **Probar Moderación**:
   ```bash
   python3 scripts/test_moderation.py
   ```

3. **Moderar Recetas Manualmente**:
   ```bash
   python3 scripts/moderate_recipes.py [directorio]
   ```

### Para Usuarios de la App

1. **Compartir Receta**:
   - La app valida automáticamente antes de subir
   - Muestra puntuación de calidad
   - Informa sobre warnings

2. **Sincronizar**:
   - La app descarga recetas moderadas
   - Actualiza metadatos automáticamente

## 📈 Métricas y Reportes

### Estadísticas Generadas
- Total de recetas
- Recetas aprobadas/rechazadas
- Tasa de aprobación
- Puntuación promedio
- Issues más comunes
- Categorías disponibles
- Contribuidores

### Reportes Automáticos
- Resumen en GitHub Actions
- Archivo `moderation_report.txt`
- Metadatos en `metadata.json`

## 🔧 Configuración Avanzada

### Personalizar Palabras Inapropiadas
Editar `scripts/moderate_recipes.py`:
```python
self.inappropriate_words = [
    "spam", "xxx", "adult", "nsfw", "hate", "violence", 
    "illegal", "fake", "scam", "phishing", "malware"
]
```

### Ajustar Criterios de Validación
Modificar límites en `scripts/moderate_recipes.py`:
```python
# Límites configurables
MIN_NAME_LENGTH = 3
MAX_NAME_LENGTH = 100
MIN_CATEGORY_LENGTH = 2
MAX_CATEGORY_LENGTH = 50
MAX_INGREDIENTS = 50
MAX_NOTES_LENGTH = 500
```

### Personalizar Puntuación
Ajustar bonificaciones y penalizaciones:
```python
# En _calculate_quality_score()
score -= len(issues) * 20      # Penalización por issues
score -= len(warnings) * 5     # Penalización por warnings
score += 5 if recipe.get('notes') else 0  # Bonificación por notas
```

## 🛠️ Mantenimiento

### Monitoreo
- Revisar reportes de GitHub Actions
- Monitorear issues de moderación
- Actualizar lista de palabras inapropiadas

### Actualizaciones
- Mejorar criterios de validación
- Añadir nuevas validaciones
- Optimizar rendimiento

### Resolución de Problemas
- Revisar logs de GitHub Actions
- Ejecutar pruebas locales
- Verificar configuración de Git

## 📚 Archivos del Sistema

```
.github/
├── workflows/
│   └── moderate-recipes.yml    # GitHub Actions workflow
└── ISSUE_TEMPLATE/
    ├── recipe-moderation.yml   # Template para reportar recetas
    └── feature-request.yml     # Template para solicitar funcionalidades

scripts/
├── moderate_recipes.py         # Script principal de moderación
├── test_moderation.py          # Pruebas del sistema
└── setup_community_repo.py     # Configuración inicial

recipes/                        # Directorio de recetas (se crea automáticamente)
├── recipe_1.json
├── recipe_2.json
└── ...

metadata.json                   # Metadatos del repositorio
moderation_report.txt           # Reporte de moderación (se genera automáticamente)
README_COMMUNITY.md             # Documentación para usuarios
```

## ✅ Estado del Sistema

- **GitHub Actions**: ✅ Configurado y funcionando
- **Script de Moderación**: ✅ Implementado y probado
- **Templates de Issues**: ✅ Creados y configurados
- **Sistema de Validación**: ✅ Funcionando correctamente
- **Pruebas Automatizadas**: ✅ Todas las pruebas pasan
- **Documentación**: ✅ Completa y actualizada

## 🎯 Próximos Pasos

1. **Configurar repositorio remoto** en GitHub
2. **Hacer push** del contenido inicial
3. **Configurar GitHub Actions** en el repositorio
4. **Integrar con la aplicación** MealPrep
5. **Monitorear** el funcionamiento del sistema

---

**¡El sistema de moderación automática está listo para usar! 🚀**