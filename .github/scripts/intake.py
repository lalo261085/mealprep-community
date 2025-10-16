import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / 'recipes_index.json'
RECIPES_DIR = ROOT / 'recipes'

def load_issue_payload() -> dict | None:
    raw = os.environ.get('GH_EVENT')
    if not raw:
        return None
    evt = json.loads(raw)
    issue = evt.get('issue') or {}
    title = (issue.get('title') or '').strip().lower()
    body = issue.get('body') or ''
    # Extraer JSON desde bloque ```json ... ```
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
            lst[i] = entry
            return
    lst.append(entry)

def handle_share(payload: dict) -> None:
    RECIPES_DIR.mkdir(parents=True, exist_ok=True)
    idx = load_index()
    name = (payload.get('name') or '').strip() or 'Receta'
    rid = normalize_id(payload.get('id') or payload.get('name') or '')
    path = f"recipes/{rid}.json"
    entry = {
        'id': rid,
        'name': name,
        'author': (payload.get('author') or '').strip(),
        'likes': int(payload.get('likes') or 0),
        'category': (payload.get('category') or '').strip(),
        'path': path,
    }
    details = {
        'ingredients': payload.get('ingredients') or [],
        'notes': payload.get('notes') or '',
        'servings': payload.get('servings') or 1,
        'category': payload.get('category') or '',
    }
    (ROOT / path).write_text(json.dumps(details, ensure_ascii=False, indent=2), encoding='utf-8')
    upsert_index_entry(idx, entry)
    save_index(idx)

def handle_vote(payload: dict) -> None:
    idx = load_index()
    rid = normalize_id(payload.get('id') or payload.get('name') or '')
    lst = idx.setdefault('recipes', [])
    for e in lst:
        if e.get('id') == rid:
            e['likes'] = int(e.get('likes') or 0) + 1
            break
    save_index(idx)

def main():
    issue = load_issue_payload()
    if not issue:
        print('No issue payload')
        return
    labels = set(issue['labels'])
    payload = issue['payload'] or {}
    if ('recipe' in labels) or issue['title'].startswith('share:'):
        handle_share(payload)
        msg = 'Gracias por compartir! La receta fue agregada/actualizada.'
    elif ('vote' in labels) or issue['title'].startswith('vote:'):
        handle_vote(payload)
        msg = 'Gracias por votar! Se incrementó el contador.'
    else:
        msg = 'No action for this issue.'
    # Commit y push
    os.system("git config user.name 'mealprep-bot'")
    os.system("git config user.email 'bot@mealprep'")
    os.system("git add recipes_index.json recipes || true")
    os.system("git commit -m 'community: update index/recipes via issue' || true")
    os.system("git push || true")
    print(msg)

if __name__ == '__main__':
    main()
