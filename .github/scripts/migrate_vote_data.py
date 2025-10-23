#!/usr/bin/env python3
"""
Migration script for existing vote data.
This script helps migrate any existing vote data to the new build_id tracking system.
"""

import json
import os
from pathlib import Path
from datetime import datetime, timezone
from vote_tracker import load_vote_tracker, save_vote_tracker

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / 'recipes_index.json'


def load_index():
    """Load the recipes index."""
    if INDEX.exists():
        try:
            return json.loads(INDEX.read_text(encoding='utf-8'))
        except Exception:
            pass
    return {'recipes': []}


def migrate_existing_votes():
    """
    Migrate existing vote data to the new system.
    This is a placeholder for any migration logic needed.
    """
    print("🔄 Migrating existing vote data...")
    
    # Load current index
    index = load_index()
    recipes = index.get('recipes', [])
    
    # For now, we don't have historical vote data to migrate
    # This function is here for future use if needed
    print("   ℹ️  No existing vote data to migrate")
    print("   ✅ Migration completed")
    
    return True


def initialize_vote_tracker():
    """Initialize the vote tracker with default structure."""
    print("🔧 Initializing vote tracker...")
    
    tracker = load_vote_tracker()
    
    # Add metadata if not present
    if 'metadata' not in tracker:
        tracker['metadata'] = {
            'version': '1.0',
            'created_at': datetime.now(timezone.utc).isoformat(),
            'description': 'MealPrep Community Vote Tracking System'
        }
        save_vote_tracker(tracker)
        print("   ✅ Vote tracker initialized with metadata")
    else:
        print("   ℹ️  Vote tracker already initialized")
    
    return True


def validate_system_integrity():
    """Validate the integrity of the vote tracking system."""
    print("🔍 Validating system integrity...")
    
    # Check if vote tracker file exists and is valid
    tracker = load_vote_tracker()
    
    # Validate structure
    required_keys = ['metadata']
    for key in required_keys:
        if key not in tracker:
            print(f"   ⚠️  Missing required key: {key}")
            return False
    
    print("   ✅ System integrity validated")
    return True


def create_sample_data():
    """Create sample data for testing purposes."""
    print("📝 Creating sample data...")
    
    # Only create sample data if no real data exists
    tracker = load_vote_tracker()
    if len(tracker) > 1:  # More than just metadata
        print("   ℹ️  Real data exists, skipping sample data creation")
        return True
    
    # Create some sample data
    sample_build_ids = [
        "sample-build-001",
        "sample-build-002", 
        "sample-build-003"
    ]
    
    sample_recipes = [
        ("sample-recipe-001", "Sample Recipe 1"),
        ("sample-recipe-002", "Sample Recipe 2"),
        ("sample-recipe-003", "Sample Recipe 3")
    ]
    
    from vote_tracker import record_build_id_vote
    
    for build_id in sample_build_ids:
        for recipe_id, recipe_name in sample_recipes:
            record_build_id_vote(build_id, recipe_id, recipe_name)
    
    print(f"   ✅ Created sample data: {len(sample_build_ids)} build IDs, {len(sample_recipes)} recipes")
    return True


def main():
    """Main migration function."""
    print("🚀 MealPrep Vote System Migration")
    print("=" * 40)
    
    try:
        # Initialize the system
        initialize_vote_tracker()
        
        # Migrate existing data
        migrate_existing_votes()
        
        # Validate integrity
        if not validate_system_integrity():
            print("❌ System integrity validation failed")
            return False
        
        # Create sample data if needed
        create_sample_data()
        
        print("=" * 40)
        print("✅ Migration completed successfully!")
        print("\nNext steps:")
        print("1. Test the system with: python .github/scripts/test_vote_system.py")
        print("2. View statistics with: python .github/scripts/vote_stats.py stats")
        print("3. The system is ready for production use!")
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
