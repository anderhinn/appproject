import streamlit as st
from dotenv import load_dotenv
from auth.steam_login import saame_nimi_steamidst, saame_steamid
load_dotenv()

#Projekt Fano
#Rakenduse nimi: OnlyGamers
#Autorid: Ander Hinn, Milena Nikishina
#Allikatest praegu on kasutatud RAWG API (https://rawg.io/apidocs); Streamlit (https://streamlit.io) ja Claude AI (https://claude.ai) vigade leidmiseks.

#Rakenduse avaleht
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

steam_input= st.session_state.get("user_id")

if not steam_input:
    st.error("Steam link puudub. Palun logi sisse.")
    st.stop()

steamid=saame_steamid(steam_input)
info= saame_nimi_steamidst(steamid)
nimi=info["personame"]


st.title(f'Tere tulemast, {nimi}!')




#Streamlit sessiooni seisundi kasutamine valitud kategooria salvestamiseks
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None

with st.container():
    _, mid, _ = st.columns([3, 2, 3])
    with mid:
        if st.button("Vali kategooria 🎮", use_container_width=True):
            st.switch_page("pages/01_Mangud.py")
