import streamlit as st
import sys
from pathlib import Path

backend_path= Path(__file__).resolve().parent.parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

import firebase_api as fb

st.set_page_config(page_title="Tiimikaaslaste otsing", page_icon="🕹️", layout="centered")
st.title("Tiimikaaslaste otsing")

current_user= st.session_state.get("user_id")
if not current_user:
    st.info("Palun logige sisse, et otsida tiimikaaslasi.")
    st.stop()

default_game_id= st.session_state.get("lfg_game_id", "")
default_game_name= st.session_state.get("lfg_game_name", "")

game_id= st.text_input("game_id", value=default_game_id, placeholder="Sisesta mängu ID (RAWG või slug)")
game_name= st.text_input("game_name", value=default_game_name, placeholder="Nt: Apex Legends")

col1, col2= st.columns([1, 1])
with col1:
    load_btn= st.button("Lae nimekiri")
with col2:
    back_btn= st.button("Tagasi mängude lehele")

if back_btn:
    st.switch_page("pages/01_Mangud.py")

if not load_btn and not st.session_state.get("auto_load_lfg"):
    st.caption("Vali game_id ja vajuta 'Lae nimekiri'")


entries= []
if load_btn or st.session_state.get("auto_load_lfg"):
    st.session_state["auto_load_lfg"]= False
    if not game_id.strip():
        st.warning("Palun sisesta mängu ID.")
        st.stop()

    try:
        entries= fb.get_lfg_by_game(game_id.strip())
        st.session_state["last_entries"] = entries
    except Exception as e:
        st.error(f"Tiimikaaslaste nimekirja laadimine nurjus: {e}")
        st.stop()
    st.caption(f"Leitud: {len(entries)}")


entries=st.session_state.get("last_entries", entries)
if entries:
    entries.sort(key= lambda x: x.get("timestamp", 0), reverse= True)
    for e in entries:
        user_id= e.get("user_id")
        username= e.get("username", "Tundmatu kasutaja")
        note= e.get("note", "")
        timestamp= e.get("timestamp", "")
        lfg_id= e.get("id", "")

        if not user_id or user_id == current_user:
            continue

        with st.container(border=True):
            st.write(f"**User:** {username} (`{user_id}`)")
            if str(game_name).strip():
                st.write(f"**Game:** {str(game_name).strip()} (`{game_id}`)")
            else:
                st.write(f"**Game ID:** `{game_id}`")
            if note:
                st.write(f"**Note:** {note}")
            if timestamp:
                st.caption(f"timestamp: {timestamp}")

            if st.button("Ava chat", key=f"chatbtn_{lfg_id}"):
                st.write("DEBUG")
                st.session_state["chat_partner_id"]= user_id
                st.session_state["chat_game_id"]= str(game_id).strip()
                st.session_state["chat_game_name"]= str(game_name).strip()
                st.query_params.update(open="chat")
                st.switch_page("pages/04_Chat.py")
                st.rerun()
else:
    st.info("Hetkel pole tiimikaaslasi selle mängu jaoks.")
                
        