import streamlit as st
import sys
from pathlib import Path

backend_path= Path(__file__).resolve().parent.parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

import firebase_api as fb

def make_chat_id(user_id_1:str, user_id_2:str) ->str:

    return "_".join(sorted([user_id_1, user_id_2]))

st.set_page_config(page_title="Chat", page_icon="💬", layout="centered")
st.title("💬Chat")


me_id=st.session_state.get("user_id")
me_name=st.session_state.get("username", "")

other_id=st.session_state.get("chat_partner_id")
game_id=st.session_state.get("chat_game_id", "")
game_name=st.session_state.get("chat_game_name", "")

if not me_id:
    st.error("Palun logige sisse.")
    st.stop()

if not other_id:
    st.error("Chat-partner puudub. Mine tagasi Looking For Group listi ja vali partner.")
    st.stop()

st.caption(f"Mäng: {game_name} ({game_id})")
st.write(f"**Sina**: {me_name} (`{me_id}`)")
st.write(f"**Partner**: `{other_id}`")

chat_id=make_chat_id(me_id, other_id)

col1,col2 = st.columns([1, 1])
with col1:
    if st.button("Tagasi LFG listi"):
        st.switch_page("pages/03_LookingForGroup")

with col2:
    if st.button("Värskenda"):
        st.rerun()

st.divider()

#Messages
st.subheader("Sõnumid")
try:
    messages=fb.get_messages(chat_id)
except Exception as e:
    st.error(f"Sõnumeid ei saanud laadida: {e}")
    messages=[]

if not messages:
    st.info("Sõnumeid veel pole. Make the first step!")
else:
    for m in messages:
        sender_id=m.get("sender_id")
        text=m.get("text", "")
        timestamp=m.get("timestamp", "")

        if sender_id==me_id:
            st.write(f"Sina: {text}")
        else:
            st.write(f"{sender_id}: {text}")
        if timestamp:
            st.caption(f"{timestamp}")

st.divider()

st.subheader("Saada sõnum")
new_text=st.chat_input("Kirjuta sõnum")

if new_text:
    try:
        fb.send_message(chat_id, me_id, new_text.strip())
        st.rerun()
    except Exception as e:
        st.error(f"Sõnumi saatmine ebaõnnestus: {e}")