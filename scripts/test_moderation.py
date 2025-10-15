#!/usr/bin/env python3
"""
Script de prueba para el sistema de moderación
Crea recetas de ejemplo y las valida
"""

import json
import os
import sys
from datetime import datetime

# Agregar el directorio padre al path para importar el moderador
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.moderate_recipes import RecipeModerator

def create_test_recipes():
    """Crear recetas de prueba para validar el sistema"""
    
    # Crear directorio de pruebas
    test_dir = "test_recipes"
    os.makedirs(test_dir, exist_ok=True)
    
    # Receta válida
    valid_recipe = {
        "id": "demo_valid_1",
        "name": "Paella Valenciana",
        "servings": 4,
        "category": "Arroces",
        "notes": "Receta tradicional valenciana con arroz bomba",
        "ingredients": [
            {"name": "Arroz bomba", "quantity": 400, "unit": "g"},
            {"name": "Pollo", "quantity": 300, "unit": "g"},
            {"name": "Conejo", "quantity": 200, "unit": "g"},
            {"name": "Judías verdes", "quantity": 150, "unit": "g"},
            {"name": "Azafrán", "quantity": 1, "unit": "pizca"}
        ],
        "shared_by": "demo_user",
        "shared_at": datetime.now().isoformat(),
        "version": "1.0"
    }
    
    # Receta con problemas
    invalid_recipe = {
        "id": "demo_invalid_1",
        "name": "A",  # Nombre muy corto
        "servings": "invalid",  # Servings inválido
        "category": "",  # Categoría vacía
        "notes": "Recipe with spam content",  # Contiene "spam"
        "ingredients": [],  # Sin ingredientes
        "shared_by": "demo_user",
        "shared_at": datetime.now().isoformat(),
        "version": "1.0"
    }
    
    # Receta con warnings
    warning_recipe = {
        "id": "demo_warning_1",
        "name": "Ensalada César",
        "servings": 150,  # Muchas porciones
        "category": "Ensaladas",
        "notes": "A" * 600,  # Notas muy largas
        "ingredients": [
            {"name": "Lechuga romana", "quantity": 1, "unit": "cabeza"},
            {"name": "Pollo a la plancha", "quantity": 200, "unit": "g"}
        ],
        "shared_by": "demo_user",
        "shared_at": datetime.now().isoformat(),
        "version": "1.0"
    }
    
    # Receta con ingredientes problemáticos
    ingredient_issues_recipe = {
        "id": "demo_ingredient_1",
        "name": "Risotto de Hongos",
        "servings": 3,
        "category": "Arroces",
        "notes": "Cremoso y delicioso",
        "ingredients": [
            {"name": "", "quantity": 300, "unit": "g"},  # Ingrediente sin nombre
            {"name": "Hongos porcini", "quantity": 200, "unit": "g"},
            {"name": "Vino blanco", "quantity": 100, "unit": "ml"},
            {"name": "Parmesano", "quantity": 80, "unit": "g"}
        ],
        "shared_by": "demo_user",
        "shared_at": datetime.now().isoformat(),
        "version": "1.0"
    }
    
    # Guardar recetas
    recipes = [
        ("valid_recipe.json", valid_recipe),
        ("invalid_recipe.json", invalid_recipe),
        ("warning_recipe.json", warning_recipe),
        ("ingredient_issues_recipe.json", ingredient_issues_recipe)
    ]
    
    for filename, recipe in recipes:
        filepath = os.path.join(test_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(recipe, f, indent=2, ensure_ascii=False)
        print(f"✅ Creada receta de prueba: {filename}")
    
    return test_dir

def test_moderation_system():
    """Probar el sistema de moderación completo"""
    
    print("🧪 INICIANDO PRUEBAS DEL SISTEMA DE MODERACIÓN")
    print("=" * 60)
    
    # Crear recetas de prueba
    print("\n📝 Creando recetas de prueba...")
    test_dir = create_test_recipes()
    
    # Ejecutar moderación
    print(f"\n🔍 Ejecutando moderación en: {test_dir}")
    moderator = RecipeModerator()
    results = moderator.moderate_all_recipes(test_dir)
    
    # Mostrar resultados
    print("\n📊 RESULTADOS DE LA MODERACIÓN:")
    print("=" * 60)
    
    report = moderator.generate_report(results)
    print(report)
    
    # Verificar resultados esperados
    print("\n✅ VERIFICACIÓN DE RESULTADOS:")
    print("-" * 40)
    
    expected_approved = 2  # La receta válida y la de warnings
    expected_rejected = 2  # Las 2 con problemas reales
    
    if results["approved_recipes"] == expected_approved:
        print(f"✅ Recetas aprobadas: {results['approved_recipes']} (esperado: {expected_approved})")
    else:
        print(f"❌ Recetas aprobadas: {results['approved_recipes']} (esperado: {expected_approved})")
    
    if results["rejected_recipes"] == expected_rejected:
        print(f"✅ Recetas rechazadas: {results['rejected_recipes']} (esperado: {expected_rejected})")
    else:
        print(f"❌ Recetas rechazadas: {results['rejected_recipes']} (esperado: {expected_rejected})")
    
    # Mostrar detalles de cada receta
    print("\n📋 DETALLES POR RECETA:")
    print("-" * 40)
    
    for recipe in results["recipes"]:
        status = "✅ APROBADA" if recipe["approved"] else "❌ RECHAZADA"
        print(f"\n{status}: {recipe['recipe_name']} (Score: {recipe['score']}/100)")
        
        if recipe["issues"]:
            print("   Problemas:")
            for issue in recipe["issues"]:
                print(f"   - {issue}")
        
        if recipe["warnings"]:
            print("   Advertencias:")
            for warning in recipe["warnings"]:
                print(f"   - {warning}")
    
    # Limpiar archivos de prueba
    print(f"\n🧹 Limpiando archivos de prueba...")
    import shutil
    shutil.rmtree(test_dir)
    print("✅ Archivos de prueba eliminados")
    
    # Resultado final
    print("\n🎯 RESUMEN FINAL:")
    print("=" * 60)
    
    if results["approved_recipes"] == expected_approved and results["rejected_recipes"] == expected_rejected:
        print("✅ TODAS LAS PRUEBAS PASARON")
        print("✅ El sistema de moderación funciona correctamente")
        return True
    else:
        print("❌ ALGUNAS PRUEBAS FALLARON")
        print("❌ Revisar la implementación del sistema de moderación")
        return False

def test_individual_validation():
    """Probar validación individual de recetas"""
    
    print("\n🔬 PRUEBAS DE VALIDACIÓN INDIVIDUAL:")
    print("=" * 60)
    
    moderator = RecipeModerator()
    
    # Receta perfecta
    perfect_recipe = {
        "name": "Receta Perfecta",
        "servings": 4,
        "category": "Arroces",
        "notes": "Una receta perfecta para probar",
        "ingredients": [
            {"name": "Ingrediente 1", "quantity": 100, "unit": "g"},
            {"name": "Ingrediente 2", "quantity": 200, "unit": "ml"}
        ]
    }
    
    result = moderator.validate_recipe(perfect_recipe)
    print(f"Receta perfecta: Score {result['score']}/100, Aprobada: {result['approved']}")
    
    # Receta con problemas
    bad_recipe = {
        "name": "",  # Sin nombre
        "servings": -1,  # Servings negativo
        "category": "",  # Sin categoría
        "ingredients": []  # Sin ingredientes
    }
    
    result = moderator.validate_recipe(bad_recipe)
    print(f"Receta problemática: Score {result['score']}/100, Aprobada: {result['approved']}")
    print("Problemas encontrados:")
    for issue in result["issues"]:
        print(f"  - {issue}")

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS DEL SISTEMA DE MODERACIÓN")
    print("=" * 60)
    
    try:
        # Pruebas de validación individual
        test_individual_validation()
        
        # Pruebas del sistema completo
        success = test_moderation_system()
        
        if success:
            print("\n🎉 ¡TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE!")
            sys.exit(0)
        else:
            print("\n💥 ALGUNAS PRUEBAS FALLARON")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n💥 ERROR DURANTE LAS PRUEBAS: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)