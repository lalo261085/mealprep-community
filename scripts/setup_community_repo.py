#!/usr/bin/env python3
"""
Script para configurar el repositorio de comunidad
Crea la estructura inicial y archivos de configuración
"""

import os
import json
import subprocess
from datetime import datetime

def create_repo_structure():
    """Crear la estructura inicial del repositorio"""
    
    print("🏗️  Creando estructura del repositorio...")
    
    # Directorios necesarios
    directories = [
        "recipes",
        ".github/workflows",
        ".github/ISSUE_TEMPLATE",
        "scripts"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Creado directorio: {directory}")
    
    # Crear archivo .gitignore
    gitignore_content = """# Archivos de moderación
moderation_report.txt

# Archivos temporales
*.tmp
*.temp

# Logs
*.log

# Archivos de sistema
.DS_Store
Thumbs.db

# Archivos de Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/

# Archivos de IDE
.vscode/
.idea/
*.swp
*.swo

# Archivos de prueba
test_recipes/
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    print("✅ Creado .gitignore")

def create_initial_metadata():
    """Crear archivo de metadatos inicial"""
    
    print("📊 Creando metadatos iniciales...")
    
    metadata = {
        "last_sync": datetime.now().isoformat(),
        "total_recipes": 0,
        "categories": [],
        "contributors": [],
        "moderation_status": "ready",
        "last_moderation": datetime.now().isoformat(),
        "repository_info": {
            "name": "mealprep-community",
            "description": "Recetas compartidas por la comunidad MealPrep",
            "version": "1.0.0",
            "created_at": datetime.now().isoformat()
        }
    }
    
    with open("metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print("✅ Creado metadata.json")

def create_sample_recipes():
    """Crear recetas de ejemplo para demostración"""
    
    print("🍽️  Creando recetas de ejemplo...")
    
    sample_recipes = [
        {
            "id": "sample_1",
            "name": "Paella Valenciana",
            "servings": 4,
            "category": "Arroces",
            "notes": "Receta tradicional valenciana con arroz bomba",
            "ingredients": [
                {"name": "Arroz bomba", "quantity": 400, "unit": "g"},
                {"name": "Pollo", "quantity": 300, "unit": "g"},
                {"name": "Conejo", "quantity": 200, "unit": "g"},
                {"name": "Judías verdes", "quantity": 150, "unit": "g"},
                {"name": "Azafrán", "quantity": 1, "unit": "pizca"},
                {"name": "Aceite de oliva", "quantity": 4, "unit": "cucharadas"},
                {"name": "Sal", "quantity": 1, "unit": "cucharadita"}
            ],
            "shared_by": "Comunidad MealPrep",
            "shared_at": datetime.now().isoformat(),
            "version": "1.0",
            "moderation_status": "approved",
            "quality_score": 95
        },
        {
            "id": "sample_2",
            "name": "Ensalada César",
            "servings": 2,
            "category": "Ensaladas",
            "notes": "Clásica ensalada César con pollo a la plancha",
            "ingredients": [
                {"name": "Lechuga romana", "quantity": 1, "unit": "cabeza"},
                {"name": "Pollo a la plancha", "quantity": 200, "unit": "g"},
                {"name": "Parmesano rallado", "quantity": 50, "unit": "g"},
                {"name": "Crutones", "quantity": 100, "unit": "g"},
                {"name": "Salsa César", "quantity": 3, "unit": "cucharadas"},
                {"name": "Aceite de oliva", "quantity": 2, "unit": "cucharadas"},
                {"name": "Limón", "quantity": 1, "unit": "unidad"}
            ],
            "shared_by": "Comunidad MealPrep",
            "shared_at": datetime.now().isoformat(),
            "version": "1.0",
            "moderation_status": "approved",
            "quality_score": 90
        },
        {
            "id": "sample_3",
            "name": "Risotto de Hongos",
            "servings": 3,
            "category": "Arroces",
            "notes": "Cremoso risotto con hongos porcini",
            "ingredients": [
                {"name": "Arroz arborio", "quantity": 300, "unit": "g"},
                {"name": "Hongos porcini", "quantity": 200, "unit": "g"},
                {"name": "Vino blanco", "quantity": 100, "unit": "ml"},
                {"name": "Parmesano", "quantity": 80, "unit": "g"},
                {"name": "Caldo de verduras", "quantity": 500, "unit": "ml"},
                {"name": "Cebolla", "quantity": 1, "unit": "unidad"},
                {"name": "Ajo", "quantity": 2, "unit": "dientes"},
                {"name": "Mantequilla", "quantity": 30, "unit": "g"}
            ],
            "shared_by": "Comunidad MealPrep",
            "shared_at": datetime.now().isoformat(),
            "version": "1.0",
            "moderation_status": "approved",
            "quality_score": 92
        }
    ]
    
    for recipe in sample_recipes:
        filename = f"recipes/{recipe['id']}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(recipe, f, indent=2, ensure_ascii=False)
        print(f"✅ Creada receta: {recipe['name']}")
    
    return sample_recipes

def update_metadata_with_samples(sample_recipes):
    """Actualizar metadatos con las recetas de ejemplo"""
    
    print("📊 Actualizando metadatos con recetas de ejemplo...")
    
    categories = set()
    contributors = set()
    
    for recipe in sample_recipes:
        categories.add(recipe["category"])
        contributors.add(recipe["shared_by"])
    
    metadata = {
        "last_sync": datetime.now().isoformat(),
        "total_recipes": len(sample_recipes),
        "categories": sorted(list(categories)),
        "contributors": sorted(list(contributors)),
        "moderation_status": "ready",
        "last_moderation": datetime.now().isoformat(),
        "repository_info": {
            "name": "mealprep-community",
            "description": "Recetas compartidas por la comunidad MealPrep",
            "version": "1.0.0",
            "created_at": datetime.now().isoformat()
        }
    }
    
    with open("metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print("✅ Metadatos actualizados")

def create_github_workflow():
    """Crear el workflow de GitHub Actions si no existe"""
    
    workflow_file = ".github/workflows/moderate-recipes.yml"
    
    if not os.path.exists(workflow_file):
        print("⚠️  Workflow de GitHub Actions no encontrado")
        print("   Asegúrate de que el archivo .github/workflows/moderate-recipes.yml existe")
    else:
        print("✅ Workflow de GitHub Actions encontrado")

def create_issue_templates():
    """Verificar que los templates de issues existen"""
    
    templates = [
        ".github/ISSUE_TEMPLATE/recipe-moderation.yml",
        ".github/ISSUE_TEMPLATE/feature-request.yml"
    ]
    
    for template in templates:
        if os.path.exists(template):
            print(f"✅ Template encontrado: {template}")
        else:
            print(f"⚠️  Template no encontrado: {template}")

def test_git_setup():
    """Verificar configuración de Git"""
    
    print("🔧 Verificando configuración de Git...")
    
    try:
        # Verificar si es un repositorio Git
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Repositorio Git configurado")
        else:
            print("⚠️  No es un repositorio Git. Ejecuta: git init")
            return False
    except FileNotFoundError:
        print("❌ Git no está instalado")
        return False
    
    return True

def main():
    """Función principal"""
    
    print("🚀 CONFIGURANDO REPOSITORIO DE COMUNIDAD MEALPREP")
    print("=" * 60)
    
    try:
        # Crear estructura
        create_repo_structure()
        
        # Crear metadatos iniciales
        create_initial_metadata()
        
        # Crear recetas de ejemplo
        sample_recipes = create_sample_recipes()
        
        # Actualizar metadatos
        update_metadata_with_samples(sample_recipes)
        
        # Verificar configuración
        create_github_workflow()
        create_issue_templates()
        
        # Verificar Git
        git_ok = test_git_setup()
        
        print("\n🎉 CONFIGURACIÓN COMPLETADA")
        print("=" * 60)
        print("✅ Estructura del repositorio creada")
        print("✅ Metadatos iniciales configurados")
        print(f"✅ {len(sample_recipes)} recetas de ejemplo creadas")
        print("✅ Templates de issues configurados")
        
        if git_ok:
            print("✅ Repositorio Git configurado")
        else:
            print("⚠️  Configuración de Git pendiente")
        
        print("\n📋 PRÓXIMOS PASOS:")
        print("1. Configura el repositorio remoto en GitHub")
        print("2. Haz push del contenido inicial")
        print("3. Configura GitHub Actions")
        print("4. Prueba el sistema de moderación")
        
        print("\n🧪 Para probar el sistema:")
        print("   python scripts/test_moderation.py")
        
    except Exception as e:
        print(f"\n💥 ERROR DURANTE LA CONFIGURACIÓN: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)