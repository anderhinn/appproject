import os
import requests
from pathlib import Path

#.env enne ei töötanud korrektselt, seega lihtne käsitsi laadimine
env_path = Path(__file__).resolve().parents[1] / ".env"

#loeme ridade kaupa
if env_path.exists():
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                key=key.strip()
                value = value.split('#', 1)[0].strip().strip('"').strip("'")
                os.environ[key] = value

BASE = "https://api.rawg.io/api"

#Abifunktsioon GET päringute tegemiseks RAWG API-le
def _get(path, params=None):
    if params is None:
        params = {}
    RAWG_KEY = os.environ.get("RAWG_API_KEY", "").strip()
    if not RAWG_KEY:
        raise RuntimeError("RAWG_API_KEY puudub .env failis")
    response = requests.get(f"{BASE}{path}", params={**params, "key": RAWG_KEY}, timeout=20)
    response.raise_for_status()
    return response.json()

#Mängude hankimine žanri järgi
def get_games_by_genre(genre_slug, page=1, page_size=10):
    data = _get("/games", {"genres": genre_slug, "page": page, "page_size": page_size})
    return data.get("results", [])

#Mängu kirjledus, pildid jne
def get_game_details(game_id):
    return _get(f"/games/{game_id}")