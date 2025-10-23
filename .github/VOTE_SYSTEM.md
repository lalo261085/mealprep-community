# 🗳️ Sistema de Votación MealPrep Community

## Descripción General

Este sistema previene votos duplicados utilizando un **Build ID único** generado por cada instalación de la aplicación MealPrep. Cada vez que un usuario vota por una receta, el sistema verifica si ese Build ID ya votó por esa receta específica.

## 🔧 Componentes del Sistema

### 1. **Cliente (Aplicación MealPrep)**
- Genera un Build ID único por instalación
- Incluye el Build ID en todos los payloads de votos
- Almacena el Build ID en `config.json` para persistencia

### 2. **Servidor (GitHub Actions)**
- Procesa issues de votos con Build ID
- Verifica duplicados usando el sistema de tracking
- Actualiza contadores de likes solo para votos únicos

### 3. **Sistema de Tracking**
- Archivo: `.github/data/vote_tracker.json`
- Almacena qué Build IDs votaron por qué recetas
- Incluye timestamps y estadísticas

## 📊 Estructura de Datos

### Payload de Voto
```json
{
  "id": "recipe-123",
  "name": "Pasta Carbonara",
  "path": "recipes/pasta-carbonara.json",
  "build_id": "2eb078b9acca6f9f"
}
```

### Vote Tracker
```json
{
  "2eb078b9acca6f9f": {
    "first_vote_at": "2024-01-15T10:30:00Z",
    "last_vote_at": "2024-01-20T14:22:00Z",
    "voted_recipes": ["recipe-123", "recipe-456"],
    "total_votes": 2
  }
}
```

## 🚫 Prevención de Duplicados

### Nivel 1: Cliente
- La app verifica localmente si ya votó por esa receta
- Evita envíos innecesarios a GitHub

### Nivel 2: Servidor
- GitHub verifica si el Build ID ya votó por esa receta
- Rechaza votos duplicados automáticamente
- Procesa solo votos únicos

## 📈 Estadísticas Disponibles

### Comandos de Estadísticas
```bash
# Ver estadísticas completas
python .github/scripts/vote_stats.py stats

# Limpiar datos antiguos (90+ días)
python .github/scripts/vote_stats.py cleanup

# Análisis de duplicados
python .github/scripts/vote_stats.py duplicates
```

### Métricas Incluidas
- Total de instalaciones únicas (Build IDs)
- Total de votos emitidos
- Promedio de votos por instalación
- Top votantes
- Top recetas por likes
- Actividad reciente

## 🔄 Flujo de Votación

1. **Usuario vota** en la aplicación MealPrep
2. **App verifica** localmente si ya votó
3. **App envía** payload con Build ID a GitHub
4. **GitHub verifica** si ese Build ID ya votó por esa receta
5. **Si es duplicado** → Rechaza el voto
6. **Si es único** → Procesa y actualiza contador de likes
7. **Sistema registra** el voto en el tracker

## 🛠️ Mantenimiento

### Limpieza Automática
- Se ejecuta automáticamente cada 10 votos
- Elimina registros de votos de más de 90 días
- Mantiene el sistema eficiente

### Reportes Semanales
- Workflow automático cada domingo
- Genera issue con estadísticas semanales
- Incluye métricas de actividad

## 🔒 Seguridad

### Características del Build ID
- **Único por instalación**: Basado en características del sistema
- **Persistente**: Se mantiene entre sesiones de la app
- **No falsificable**: Usa hash SHA-256 de datos del sistema
- **Anónimo**: No contiene información personal

### Protecciones
- Validación de formato de Build ID
- Sanitización de datos de entrada
- Manejo seguro de errores
- Logs de auditoría

## 📝 Logs y Debugging

### Archivos de Log
- `.github/data/vote_tracker.json` - Datos de votos
- `data/community.log` - Logs de la aplicación
- Issues de GitHub - Historial de votos

### Información de Debug
- Build ID en cada voto
- Timestamps de votos
- Estadísticas de uso
- Detección de anomalías

## 🔧 Configuración

### Variables de Entorno
- `GITHUB_TOKEN` - Token para acceso a la API
- `VOTE_CLEANUP_DAYS` - Días para limpieza (default: 90)

### Archivos de Configuración
- `vote_tracker.py` - Lógica de tracking
- `intake.py` - Procesamiento de issues
- `vote_stats.py` - Estadísticas y reportes

---

*Este sistema garantiza la integridad de los votos mientras mantiene una experiencia de usuario fluida y transparente.*