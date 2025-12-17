import os
import json
import requests
from dotenv import load_dotenv

# Laeme .env failist keskkonnamuutujad (nt API võtmed)
load_dotenv()

# Võtame Steam API võtme keskkonnamuutujatest
# (see peab olema .env failis)
STEAM_API_KEY = os.environ.get("api_key")

# Fail, kuhu salvestatakse kasutajad
USERS_FILE = "backend/auth/kasutajad.json"



def lae():
    # Üritame lugeda kasutajate faili
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            sisu = f.read().strip()

            # Kui fail on tühi, tagastame tühja sõnastiku
            if not sisu:
                return {}

            # Teisendame JSON-teksti Python dict-iks
            return json.loads(sisu)

    # Kui faili ei ole olemas, tagastame tühja dict-i
    except FileNotFoundError:
        return {}


def salvestame(andmed: dict):
    # Salvestame kasutajate andmed faili JSON-kujul
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(andmed, f, indent=4, ensure_ascii=False) #indent teeb sõnastiku 'tulpadeks'. ensure_ascii Väga oluline eesti keele jaoks.



def saame_id_urlist(url_voi_id: str) -> str:
    # Eemaldame algusest ja lõpust tühikud
    text = url_voi_id.strip()

    # Kui sisestus on link
    if text.startswith("http"):

        # Kui link on kujul /profiles/STEAMID
        if '/profiles/' in text:
            return text.split('/profiles/')[1].strip('/')

        # Kui link on kujul /id/vanityname
        if '/id/' in text:
            return text.split('/id/')[1].strip('/')

    # Kui ei ole link, siis eeldame,
    # et kasutaja sisestas ID või nime otse
    return text.strip('/')

    
def saame_steamid(id_voi_vanity: str) -> str:
    # Kui sisend on ainult numbrid,
    # siis see on juba SteamID
    if id_voi_vanity.isdigit():
        return id_voi_vanity

    url=f'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/'
    # Steam API endpoint vanity-nime teisendamiseks SteamID-ks
    url = 'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/'
    params = {
        "key": STEAM_API_KEY,
        "vanityurl": id_voi_vanity
    }

    # Teeme päringu Steam API-le
    response = requests.get(url, params=params)

    # Teisendame vastuse JSON-iks
    data = response.json()

    # Kui Steam ei suutnud nime lahendada
    if data.get('response', {}).get('success') != 1:
        raise ValueError("Ei suutnud vanity-nime SteamID-ks teisendada.")

    # Tagastame SteamID
    return data["response"]["steamid"]



def saame_nimi_steamidst(steamid):
    # Steam API endpoint kasutaja info saamiseks
    url = 'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
    params = {
        "key": STEAM_API_KEY,
        "steamids": steamid
    }

    # Teeme päringu Steam API-le
    response = requests.get(url, params=params)
    data = response.json()

        # Võtame kasutajate listi vastusest
    players = data.get('response', {}).get('players', [])

    # Kui kasutajat ei leitud
    if not players:
        raise ValueError("Ei leidnud Steam kasutajat antud SteamID-ga.")

    
    # Võtame esimese (ja ainsa) kasutaja
    player = players[0]

    # Võtame kasutajanime
    nimi = player.get('personaname', "Tundmatu kasutaja")

   
    # Laeme olemasolevad kasutajad
    kasutajad = lae()

    # Salvestame uue kasutaja (või uuendame olemasolevat)
    kasutajad[steamid] = {
        "personame": nimi,
    }

        # Tagastame info edasi Streamlitile
    return {"steamid": steamid, "personame": nimi}


def registreeri_kasutaja(url_voi_id: str) -> dict:
    # Puhastame kasutaja sisendi
    puhastatud_id = saame_id_urlist(url_voi_id)

    # Leiame SteamID
    steamid = saame_steamid(puhastatud_id)

    # Leiame kasutajanime
    info = saame_nimi_steamidst(steamid)

    # Tagastame kogu info
    return info
