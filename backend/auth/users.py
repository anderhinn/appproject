import json
from pathlib import Path

fail=Path("backend/auth/kasutajad.json")

def lae_kasutajad():
    if not fail.exists():
        return {}
    with open(fail, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def salvesta_kasutajad(kasutajad:dict):
    fail.parent.mkdir(parents=True, exist_ok=True)
    with open(fail, 'w', encoding='utf-8') as f:
        json.dump(kasutajad, f, indent=2, ensure_ascii=False)

def leia_voi_lisa_kasutaja(nimi:str, steamid:str | None=None):
    kasutajad= lae_kasutajad()
    if steamid not in kasutajad:
        kasutajad[steamid]= {"nimi" : nimi or steamid}
        salvesta_kasutajad(kasutajad)
    else:
        if nimi and kasutajad[steamid].get("nimi") != nimi:
            kasutajad[steamid]["nimi"] = nimi
            salvesta_kasutajad(kasutajad)
    return kasutajad[steamid]    