import json                      
from pathlib import Path        

fail = Path("backend/auth/kasutajad.json")
# Failitee, kus kasutajate andmed salvestatakse


def lae_kasutajad():
    # Funktsioon loeb kasutajad JSON-failist

    if not fail.exists():
        # Kui faili ei eksisteeri, tagastame tühja sõnastiku
        return {}

    # Avame faili lugemiseks UTF-8 kodeeringuga
    with open(fail, 'r', encoding='utf-8') as f:
        # Loeme JSON-i ja teisendame selle Python sõnastikuks
        return json.load(f)


def salvesta_kasutajad(kasutajad: dict):
    # Funktsioon salvestab kasutajate sõnastiku JSON-faili

    # Loome kaustad backend/auth, kui neid veel ei ole
    fail.parent.mkdir(parents=True, exist_ok=True)

    # Avame faili kirjutamiseks UTF-8 kodeeringuga
    with open(fail, 'w', encoding='utf-8') as f:
        # Kirjutame sõnastiku JSON-faili
        json.dump(kasutajad, f, indent=2, ensure_ascii=False)


def leia_voi_lisa_kasutaja(nimi: str, steamid: str | None = None):
    # Funktsioon otsib kasutaja SteamID järgi või lisab uue kasutaja

    kasutajad = lae_kasutajad()
    # Laeme olemasolevad kasutajad failist

    if steamid not in kasutajad:
        # Kui sellise SteamID-ga kasutajat ei ole olemas

        kasutajad[steamid] = {"nimi": nimi or steamid}
        # Lisame uue kasutaja (kui nimi puudub, kasutame SteamID-d)

        salvesta_kasutajad(kasutajad)
        # Salvestame muudatused faili

    else:
        # Kui kasutaja on juba olemas

        if nimi and kasutajad[steamid].get("nimi") != nimi:
            # Kui nimi on antud ja see erineb salvestatud nimest

            kasutajad[steamid]["nimi"] = nimi
            # Uuendame kasutaja nime

            salvesta_kasutajad(kasutajad)
            # Salvestame muudatused faili

    return kasutajad[steamid]
    # Tagastame leitud või lisatud kasutaja andmed
