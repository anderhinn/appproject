import os
import requests
from pathlib import Path

#.env enne ei töötanud korrektselt, seega lihtne käsitsi laadimine
#Leiame .env faili tee, üks tase ülevalpool backend kausta
env_path = Path(__file__).resolve().parents[1] / ".env"

#loeme .env faili ridade kaupa
if env_path.exists():
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            #ignoreerime tühjad read ja kommentaarid
            if line and not line.startswith('#') and '=' in line:
                #jagame rea võtme ja väärtuse osaks
                key, value = line.split('=', 1)
                #puhastame võtme ja väärtuse
                key=key.strip()
                value = value.split('#', 1)[0].strip().strip('"').strip("'")
                #salvestame keskkonnamuutujaks
                os.environ[key] = value
#RAWG API baasurl
BASE = "https://api.rawg.io/api"

#Abifunktsioon GET päringute tegemiseks RAWG API-le
#Üldine get-päringu funktsioon RAWG API jaoks
#Lisab automaatselt API võtme ja käsitleb vigu
def _get(path, params=None):
    if params is None:
        params = {}
    #Loeme API võtme keskkonnamuutujatest
    RAWG_KEY = os.environ.get("RAWG_API_KEY", "").strip()
    #Kui võtit pole = katkestame
    if not RAWG_KEY:
        raise RuntimeError("RAWG_API_KEY puudub .env failis")
    #Teeme get-päringu RAWG API-le
    response = requests.get(f"{BASE}{path}", params={**params, "key": RAWG_KEY}, timeout=20)
    #Kui http staatus ei ole 200 viskab vea
    response.raise_for_status()
    #tagastame vastuse JSON-kujul
    return response.json()

#Mängude hankimine žanri järgi
#Toob RAWG API-st mängud kindla žanri järgi
#genre_slug nt shooter
#page_size = mitu mängu korraga kuvatakse
def get_games_by_genre(genre_slug, page=1, page_size=10):
    data = _get("/games", {"genres": genre_slug, "page": page, "page_size": page_size})
    #tagastame ainult mängude nimekirja
    return data.get("results", [])

#Mängu kirjledus, pildid jne
def get_game_details(game_id):
    return _get(f"/games/{game_id}")