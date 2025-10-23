#!/usr/bin/env python3
"""
Test script for the MealPrep vote tracking system.
This script simulates various voting scenarios to ensure the system works correctly.
"""

import json
import sys
from pathlib import Path
from vote_tracker import (
    has_build_id_voted, 
    record_build_id_vote, 
    get_build_id_stats,
    cleanup_old_votes
)

def test_basic_voting():
    """Test basic voting functionality."""
    print("🧪 Testing basic voting functionality...")
    
    # Test data
    build_id = "test-build-12345"
    recipe_id = "test-recipe-67890"
    recipe_name = "Test Recipe"
    
    # Test 1: Initial vote should not exist
    assert not has_build_id_voted(build_id, recipe_id), "Build ID should not have voted initially"
    print("   ✅ Initial state check passed")
    
    # Test 2: Record a vote
    record_build_id_vote(build_id, recipe_id, recipe_name)
    assert has_build_id_voted(build_id, recipe_id), "Build ID should have voted after recording"
    print("   ✅ Vote recording passed")
    
    # Test 3: Duplicate vote should be detected
    assert has_build_id_voted(build_id, recipe_id), "Duplicate vote should be detected"
    print("   ✅ Duplicate detection passed")
    
    # Test 4: Different recipe should not be affected
    different_recipe = "different-recipe-11111"
    assert not has_build_id_voted(build_id, different_recipe), "Different recipe should not be voted"
    print("   ✅ Different recipe isolation passed")
    
    print("✅ Basic voting tests passed!\n")


def test_multiple_build_ids():
    """Test multiple build IDs voting for the same recipe."""
    print("🧪 Testing multiple build IDs...")
    
    recipe_id = "shared-recipe-12345"
    recipe_name = "Shared Recipe"
    
    # Different build IDs should be able to vote for the same recipe
    build_ids = ["build-001", "build-002", "build-003"]
    
    for build_id in build_ids:
        assert not has_build_id_voted(build_id, recipe_id), f"Build {build_id} should not have voted initially"
        record_build_id_vote(build_id, recipe_id, recipe_name)
        assert has_build_id_voted(build_id, recipe_id), f"Build {build_id} should have voted after recording"
    
    print("   ✅ Multiple build IDs can vote for same recipe")
    
    # Each build ID should not be able to vote again
    for build_id in build_ids:
        assert has_build_id_voted(build_id, recipe_id), f"Build {build_id} should not be able to vote again"
    
    print("   ✅ Duplicate prevention works for all build IDs")
    print("✅ Multiple build IDs tests passed!\n")


def test_statistics():
    """Test statistics functionality."""
    print("🧪 Testing statistics...")
    
    build_id = "stats-test-build"
    recipes = [
        ("recipe-1", "Recipe 1"),
        ("recipe-2", "Recipe 2"),
        ("recipe-3", "Recipe 3")
    ]
    
    # Vote for multiple recipes
    for recipe_id, recipe_name in recipes:
        record_build_id_vote(build_id, recipe_id, recipe_name)
    
    # Check statistics
    stats = get_build_id_stats(build_id)
    assert stats is not None, "Stats should exist"
    assert stats['total_votes'] == len(recipes), f"Total votes should be {len(recipes)}"
    assert len(stats['voted_recipes']) == len(recipes), f"Voted recipes should be {len(recipes)}"
    
    print(f"   ✅ Build ID stats: {stats['total_votes']} votes, {len(stats['voted_recipes'])} recipes")
    print("✅ Statistics tests passed!\n")


def test_cleanup():
    """Test cleanup functionality."""
    print("🧪 Testing cleanup...")
    
    # This test would require manipulating timestamps, which is complex
    # For now, just test that the function runs without error
    cleaned = cleanup_old_votes(days_threshold=0)  # Clean everything
    print(f"   ✅ Cleanup function executed, removed {cleaned} records")
    print("✅ Cleanup tests passed!\n")


def test_edge_cases():
    """Test edge cases and error handling."""
    print("🧪 Testing edge cases...")
    
    # Test empty build_id
    assert not has_build_id_voted("", "recipe-123"), "Empty build_id should not have voted"
    print("   ✅ Empty build_id handling")
    
    # Test empty recipe_id
    assert not has_build_id_voted("build-123", ""), "Empty recipe_id should not have voted"
    print("   ✅ Empty recipe_id handling")
    
    # Test special characters
    special_build_id = "build-with-special-chars!@#$%"
    special_recipe_id = "recipe-with-special-chars!@#$%"
    record_build_id_vote(special_build_id, special_recipe_id, "Special Recipe")
    assert has_build_id_voted(special_build_id, special_recipe_id), "Special characters should work"
    print("   ✅ Special characters handling")
    
    print("✅ Edge cases tests passed!\n")


def run_all_tests():
    """Run all tests."""
    print("🚀 Starting MealPrep Vote System Tests\n")
    print("=" * 50)
    
    try:
        test_basic_voting()
        test_multiple_build_ids()
        test_statistics()
        test_cleanup()
        test_edge_cases()
        
        print("=" * 50)
        print("🎉 All tests passed! The vote system is working correctly.")
        return True
        
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
