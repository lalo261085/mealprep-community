#!/usr/bin/env python3
"""
Script de moderación automática para recetas de la comunidad
Valida estructura, contenido y calidad de las recetas
"""

import json
import os
import re
import sys
from typing import List, Dict, Any, Tuple
from datetime import datetime

class RecipeModerator:
    """Moderador automático de recetas"""
    
    def __init__(self):
        # Palabras inapropiadas (expandible)
        self.inappropriate_words = [
            "spam", "xxx", "adult", "nsfw", "hate", "violence", 
            "illegal", "fake", "scam", "phishing", "malware"
        ]
        
        # Campos obligatorios
        self.required_fields = [
            "name", "servings", "category", "ingredients"
        ]
        
        # Patrones de validación
        self.name_pattern = re.compile(r'^[a-zA-ZáéíóúñÁÉÍÓÚÑ0-9\s\-\.\,\:\;\(\)]+$')
        
    def validate_recipe(self, recipe: Dict[str, Any]) -> Dict[str, Any]:
        """Validar una receta individual"""
        issues = []
        warnings = []
        
        # 1. Verificar campos obligatorios
        for field in self.required_fields:
            if field not in recipe or not recipe[field]:
                issues.append(f"Campo obligatorio faltante: {field}")
        
        # 2. Validar nombre de receta
        if recipe.get('name'):
            name = recipe['name'].strip()
            if len(name) < 3:
                issues.append("Nombre de receta muy corto (mínimo 3 caracteres)")
            elif len(name) > 100:
                issues.append("Nombre de receta muy largo (máximo 100 caracteres)")
            elif not self.name_pattern.match(name):
                issues.append("Nombre de receta contiene caracteres no válidos")
            elif not any(c.isalpha() for c in name):
                issues.append("Nombre de receta debe contener al menos una letra")
        
        # 3. Validar porciones
        if recipe.get('servings'):
            try:
                servings = int(recipe['servings'])
                if servings < 1:
                    issues.append("Número de porciones debe ser mayor a 0")
                elif servings > 100:
                    warnings.append("Número de porciones muy alto (más de 100)")
            except (ValueError, TypeError):
                issues.append("Número de porciones debe ser un número entero")
        
        # 4. Validar categoría
        if recipe.get('category'):
            category = recipe['category'].strip()
            if len(category) < 2:
                issues.append("Categoría muy corta (mínimo 2 caracteres)")
            elif len(category) > 50:
                issues.append("Categoría muy larga (máximo 50 caracteres)")
        
        # 5. Validar ingredientes
        if recipe.get('ingredients'):
            if not isinstance(recipe['ingredients'], list):
                issues.append("Ingredientes debe ser una lista")
            else:
                if len(recipe['ingredients']) == 0:
                    issues.append("Receta debe tener al menos un ingrediente")
                elif len(recipe['ingredients']) > 50:
                    warnings.append("Muchos ingredientes (más de 50)")
                
                for i, ingredient in enumerate(recipe['ingredients']):
                    if not isinstance(ingredient, dict):
                        issues.append(f"Ingrediente {i+1} debe ser un objeto")
                        continue
                    
                    if not ingredient.get('name'):
                        issues.append(f"Ingrediente {i+1} no tiene nombre")
                    else:
                        name = ingredient['name'].strip()
                        if len(name) < 2:
                            issues.append(f"Ingrediente {i+1}: nombre muy corto")
                        elif len(name) > 100:
                            issues.append(f"Ingrediente {i+1}: nombre muy largo")
        
        # 6. Detectar contenido inapropiado
        recipe_text = json.dumps(recipe, ensure_ascii=False).lower()
        for word in self.inappropriate_words:
            if word in recipe_text:
                issues.append(f"Contenido inapropiado detectado: {word}")
        
        # 7. Validar notas (opcional)
        if recipe.get('notes'):
            notes = recipe['notes'].strip()
            if len(notes) > 500:
                warnings.append("Notas muy largas (más de 500 caracteres)")
        
        return {
            "recipe_id": recipe.get('id', 'unknown'),
            "recipe_name": recipe.get('name', 'Sin nombre'),
            "issues": issues,
            "warnings": warnings,
            "approved": len(issues) == 0,
            "score": self._calculate_quality_score(recipe, issues, warnings)
        }
    
    def _calculate_quality_score(self, recipe: Dict[str, Any], issues: List[str], warnings: List[str]) -> int:
        """Calcular puntuación de calidad (0-100)"""
        score = 100
        
        # Penalizar por issues
        score -= len(issues) * 20
        
        # Penalizar por warnings
        score -= len(warnings) * 5
        
        # Bonificar por completitud
        if recipe.get('notes'):
            score += 5
        if recipe.get('ingredients') and len(recipe['ingredients']) >= 3:
            score += 5
        if recipe.get('category') and recipe['category'] != 'Sin categoría':
            score += 5
        
        return max(0, min(100, score))
    
    def moderate_all_recipes(self, recipes_dir: str) -> Dict[str, Any]:
        """Moderar todas las recetas en un directorio"""
        results = {
            "total_recipes": 0,
            "approved_recipes": 0,
            "rejected_recipes": 0,
            "total_issues": 0,
            "total_warnings": 0,
            "recipes": [],
            "summary": {}
        }
        
        if not os.path.exists(recipes_dir):
            print(f"❌ Directorio no encontrado: {recipes_dir}")
            return results
        
        print(f"🔍 Moderando recetas en: {recipes_dir}")
        
        for filename in sorted(os.listdir(recipes_dir)):
            if filename.endswith('.json'):
                filepath = os.path.join(recipes_dir, filename)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        recipe = json.load(f)
                    
                    results["total_recipes"] += 1
                    moderation_result = self.validate_recipe(recipe)
                    results["recipes"].append(moderation_result)
                    
                    if moderation_result["approved"]:
                        results["approved_recipes"] += 1
                        print(f"✅ {filename}: {moderation_result['recipe_name']} (Score: {moderation_result['score']})")
                    else:
                        results["rejected_recipes"] += 1
                        print(f"❌ {filename}: {moderation_result['recipe_name']}")
                        for issue in moderation_result["issues"]:
                            print(f"   - {issue}")
                    
                    results["total_issues"] += len(moderation_result["issues"])
                    results["total_warnings"] += len(moderation_result["warnings"])
                    
                except json.JSONDecodeError as e:
                    print(f"❌ {filename}: Error de JSON - {e}")
                    results["rejected_recipes"] += 1
                    results["total_issues"] += 1
                except Exception as e:
                    print(f"❌ {filename}: Error inesperado - {e}")
                    results["rejected_recipes"] += 1
                    results["total_issues"] += 1
        
        # Generar resumen
        results["summary"] = {
            "approval_rate": (results["approved_recipes"] / results["total_recipes"] * 100) if results["total_recipes"] > 0 else 0,
            "average_score": sum(r["score"] for r in results["recipes"]) / len(results["recipes"]) if results["recipes"] else 0,
            "most_common_issues": self._get_most_common_issues(results["recipes"])
        }
        
        return results
    
    def _get_most_common_issues(self, recipes: List[Dict[str, Any]]) -> List[Tuple[str, int]]:
        """Obtener los issues más comunes"""
        issue_count = {}
        for recipe in recipes:
            for issue in recipe["issues"]:
                issue_count[issue] = issue_count.get(issue, 0) + 1
        
        return sorted(issue_count.items(), key=lambda x: x[1], reverse=True)[:5]
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generar reporte de moderación"""
        report = []
        report.append("=" * 60)
        report.append("📋 REPORTE DE MODERACIÓN AUTOMÁTICA")
        report.append("=" * 60)
        report.append(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Estadísticas generales
        report.append("📊 ESTADÍSTICAS GENERALES:")
        report.append(f"   Total de recetas: {results['total_recipes']}")
        report.append(f"   Recetas aprobadas: {results['approved_recipes']}")
        report.append(f"   Recetas rechazadas: {results['rejected_recipes']}")
        report.append(f"   Tasa de aprobación: {results['summary']['approval_rate']:.1f}%")
        report.append(f"   Puntuación promedio: {results['summary']['average_score']:.1f}/100")
        report.append("")
        
        # Issues más comunes
        if results['summary']['most_common_issues']:
            report.append("⚠️  ISSUES MÁS COMUNES:")
            for issue, count in results['summary']['most_common_issues']:
                report.append(f"   - {issue} ({count} veces)")
            report.append("")
        
        # Recetas rechazadas
        rejected = [r for r in results['recipes'] if not r['approved']]
        if rejected:
            report.append("❌ RECETAS RECHAZADAS:")
            for recipe in rejected:
                report.append(f"   - {recipe['recipe_name']} ({recipe['recipe_id']})")
                for issue in recipe['issues']:
                    report.append(f"     • {issue}")
            report.append("")
        
        # Recetas con warnings
        warned = [r for r in results['recipes'] if r['warnings']]
        if warned:
            report.append("⚠️  RECETAS CON ADVERTENCIAS:")
            for recipe in warned:
                report.append(f"   - {recipe['recipe_name']} (Score: {recipe['score']})")
                for warning in recipe['warnings']:
                    report.append(f"     • {warning}")
            report.append("")
        
        report.append("=" * 60)
        
        return "\n".join(report)

def main():
    """Función principal"""
    recipes_dir = "recipes"
    
    if len(sys.argv) > 1:
        recipes_dir = sys.argv[1]
    
    moderator = RecipeModerator()
    results = moderator.moderate_all_recipes(recipes_dir)
    
    # Generar y mostrar reporte
    report = moderator.generate_report(results)
    print(report)
    
    # Guardar reporte en archivo
    with open("moderation_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
    
    # Salir con código de error si hay recetas rechazadas
    if results["rejected_recipes"] > 0:
        print(f"\n❌ Moderación fallida: {results['rejected_recipes']} recetas rechazadas")
        sys.exit(1)
    else:
        print(f"\n✅ Moderación exitosa: {results['approved_recipes']} recetas aprobadas")
        sys.exit(0)

if __name__ == "__main__":
    main()