# 🌍 Comunidad de Recetas - MealPrep

Este repositorio contiene recetas compartidas por la comunidad de usuarios de MealPrep.

## 📋 Cómo Funciona

### Para Compartir Recetas
1. **Usa la aplicación MealPrep** para crear tu receta
2. **Ve al tab "Comunidad"** en la aplicación
3. **Selecciona "Compartir Receta"** 
4. **La receta se validará automáticamente** antes de subirse
5. **GitHub Actions moderará** la receta para asegurar calidad

### Para Descargar Recetas
1. **Ve al tab "Comunidad"** en la aplicación
2. **Explora por categorías** o usa la búsqueda
3. **Haz clic en una receta** para ver detalles
4. **Importa la receta** a tu colección local

## 🔍 Moderación Automática

Todas las recetas pasan por un proceso de moderación automática que verifica:

- ✅ **Estructura válida**: Campos obligatorios presentes
- ✅ **Contenido apropiado**: Sin spam o contenido inapropiado
- ✅ **Nombres válidos**: Nombres de recetas e ingredientes apropiados
- ✅ **Formato correcto**: JSON válido y estructura consistente

## 📊 Estadísticas

- **Total de recetas**: Se actualiza automáticamente
- **Categorías disponibles**: Arroces, Ensaladas, Sopas, etc.
- **Contribuidores**: Lista de usuarios que han compartido recetas

## 🛠️ Estructura del Repositorio

```
recipes/           # Archivos JSON de recetas
├── recipe_1.json
├── recipe_2.json
└── ...

metadata.json      # Metadatos del repositorio
.github/
├── workflows/     # GitHub Actions para moderación
└── ISSUE_TEMPLATE/ # Templates para reportar problemas
```

## 📝 Formato de Recetas

Las recetas siguen este formato estándar:

```json
{
  "id": "recipe_1234567890",
  "name": "Paella Valenciana",
  "servings": 4,
  "category": "Arroces",
  "notes": "Receta tradicional valenciana",
  "ingredients": [
    {
      "name": "Arroz bomba",
      "quantity": 400,
      "unit": "g"
    }
  ],
  "shared_by": "usuario",
  "shared_at": "2024-01-15T10:30:00",
  "version": "1.0",
  "moderation_status": "approved",
  "quality_score": 95
}
```

## 🚨 Reportar Problemas

Si encuentras una receta problemática:

1. **Ve a "Issues"** en este repositorio
2. **Selecciona "Moderar Receta"**
3. **Completa el formulario** con detalles del problema
4. **Los moderadores revisarán** tu reporte

## 🤝 Contribuir

### Como Desarrollador
- Fork el repositorio
- Crea una rama para tu feature
- Implementa mejoras en la moderación
- Envía un Pull Request

### Como Moderador
- Revisa issues de moderación
- Aproba o rechaza Pull Requests
- Mantén la calidad del contenido

## 📈 Métricas de Calidad

El sistema de moderación automática calcula una puntuación de calidad (0-100) basada en:

- **Completitud**: Todos los campos obligatorios
- **Detalle**: Notas y descripciones completas
- **Variedad**: Múltiples ingredientes
- **Categorización**: Categoría apropiada

## 🔄 Sincronización

La aplicación se sincroniza automáticamente con este repositorio:

- **Cada vez que abres** el tab Comunidad
- **Cuando compartes** una nueva receta
- **Al hacer clic** en "Sincronizar"

## 📱 Compatibilidad

- **MealPrep Desktop**: Windows, macOS, Linux
- **Versión mínima**: 1.0.0
- **Idiomas soportados**: Español, Inglés, Francés, Italiano, Portugués

## 🆘 Soporte

Si tienes problemas:

1. **Revisa los Issues** existentes
2. **Crea un nuevo Issue** con detalles
3. **Usa las etiquetas** apropiadas
4. **Proporciona logs** si es necesario

---

**¡Gracias por ser parte de la comunidad MealPrep! 🍽️**