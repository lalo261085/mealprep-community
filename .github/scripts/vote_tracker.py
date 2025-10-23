"""
Vote tracking system to prevent duplicate votes from the same build_id.
This module manages a JSON file that tracks which build_ids have voted for which recipes.
"""

import json
import os
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Set, Optional

ROOT = Path(__file__).resolve().parents[2]
VOTE_TRACKER_FILE = ROOT / '.github' / 'data' / 'vote_tracker.json'


def load_vote_tracker() -> Dict[str, Dict[str, any]]:
    """Load the vote tracker data from JSON file."""
    if not VOTE_TRACKER_FILE.exists():
        return {}
    
    try:
        with open(VOTE_TRACKER_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def save_vote_tracker(data: Dict[str, Dict[str, any]]) -> None:
    """Save the vote tracker data to JSON file."""
    VOTE_TRACKER_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(VOTE_TRACKER_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def has_build_id_voted(build_id: str, recipe_id: str) -> bool:
    """Check if a build_id has already voted for a specific recipe."""
    tracker = load_vote_tracker()
    
    # Check if build_id exists and has voted for this recipe
    if build_id in tracker:
        voted_recipes = tracker[build_id].get('voted_recipes', set())
        return recipe_id in voted_recipes
    
    return False


def record_build_id_vote(build_id: str, recipe_id: str, recipe_name: str) -> None:
    """Record that a build_id has voted for a specific recipe."""
    tracker = load_vote_tracker()
    
    if build_id not in tracker:
        tracker[build_id] = {
            'first_vote_at': datetime.now(timezone.utc).isoformat(),
            'voted_recipes': set(),
            'total_votes': 0
        }
    
    # Convert set to list for JSON serialization
    if isinstance(tracker[build_id].get('voted_recipes'), set):
        tracker[build_id]['voted_recipes'] = list(tracker[build_id]['voted_recipes'])
    
    # Add recipe to voted list if not already there
    voted_recipes = set(tracker[build_id].get('voted_recipes', []))
    if recipe_id not in voted_recipes:
        voted_recipes.add(recipe_id)
        tracker[build_id]['voted_recipes'] = list(voted_recipes)
        tracker[build_id]['total_votes'] = len(voted_recipes)
        tracker[build_id]['last_vote_at'] = datetime.now(timezone.utc).isoformat()
    
    save_vote_tracker(tracker)


def get_build_id_stats(build_id: str) -> Optional[Dict[str, any]]:
    """Get statistics for a specific build_id."""
    tracker = load_vote_tracker()
    return tracker.get(build_id)


def cleanup_old_votes(days_threshold: int = 90) -> int:
    """Clean up vote records older than the specified number of days."""
    tracker = load_vote_tracker()
    cutoff_date = datetime.now(timezone.utc).timestamp() - (days_threshold * 24 * 60 * 60)
    removed_count = 0
    
    for build_id in list(tracker.keys()):
        build_data = tracker[build_id]
        first_vote = build_data.get('first_vote_at')
        
        if first_vote:
            try:
                first_vote_timestamp = datetime.fromisoformat(first_vote.replace('Z', '+00:00')).timestamp()
                if first_vote_timestamp < cutoff_date:
                    del tracker[build_id]
                    removed_count += 1
            except Exception:
                # If we can't parse the date, keep the record
                pass
    
    if removed_count > 0:
        save_vote_tracker(tracker)
    
    return removed_count


def get_recipe_vote_stats(recipe_id: str) -> Dict[str, int]:
    """Get voting statistics for a specific recipe."""
    tracker = load_vote_tracker()
    unique_voters = 0
    total_votes = 0
    
    for build_id, data in tracker.items():
        voted_recipes = data.get('voted_recipes', [])
        if recipe_id in voted_recipes:
            unique_voters += 1
        total_votes += data.get('total_votes', 0)
    
    return {
        'unique_voters': unique_voters,
        'total_votes': total_votes
    }


if __name__ == '__main__':
    # Test the vote tracker
    test_build_id = "test-build-123"
    test_recipe_id = "test-recipe-456"
    
    print(f"Has {test_build_id} voted for {test_recipe_id}? {has_build_id_voted(test_build_id, test_recipe_id)}")
    
    record_build_id_vote(test_build_id, test_recipe_id, "Test Recipe")
    print(f"After recording vote: {has_build_id_voted(test_build_id, test_recipe_id)}")
    
    stats = get_build_id_stats(test_build_id)
    print(f"Build ID stats: {stats}")