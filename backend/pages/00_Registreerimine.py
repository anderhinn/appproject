import streamlit as st
import time
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from auth import steam_login

st.title("Registreerimine")
url=st.text_input("Sisesta oma Steam lingi või ID:")

if st.button("Logi sisse"):
    if not url.strip():
        st.error("Palun sisesta kehtiv Steam link või ID.")
    else:
        try:
            info= steam_login.registreeri_kasutaja(url.strip())
            steamid= info["steamid"]
            nimi= info["personame"]

            st.session_state["user_id"]= steamid
            st.session_state["username"]= nimi
            st.success(f"Tere, {nimi}! Oled edukalt sisse logitud.")
            time.sleep(2)

            st.switch_page("pages/01_Mangud.py")
        except Exception as e:
            st.error(f"Sisselogimine nurjus: {e}")
    