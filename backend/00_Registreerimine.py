import streamlit as st
import time
import sys
from pathlib import Path
# Impordime Steamiga sisselogimise loogika
from auth import steam_login
from auth.users import leia_voi_lisa_kasutaja

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

# Lisame Pythonile kausta tee ühe taseme võrra ülespoole,
# et ta leiaks kausta "auth" ja faili "steam_login.py"
sys.path.append(str(Path(__file__).parent.parent))


# Lehe pealkiri Streamlitis
st.title("Registreerimine")

# Tekstiväli, kuhu kasutaja sisestab oma Steam lingi või Steam ID
url = st.text_input("Sisesta oma Steam lingi või ID:")



# Nupp "Logi sisse"
if st.button("Logi sisse"):
    
    # Kontroll: kui kasutaja ei sisestanud midagi (või ainult tühikud)
    if not url.strip():
        # Näitame veateadet
        st.error("Palun sisesta kehtiv Steam link või ID.")
    else:
        try:
            # Kutsume välja funktsiooni, mis tegeleb
            # Steam ID leidmise ja kasutaja registreerimisega
            info = steam_login.registreeri_kasutaja(url.strip())

            # Võtame vastusest Steam kasutaja unikaalse ID
            steamid = info["steamid"]

            # Võtame vastusest Steam kasutajanime
            nimi = info["personame"]

            leia_voi_lisa_kasutaja(nimi, steamid)

            # Salvestame Steam ID sessiooni,
            # et seda saaks kasutada teistel lehtedel
            st.session_state["user_id"] = steamid

            # Salvestame kasutajanime sessiooni
            st.session_state["username"] = nimi

            # Näitame eduteadet
            st.success(f"Tere, {nimi}! Oled edukalt sisse logitud.")

            # Väike paus (kasutaja näeb teadet)
            time.sleep(2)

            # Suuname kasutaja edasi mängude lehele
            st.switch_page("pages/app.py")


        except Exception as e:
            # Kui tekib ükskõik milline viga (API, link, võtmed jne),
            # näitame veateadet kasutajale
            st.error(f"Sisselogimine nurjus: {e}")

    