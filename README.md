# Recetario con Sistema de Votación (MealPrep Community)

Este repositorio ahora incluye un **sistema de votación centralizado** inspirado en `MealPrep_v2.0_mac`.

## ¿Qué se agregó?
- `.github/scripts/vote_tracker.py`: lógica de tracking de votos por `build_id` (evita duplicados).
- `.github/scripts/intake.py`: procesa issues para compartir recetas (`share:`) y votar (`vote:`).
- `.github/scripts/vote_stats.py`: genera estadísticas de votos.
- `.github/scripts/migrate_vote_data.py`: inicializa y migra datos si fuera necesario.
- `.github/workflows/community.yml`: workflow que procesa issues abiertos.
- `.github/workflows/vote-stats.yml`: reporte semanal de estadísticas.
- `.github/VOTE_SYSTEM.md`: documentación del sistema.
- `.github/data/vote_config.json`: configuración del sistema de votos.

## Cómo probar localmente
```bash
python3 .github/scripts/test_vote_system.py
python3 .github/scripts/vote_stats.py stats
```

## Cómo usar con GitHub Issues
- Abrí un issue con label `vote` y en el cuerpo pegá un bloque JSON con la receta y tu `build_id`:

```json
{
  "id": "bud-n-de-banana",
  "build_id": "your-build-id-123"
}
```

- Para compartir receta, usá label `recipe` o título `share:` con bloque JSON del contenido.

El workflow `Community intake` procesará el issue, actualizará `recipes_index.json`, recetas y `.github/data/vote_tracker.json`, y hará commit/push automático.
