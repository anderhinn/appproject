import streamlit as st
import requests
import json

api_key= 'FD4452975543211A9F52DBA03A76627D'
steam_id= '76561199229065635'
url= f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steam_id}'


def lae():
    try:
        f= open(fail, 'r', encoding='utf-8')
        sisu= f.read().strip()
    
    
        if not sisu:
            return {}
        
        
        return json.loads(sisu)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def salvestame(andmed):
    f= open(fail, 'w', encoding='utf-8')
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

#------------------------------------------

fail='auth/kasutajad.json'
st.title('Registreerimine')


url=st.text_input('Sisesta oma Steam lingi:')



if st.button('Logi sisse'):
    if not url.strip():
        st.error('Sisestage lingi!')
    else:
        id= saame_id_urlist(url)
        if id.isdigit():
            steamid=id
        else:
            steamid= saame_id_nimist(id)
            if steamid is None:
                st.error('Ei leidnud kasutajat!')
            else:
                nimi= saame_nimi_steamidst(steamid)
                st.success(f'Tere Tulemast {nimi}')
                andmed=lae()
                
                if nimi in andmed:
                    st.switch_page('pages/01_Mangud.py')
        

