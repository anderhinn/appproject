import os
import time
import requests
from dotenv import load_dotenv
#laeme .env
load_dotenv()

#firebase realtime database url
FIREBASE_URL= os.environ.get("FIREBASE_URL")
#LFG - Looking For Group

#Moodustab firebase päringu url'i
#Firebase RTDB REST API kasutab lõpus alati .json
def _database(path:str)->str:
    if not FIREBASE_URL:
        #Kui .env-s pole FIREBASE_URL siis ei saa ühtegi päringut teha
        raise RuntimeError("FIREBASE_URL puudub .env failis")
    #eemaldame lõpu "/" ja lisame path + .json
    return f"{FIREBASE_URL.rstrip('/')}/{path}.json"

#Lisab uue LFG kirje firebase'i
#user_id = steamid jne
def add_lfg(user_id:str, username:str, game_id:str, game_name:str, note:str=""):
    data={
        "user_id": user_id,
        "username": username,
        "game_id": game_id,
        "game_name": game_name,
        "note": note,
        "timestamp": int(time.time()),
        "active": True, #hiljem saab nii öelda peita ilma kustutamata
    }
    #POST - Firebase loob uue unikaalse kirje ID (push key)
    r= requests.post(_database("lfg"), json=data)
    r.raise_for_status() #kui viga, viskab exceptioni
    return r.json() #tagastab näiteks {"name": -90fi045tu9fdg"} jne

#Toob firebase'ist kõik LFG kirjed ja filtreerib
#need game'id järgi
#Tagastab listi kirjetest (dict)
def get_lfg_by_game(game_id:str):
    #GET kogu lfg haru
    r= requests.get(_database("lfg"))
    r.raise_for_status()
    #Firebase tagastab dicti kujul {"pushkey1": {...}} jne
    data= r.json() or {}
    results= []
    #Käime kõik kirjed läbi ja valime ainult sobivad
    for key, value in data.items():
        #Kontrollime, et game_id klapib ja kirje on aktiivne
        if value.get("game_id") == game_id and value.get("active", True):
            value["id"]= key #Lisame kirjele tema FIrebase key, et UI-s oleks unikaalne ID
            results.append(value)
    return results



#Messages plokk
#Saadab sõnumi kindlasse chatti.
#Chat_id=kahe kasutaja ühine ID
def send_message(chat_id:str, sender_id:str, text:str):
    #sõnumi objekt, mida firebase'i salvestame
    msg={
        "sender_id": sender_id,
        "text": text,
        "timestamp": int(time.time()),
    }
    #salvestame sõnumi teele chats/chat_id/messages
    r= requests.post(_database(f"chats/{chat_id}/messages"), json=msg)
    r.raise_for_status()
    return r.json()

#Toob kõik sõnumid selle chat_id kohta
#Tagastab listi sõnumitest ajajärjekorras
def get_messages(chat_id:str):
    #GET kõik sõnumid selle chati all
    r= requests.get(_database(f"chats/{chat_id}/messages"))
    r.raise_for_status()
    #Firebase tagastab dicti {"msgkey1": {...}}
    data= r.json() or {}
    #Teeme dict väärtustest listi
    messages= list(data.values())
    #sorteerime timestamp järgi
    messages.sort(key=lambda m: m.get("timestamp", 0))
    return messages


            