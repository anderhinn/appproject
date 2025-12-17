import streamlit as st
import sys
from pathlib import Path
#Taustamustri URL (tulevikuks)
PATTERN_URL = "https://www.transparenttextures.com/patterns/xv.png"

#Lihtne css
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

#Lisame backend kausta sys.pathi, et saaksime
#importida firebase_api ka pages/ kaustast
backend_path= Path(__file__).resolve().parent.parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

#Firebase funktsioonid (chat ja sõnumid)
import firebase_api as fb

#Loob kahele kasutajale ühise chat_id, sorted tagab
#et järjekord on alati sama (user1 ja user2 chat ei ole sama, mis user2 ja user1)
def make_chat_id(user_id_1:str, user_id_2:str) ->str:

    return "_".join(sorted([user_id_1, user_id_2]))

#Lehe seadistus
st.set_page_config(page_title="Chat", page_icon="💬", layout="centered")
st.title("💬Chat")

#Sisseloginud kasutaja andmes sessioonist
me_id=st.session_state.get("user_id")
me_name=st.session_state.get("username", "")

#Partneri ja mängu info (võtame lfg lehelt)
other_id=st.session_state.get("chat_partner_id")
game_id=st.session_state.get("chat_game_id", "")
game_name=st.session_state.get("chat_game_name", "")

#Kui kasutaja pole sisse logitud = no chatting
if not me_id:
    st.error("Palun logige sisse.")
    st.stop()

#kui partnerit pole valitud = no chatting
if not other_id:
    st.error("Chat-partner puudub. Mine tagasi Looking For Group listi ja vali partner.")
    st.stop()

#Kuvame chati ülaosas info mängu, kasutaja ja partneri kohta
st.caption(f"Mäng: {game_name} ({game_id})")
st.write(f"**Sina**: {me_name} (`{me_id}`)")
st.write(f"**Partner**: `{other_id}`")

#Arvutame konkreetse vestluse chat_id
chat_id=make_chat_id(me_id, other_id)

#Nupud tagasi ja värskenda
col1,col2 = st.columns([1, 1])
with col1:
    if st.button("Tagasi LFG listi"):
        st.switch_page("pages/03_LookingForGroup.py")

with col2:
    if st.button("Värskenda"):
        st.rerun()

st.divider()

#Messages plokk
st.subheader("Sõnumid")
try:
    #Laeme kõik sõnumid selle chat_id jaoks Firebase'ist
    messages=fb.get_messages(chat_id)
except Exception as e:
    st.error(f"Sõnumeid ei saanud laadida: {e}")
    messages=[]

#Kui sõnumeid pole = motiveerime
if not messages:
    st.info("Sõnumeid veel pole. Make the first step!")
else:
    #Kuvame kõik sõnumid järjest
    for m in messages:
        sender_id=m.get("sender_id")
        text=m.get("text", "")
        timestamp=m.get("timestamp", "")

        #Eraldi vormistus, minu vs partneri sõnum
        if sender_id==me_id:
            st.write(f"Sina: {text}")
        else:
            st.write(f"{sender_id}: {text}")
        if timestamp:
            st.caption(f"{timestamp}")

st.divider()

#Sõnumi saatmine
st.subheader("Saada sõnum")
#Chatile sobiv sisestusväli (enter=saada)
new_text=st.chat_input("Kirjuta sõnum")

#Kui kasutaja sisestas sõnumi
if new_text:
    try:
        #salvestame sõnum firebase'i
        fb.send_message(chat_id, me_id, new_text.strip())
        #Värskendame lehte, et sõnum ilmuks kohe
        st.rerun()
    except Exception as e:
        st.error(f"Sõnumi saatmine ebaõnnestus: {e}")