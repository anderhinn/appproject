import os
import time
import requests
from dotenv import load_dotenv
load_dotenv()

FIREBASE_URL= os.environ.get("FIREBASE_URL")
#LFG - Looking For Group


def _database(path:str)->str:
    if not FIREBASE_URL:
        raise RuntimeError("FIREBASE_URL puudub .env failis")
    return f"{FIREBASE_URL.rstrip('/')}/{path}.json"

def add_lfg(user_id:str, username:str, game_id:str, game_name:str, note:str=""):
    data={
        "user_id": user_id,
        "username": username,
        "game_id": game_id,
        "game_name": game_name,
        "note": note,
        "timestamp": int(time.time()),
        "active": True,
    }
    r= requests.post(_database("lfg"), json=data)
    r.raise_for_status()
    return r.json()

def get_lfg_by_game(game_id:str):
    r= requests.get(_database("lfg"))
    r.raise_for_status()
    data= r.json() or {}
    results= []
    for key, value in data.items():
        if value.get("game_id") == game_id and value.get("active", True):
            value["id"]= key
            results.append(value)
    return results



#Messages plokk
def send_message(chat_id:str, sender_id:str, text:str):
    msg={
        "sender_id": sender_id,
        "text": text,
        "timestamp": int(time.time()),
    }
    r= requests.post(_database(f"chats/{chat_id}/messages"), json=msg)
    r.raise_for_status()
    return r.json()

def get_messages(chat_id:str):
    r= requests.get(_database(f"chats/{chat_id}/messages"))
    r.raise_for_status()
    data= r.json() or {}
    messages= list(data.values())
    messages.sort(key=lambda m: m.get("timestamp", 0))
    return messages


            