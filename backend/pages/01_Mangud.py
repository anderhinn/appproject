import streamlit as st
import re
import sys
from pathlib import Path

#Lisame backend kataloogi sys.path-i (igaks juhuks, enne rawg_api'ga esines probleeme), et importimine töötaks korrektselt
backend_path = Path(__file__).resolve().parent.parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

import rawg_api as rawg

#Lehe seadistamine ja pealkiri
st.set_page_config(page_title="Mängud", page_icon="🎮", layout="centered")
st.title("Valitud kategooria mängud")

st.markdown("""
<style>
h1 {color: #ACEC00 !important; text-align: center; white-space:pre-line}
p {color: #8CE600 !important;}
</style>
""", unsafe_allow_html=True)

#Kategooriate kaardistus RAWG API žanridele
CAT_MAP = {
    "Tulistamismängud": "shooter",
    "Mälurimängud": "puzzle",
    "Seiklusmängud": "adventure",
    "Strateegiamängud": "strategy",
    "Spordimängud": "sports",
    "Õudusmängud": "horror",
    "Simulaatorid": "simulation",
    "MMO-mängud": "massively-multiplayer",
    "Liivakastimängud": "sandbox",
    "Ellujäämismängud": "survival",
}

params = st.query_params
estonian_cat = (params.get("cat") or "").strip() #Kategooria eesti keeles
page=int(params.get("page") or 1) #Lehe number

#Kui kategooria puudub, palume kasutajal valida kategooria samal leheküljel
if not estonian_cat or estonian_cat not in CAT_MAP:
    st.info("Valitud kategooria puudub. Palun valige kategooria eelmises lehes.")
    estonian_cat=st.selectbox("Vali kategooria:", list(CAT_MAP.keys()))
    if not estonian_cat:
        st.stop()

#Nupud
left, _, right=st.columns([1,4,1])
with left:
    if st.button("Eelnev leht"):
        st.switch_page("app.py")

st.caption(f"Valitud kategooria: **{estonian_cat}** (leht {page})")

genre_slug = CAT_MAP.get(estonian_cat)

#Kui žanr on kehtiv, küsime mängud RAWG API-st
if genre_slug:
    games=rawg.get_games_by_genre(genre_slug, page=page, page_size=10)
    if not games:
        st.info("Selles kategoorias mänge ei leitud. Lisame need varsti!")
        if st.button("Tagasi"):
            st.switch_page("app.py")
        st.stop()
else:
    st.error("Tundmatu kategooria.")
    st.stop()

#Iga mängu kaardi kuvamine: nimi, pilt, release date, rating ja lühikirjeldus
for game in games:
    with st.container(border=True):
        st.subheader(game.get("name", ""))
        if game.get("background_image"):
            st.image(game["background_image"], width="stretch")
        
        meta=[]
        if game.get("rating") is not None:
            meta.append(f"Rating: {game['rating']}")
        if game.get("released"):
            meta.append(f"Released: {game['released']}")
        if meta:
            st.write(" | ".join(meta))

        #detailipäring    
        try:
            details = rawg.get_game_details(int(game["id"]))
            description = (details.get("description_raw") or "").strip()
            if description:
                #eemaldame HTML sildid ja kuvame 1500 tähemärki (enne oli 600, mida jäi väheks, aga ikkagi on mänge, kus ei piisa isegi 1700 tähemärgist. Lähitulevikus võiks expanderi lisada)
                description=re.sub(r"<.*?>", "", description).strip()
                st.write(description[:1500] + ("..." if len(description) > 1500 else ""))
        except Exception as e:
            pass
        #see koht hetkel ei tööta korralikult, kuna leht 02_GameInfo.py on arendamisel
        if st.button("Otsi", key=f"otsi_{game['id']}"):
            st.query_params.update(cat=estonian_cat, game_id=game['id'])
            st.switch_page("pages/02_GameInfo.py")

with right:
    if st.button("Järgmine leht"):
        st.query_params.update(cat=estonian_cat, page=str(page + 1))
        st.rerun()