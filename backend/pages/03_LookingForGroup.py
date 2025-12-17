import streamlit as st
import sys
from pathlib import Path

#Lihtne stiil
st.markdown('''
<style>

h1 {
    
    color: #ACEC00 !important;
    text-align: center;
}
p {
    color: #BCEC00 !important;
    }

</style>
''', unsafe_allow_html= True)

#Lisame backend kausta sys.pathi, et firebase_api import töötaks
backend_path= Path(__file__).resolve().parent.parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

import firebase_api as fb #Firebase LFG funktsioonid

#Lehe seadistused ja pealkiri
st.set_page_config(page_title="Tiimikaaslaste otsing", page_icon="🕹️", layout="centered")
st.title("Tiimikaaslaste otsing")

#Praegune kasutaja sessionist (steamid)
current_user= st.session_state.get("user_id")
if not current_user:
    st.info("Palun logige sisse, et otsida tiimikaaslasi.")
    st.stop()

#vaikimisi mängu info (tuleb Mängude lehelt session_state kaudu)
default_game_id= st.session_state.get("lfg_game_id", "")
default_game_name= st.session_state.get("lfg_game_name", "")

#mängu id ja nimi
game_id= st.text_input("game_id", value=default_game_id, placeholder="Sisesta mängu ID (RAWG või slug)")
game_name= st.text_input("game_name", value=default_game_name, placeholder="Nt: Apex Legends")

#Nupud lae nimekiri ja tagasi
col1, col2= st.columns([1, 1])
with col1:
    load_btn= st.button("Lae nimekiri")
with col2:
    back_btn= st.button("Tagasi mängude lehele")

#Nupp tagasi
if back_btn:
    st.switch_page("pages/01_Mangud.py")

#Vihje, kui nimekirja ei laeta automaatselt
if not load_btn and not st.session_state.get("auto_load_lfg"):
    st.caption("Vali game_id ja vajuta 'Lae nimekiri'")

#Laetud tulemused (lfg kirjed)
entries= []

#Laeme andmed kas nupuga või automaatselt (auto_load_lfg)
if load_btn or st.session_state.get("auto_load_lfg"):
    st.session_state["auto_load_lfg"]= False
    #Kontroll, gameid peaks olemas olema
    if not game_id.strip():
        st.warning("Palun sisesta mängu ID.")
        st.stop()

    #Firebase päring, toome kõik LFG kirjed selle gameid jaoks
    try:
        entries= fb.get_lfg_by_game(game_id.strip())
        st.session_state["last_entries"] = entries
    except Exception as e:
        st.error(f"Tiimikaaslaste nimekirja laadimine nurjus: {e}")
        st.stop()
    st.caption(f"Leitud: {len(entries)}")

#Kui midagi ei laaditud, kasutame viimati laetud entries
entries=st.session_state.get("last_entries", entries)
#Kuvame nimekirja, kui kirjeid on
if entries:
    #Sorteerime uuemad ette
    entries.sort(key= lambda x: x.get("timestamp", 0), reverse= True)
    for e in entries:
        #Loeme kirje väljad
        user_id= e.get("user_id")
        username= e.get("username", "Tundmatu kasutaja")
        note= e.get("note", "")
        timestamp= e.get("timestamp", "")
        lfg_id= e.get("id", "")

        #Ei kuva iseennast ega vigast kirjet
        if not user_id or user_id == current_user:
            continue

        #Kasutaja kaart
        with st.container(border=True):
            st.write(f"**User:** {username} (`{user_id}`)")
            #Kuvame mängu nime, kui see on olemas
            if str(game_name).strip():
                st.write(f"**Game:** {str(game_name).strip()} (`{game_id}`)")
            else:
                st.write(f"**Game ID:** `{game_id}`")
            #Kasutaja märkus
            if note:
                st.write(f"**Note:** {note}")
            #Aeg
            if timestamp:
                st.caption(f"timestamp: {timestamp}")

            #Ava chat, salvestame partneri session_state sisse ja liigume chat lehele
            if st.button("Ava chat", key=f"chatbtn_{lfg_id}"):
                st.session_state["chat_partner_id"]= user_id
                st.session_state["chat_game_id"]= str(game_id).strip()
                st.session_state["chat_game_name"]= str(game_name).strip()
                st.switch_page("pages/04_Chat.py")
                st.rerun()
else:
    st.info("Hetkel pole tiimikaaslasi selle mängu jaoks.")
                
        