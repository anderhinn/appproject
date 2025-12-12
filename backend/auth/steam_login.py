import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

STEAM_API_KEY= os.environ.get("api_key")
USERS_FILE="kasutajad.json"


def lae():
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            sisu= f.read().strip()
    
            if not sisu:
                return {}
        
            return json.loads(sisu)
    except FileNotFoundError:
        return {}


def salvestame(andmed:dict):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(andmed, f, indent=4, ensure_ascii=False)


def saame_id_urlist(url_voi_id:str) -> str:
    text= url_voi_id.strip()
    if text.startswith("http"):
        if '/profiles/' in text:
            return text.split('/profiles/')[1].strip('/')
        if '/id/' in text:
            return text.split('/id/')[1].strip('/')
    return text.strip('/')
    
def saame_steamid(id_voi_vanity: str) -> str:
    if id_voi_vanity.isdigit():
        return id_voi_vanity
    url=f'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/'
    params= {"key": STEAM_API_KEY, "vanityurl": id_voi_vanity}
    response= requests.get(url, params=params)
    data= response.json()

    if data.get('response', {}).get('success') != 1:
        raise ValueError("Ei suutnud vanity-nime SteamID-ks teisendada.")
    return data["response"]["steamid"]


def saame_nimi_steamidst(steamid):
    url=f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
    params= {"key": STEAM_API_KEY, "steamids": steamid}
    response= requests.get(url, params=params)
    data= response.json()
    players=data.get('response', {}).get('players', [])
    if not players:
        raise ValueError("Ei leidnud Steam kasutajat antud SteamID-ga.")
    
    player= players[0]
    nimi=player.get('personaname', "Tundmatu kasutaja")

    kasutajad= lae()
    kasutajad[steamid]= {
        "personame": nimi,
    }
    return {"steamid": steamid, "personame": nimi}


def registreeri_kasutaja(url_voi_id: str) -> dict:
    puhastatud_id= saame_id_urlist(url_voi_id)
    steamid= saame_steamid(puhastatud_id)
    info= saame_nimi_steamidst(steamid)
    return info
