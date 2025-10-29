import json
import os
import re
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / 'recipes_index.json'
RECIPES_DIR = ROOT / 'recipes'

# Import vote tracking system
from vote_tracker import has_build_id_voted, record_build_id_vote, cleanup_old_votes


def load_issue_payload() -> dict | None:
    raw = os.environ.get('GH_EVENT')
    if not raw:
        return None
    evt = json.loads(raw)
    issue = evt.get('issue') or {}
    title = (issue.get('title') or '').strip().lower()
    body = issue.get('body') or ''
    # Extract JSON from a code block ```json ... ```
    m = re.search(r"```json\s*(.*?)\s*```", body, re.DOTALL | re.IGNORECASE)
    payload = None
    if m:
        try:
            payload = json.loads(m.group(1))
        except Exception:
            payload = None
    return {
        'title': title,
        'labels': [l.get('name','').lower() for l in (issue.get('labels') or [])],
        'payload': payload,
        'issue_number': issue.get('number'),
    }


def load_index() -> dict:
    if INDEX.exists():
        try:
            return json.loads(INDEX.read_text(encoding='utf-8'))
        except Exception:
            pass
    return {'recipes': []}


def save_index(idx: dict) -> None:
    INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2), encoding='utf-8')


def normalize_id(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9_-]+", "-", (text or '').strip()).strip('-').lower()
    return s or 'recipe'


def upsert_index_entry(idx: dict, entry: dict) -> None:
    rid = entry.get('id')
    lst = idx.setdefault('recipes', [])
    for i, e in enumerate(lst):
        if (e.get('id') == rid) or (rid and e.get('path') == entry.get('path')):
            # Preserve original creation timestamp if not provided
            if not entry.get('created_at') and e.get('created_at'):
                entry['created_at'] = e.get('created_at')
            lst[i] = entry
            return
    lst.append(entry)


def handle_share(payload: dict) -> tuple[bool, str]:
    """Create a new recipe entry. Reject if name or id already exists.

    Returns (success, message).
    """
    RECIPES_DIR.mkdir(parents=True, exist_ok=True)
    idx = load_index()
    now = datetime.now(timezone.utc).isoformat()

    name = (payload.get('name') or '').strip() or 'Receta'
    rid = normalize_id(payload.get('id') or payload.get('name') or '')
    path = f"recipes/{rid}.json"

    # Reject duplicates by id or by case-insensitive name
    normalized_name = name.lower()
    for e in idx.get('recipes', []):
        existing_id = (e.get('id') or '').strip()
        existing_name = (e.get('name') or '').strip().lower()
        if existing_id == rid:
            return False, (
                f"Error: ya existe una receta con id '{rid}' (nombre: {e.get('name','')}). "
                "No se permiten duplicados."
            )
        if existing_name and existing_name == normalized_name:
            return False, (
                f"Error: ya existe una receta con el mismo nombre: '{name}' (id: {existing_id}). "
                "Por favor elegí otro nombre."
            )

    # Create new entry
    entry = {
        'id': rid,
        'name': name,
        'author': (payload.get('author') or '').strip(),
        'likes': int(payload.get('likes') or 0),
        'category': (payload.get('category') or '').strip(),
        'path': path,
        'created_at': now,
        'updated_at': now,
    }
    # Save recipe details
    details = {
        'ingredients': payload.get('ingredients') or [],
        'notes': payload.get('notes') or '',
        'servings': payload.get('servings') or 1,
        'category': payload.get('category') or '',
    }
    (ROOT / path).write_text(json.dumps(details, ensure_ascii=False, indent=2), encoding='utf-8')
    upsert_index_entry(idx, entry)
    save_index(idx)
    return True, f"Gracias por compartir! La receta '{name}' fue agregada."


def handle_vote(payload: dict) -> tuple[bool, str]:
    """
    Handle a vote request. Returns (success, message).
    """
    idx = load_index()
    rid = normalize_id(payload.get('id') or payload.get('name') or '')
    build_id = payload.get('build_id', '').strip()
    
    # Check if build_id is provided
    if not build_id:
        return False, "Error: build_id es requerido para votar"
    
    # Check if this build_id has already voted for this recipe
    if has_build_id_voted(build_id, rid):
        return False, f"Ya has votado por esta receta desde esta instalación (build_id: {build_id[:8]}...)"
    
    # Find the recipe in the index
    recipe_found = False
    lst = idx.setdefault('recipes', [])
    for e in lst:
        if e.get('id') == rid:
            # Record the vote in the tracker
            record_build_id_vote(build_id, rid, e.get('name', ''))
            
            # Increment the likes count
            e['likes'] = int(e.get('likes') or 0) + 1
            now = datetime.now(timezone.utc).isoformat()
            e['updated_at'] = now
            e['last_vote_at'] = now
            recipe_found = True
            break
    
    if not recipe_found:
        return False, f"Receta no encontrada: {rid}"
    
    save_index(idx)
    return True, f"¡Voto registrado! Likes actualizados para la receta '{rid}'"


def main():
    issue = load_issue_payload()
    if not issue:
        print('No issue payload')
        return
    
    labels = set(issue['labels'])
    payload = issue['payload'] or {}
    
    # Clean up old votes periodically (every 10th run)
    import random
    if random.randint(1, 10) == 1:
        cleaned = cleanup_old_votes(days_threshold=90)
        if cleaned > 0:
            print(f"Cleaned up {cleaned} old vote records")
    
    if ('recipe' in labels) or issue['title'].startswith('share:'):
        success, msg = handle_share(payload)
        commit_changes = success
    elif ('vote' in labels) or issue['title'].startswith('vote:'):
        success, msg = handle_vote(payload)
        commit_changes = success
        if not success:
            print(f"Vote rejected: {msg}")
    else:
        msg = 'No action for this issue.'
        commit_changes = False
    
    # Commit and push changes back only if successful
    if commit_changes:
        os.system("git config user.name 'mealprep-bot'")
        os.system("git config user.email 'bot@mealprep'")
        os.system("git add recipes_index.json recipes .github/data/vote_tracker.json || true")
        os.system("git commit -m 'community: update index/recipes via issue' || true")
        os.system("git push || true")
    
    print(msg)


if __name__ == '__main__':
    main()
