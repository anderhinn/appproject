import streamlit as st
from dotenv import load_dotenv
from auth.steam_login import saame_nimi_steamidst, saame_steamid
#Laeme .env faili
load_dotenv()

#Projekt Fano
#Rakenduse nimi: OnlyGamers
#Autorid: Ander Hinn, Milena Nikishina
#Allikatest praegu on kasutatud RAWG API (https://rawg.io/apidocs); Streamlit (https://streamlit.io) ja Claude AI (https://claude.ai) vigade leidmiseks.

#lihtne css
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

#võtame steam kasutaja id sessioonist
steam_input= st.session_state.get("user_id")

#kui kasutaja pole sisse logitud, peatame lehte
if not steam_input:
    st.error("Steam link puudub. Palun logi sisse.")
    st.stop()

#teisendame sisendi steamid-ks
steamid=saame_steamid(steam_input)
#küsime steam API-st kasutaja info
info= saame_nimi_steamidst(steamid)
#võtame kasutaja steam nickname
nimi=info["personame"]

#tervitus koos nimega
st.title(f'Tere tulemast, {nimi}!')




#Kui kategooriat pole veel salvestatud, loome võtme
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None

#keskendatud nupp kategooriate lehele liikumiseks
with st.container():
    _, mid, _ = st.columns([3, 2, 3])
    with mid:
        if st.button("Vali kategooria 🎮", use_container_width=True):
            st.switch_page("pages/01_Mangud.py")
