import json
from pathlib import Path

#Fail kuhu salvestame kasutajate andmed
fail=Path("backend/auth/kasutajad.json")

#Loeb kasutajate andmed json-failist
#Kui fail ei ole olemas, tagastab tühja sõnastiku
def lae_kasutajad():
    if not fail.exists():
        #faili pole =pole ka kasutajaid
        return {}
    #avame faili lugemiseks
    with open(fail, 'r', encoding='utf-8') as f:
        return json.load(f)
    
#salvestab kasutajate sõnastiku json-faili
#vajadusel loob kausta automaatselt
def salvesta_kasutajad(kasutajad:dict):
    #loome kausta, kui ei eksisteeri
    fail.parent.mkdir(parents=True, exist_ok=True)
    #kirjutame andmed faili
    with open(fail, 'w', encoding='utf-8') as f:
        json.dump(kasutajad, f, indent=2, ensure_ascii=False)

#Leiab kasutaja steamid järgi või lisab uue kasutaja
#kui steamid pole olemas veel = lisatakse uus kirje
#kui nimi muutunud = uuendatakse
#tagastab alati kasutaja andmed
def leia_voi_lisa_kasutaja(nimi:str, steamid:str | None=None):
    #loeme olemasolevad kasutajad
    kasutajad= lae_kasutajad()
    #kui seda steamid-d veel pole = lisame uus kasutaja
    if steamid not in kasutajad:
        kasutajad[steamid]= {"nimi" : nimi or steamid}
        salvesta_kasutajad(kasutajad)
    else:
        #kui kasutaja on olemas, aga nimi muutunud = uuendame nime
        if nimi and kasutajad[steamid].get("nimi") != nimi:
            kasutajad[steamid]["nimi"] = nimi
            salvesta_kasutajad(kasutajad)
    #tagastame kasutaja andmed
    return kasutajad[steamid]