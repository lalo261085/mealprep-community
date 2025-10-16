# MealPrep Community Recipes

Este repositorio contiene las recetas compartidas por la comunidad de MealPrep.

## Cómo compartir una receta desde la app
- En la pestaña "Recetas", selecciona una receta y haz clic en "Compartir en comunidad".
- Se abrirá un issue en GitHub con la receta en formato JSON dentro de un bloque de código.
- Revisa el contenido y envía el issue.

Un workflow (acciones de GitHub) tomará ese issue, validará el JSON y agregará/actualizará la receta en `recipes/` y la entrada en `recipes_index.json`.

## Cómo votar una receta
- En la pestaña "Comunidad", selecciona la receta y pulsa "Votar".
- Se abrirá un issue de tipo voto. El workflow incrementará el contador de `likes`.

## Estructura del repo
- `recipes/` — Contiene archivos JSON con recetas detalladas (ingredientes, notas, etc.).
- `recipes_index.json` — Índice resumido de recetas (para listados rápidos en la app).
- `.github/workflows/community.yml` — Automatización para procesar issues de compartir/votar.

## Formato de archivos
Ejemplo de entrada del índice (`recipes_index.json`):
```json
{
  "recipes": [
    {"id": "tortilla", "name": "Tortilla", "author": "Ana", "likes": 0, "category": "Cena", "path": "recipes/tortilla.json"}
  ]
}
```

Ejemplo de receta en `recipes/tortilla.json`:
```json
{
  "ingredients": [
    {"name": "Huevo", "unit": "ud", "quantity": 3, "category": "Huevos", "notes": ""}
  ],
  "notes": "Clásica",
  "servings": 4,
  "category": "Cena"
}
```
