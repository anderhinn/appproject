import json
import requests

api_key= 'FD4452975543211A9F52DBA03A76627D'
steam_id= '76561199229065635'
url= f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steam_id}'


def lae():
    f= open('kasutajad.json', 'r', encoding='utf-8')
    sisu= f.read().strip()
    
    f.close()
    
    if not sisu:
        return {}
    
    andmed=json.load(f)
    return andmed

def salvestame(andmed):
    f= open('kasutajad.json', 'w', encoding='utf-8')
    json.dump(andmed, f, indent=4, ensure_ascii=False)
    f.close()

def saame_id_urlist(url):
    url=url.strip()
    if '/profiles/' in url:
        return url.split('/profiles/')[1].strip('/')
    if '/id/' in url:
        return url.split('/id/')[1].strip('/')
    
def saame_id_nimist(id):
    url=f'https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key={api_key}&vanityurl={id}'
    response= requests.get(url)
    andmed= response.json()
    steamid= andmed['response']['steamid']
    return steamid

    
def saame_nimi_steamidst(steamid):
    url=f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steamid}'
    response= requests.get(url)
    andmed= response.json()
    asukoht= andmed['response']['players']
    nimi=asukoht[0]['personaname']
    kasutajad=lae()
    kasutajad[nimi]= steamid
    salvestame(kasutajad)
    return nimi


    



url=input('Sisesta Steam profiili aadress: ')
id= saame_id_urlist(url)
print(id)
steamid= saame_id_nimist(id)
nimi= saame_nimi_steamidst(steamid)
print(nimi)

