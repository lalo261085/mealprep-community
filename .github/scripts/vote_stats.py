#!/usr/bin/env python3
"""
Vote statistics and management script for the MealPrep community repository.
This script provides insights into voting patterns and helps manage the vote tracking system.
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone
from vote_tracker import load_vote_tracker, get_recipe_vote_stats, cleanup_old_votes

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


def show_vote_statistics():
    """Display comprehensive vote statistics."""
    tracker = load_vote_tracker()
    index = load_index()
    
    print("=== MEALPREP COMMUNITY VOTE STATISTICS ===\n")
    
    # Overall statistics
    total_build_ids = len(tracker)
    total_votes = sum(data.get('total_votes', 0) for data in tracker.values())
    
    print(f"📊 Overall Statistics:")
    print(f"   • Total unique installations (build_ids): {total_build_ids}")
    print(f"   • Total votes cast: {total_votes}")
    print(f"   • Average votes per installation: {total_votes / max(total_build_ids, 1):.2f}")
    print()
    
    # Top voters
    top_voters = sorted(
        [(build_id, data.get('total_votes', 0)) for build_id, data in tracker.items()],
        key=lambda x: x[1],
        reverse=True
    )[:10]
    
    print("🏆 Top Voters (by total votes):")
    for i, (build_id, votes) in enumerate(top_voters, 1):
        print(f"   {i:2d}. {build_id[:12]}... ({votes} votes)")
    print()
    
    # Recipe statistics
    recipes = index.get('recipes', [])
    recipe_stats = []
    
    for recipe in recipes:
        recipe_id = recipe.get('id', '')
        recipe_name = recipe.get('name', 'Unknown')
        likes = recipe.get('likes', 0)
        stats = get_recipe_vote_stats(recipe_id)
        
        recipe_stats.append({
            'id': recipe_id,
            'name': recipe_name,
            'likes': likes,
            'unique_voters': stats['unique_voters']
        })
    
    # Sort by likes
    recipe_stats.sort(key=lambda x: x['likes'], reverse=True)
    
    print("🍽️  Top Recipes (by likes):")
    for i, recipe in enumerate(recipe_stats[:10], 1):
        print(f"   {i:2d}. {recipe['name'][:30]:<30} ({recipe['likes']} likes, {recipe['unique_voters']} unique voters)")
    print()
    
    # Recent activity
    recent_voters = []
    for build_id, data in tracker.items():
        last_vote = data.get('last_vote_at')
        if last_vote:
            try:
                last_vote_dt = datetime.fromisoformat(last_vote.replace('Z', '+00:00'))
                recent_voters.append((build_id, last_vote_dt, data.get('total_votes', 0)))
            except Exception:
                pass
    
    recent_voters.sort(key=lambda x: x[1], reverse=True)
    
    print("🕒 Recent Activity (last 10 voters):")
    for build_id, last_vote, total_votes in recent_voters[:10]:
        time_ago = datetime.now(timezone.utc) - last_vote
        hours_ago = int(time_ago.total_seconds() / 3600)
        print(f"   • {build_id[:12]}... ({total_votes} total votes, {hours_ago}h ago)")
    print()


def show_duplicate_votes():
    """Show potential duplicate voting attempts."""
    tracker = load_vote_tracker()
    
    print("🔍 Duplicate Vote Analysis:")
    print("   (This would show if any build_id tried to vote multiple times for the same recipe)")
    print("   (Currently, duplicates are prevented at the time of voting)")
    print()


def cleanup_old_data(days_threshold=90):
    """Clean up old vote data."""
    print(f"🧹 Cleaning up vote data older than {days_threshold} days...")
    cleaned = cleanup_old_votes(days_threshold)
    print(f"   Removed {cleaned} old vote records")
    print()


def show_help():
    """Show help information."""
    print("MealPrep Community Vote Statistics Tool")
    print("Usage: python vote_stats.py [command]")
    print()
    print("Commands:")
    print("  stats     - Show comprehensive vote statistics (default)")
    print("  cleanup   - Clean up old vote data (90+ days)")
    print("  duplicates - Show duplicate vote analysis")
    print("  help      - Show this help message")
    print()


def main():
    if len(sys.argv) < 2:
        command = "stats"
    else:
        command = sys.argv[1].lower()
    
    if command == "stats":
        show_vote_statistics()
    elif command == "cleanup":
        cleanup_old_data()
    elif command == "duplicates":
        show_duplicate_votes()
    elif command == "help":
        show_help()
    else:
        print(f"Unknown command: {command}")
        show_help()


if __name__ == '__main__':
    main()
