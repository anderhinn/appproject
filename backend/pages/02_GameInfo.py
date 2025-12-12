import streamlit as st
import rawg_api as rawg

#Lehe seadistus
st.set_page_config(page_title="Mängu info", page_icon="🎲", layout="centered")
st.title("Mängu info")

#Developing in progrress, hetkel see leht ei tööta korrektselt
st.caption("Developing in progress...")

params = st.query_params
game_id = params.get("game_id")
category = params.get("cat", "")

#Mängu ID puudub - pakume tagasi minna mängude lehele
if not game_id:
    st.info("Mängu ID puudub. Palun valige mäng eelmises lehes.")
    if st.button("Tagasi"):
        st.switch_page("pages/01_Mangud.py")
    st.stop()

#Errorite käsitlemine
try:
    details = rawg.get_game_details(int(game_id))
    
    if not details:
        st.error("Mängu andmeid ei leitud.")
        st.stop()
    
    st.header(details.get("name", ""))
    
    if details.get("background_image"):
        st.image(details["background_image"], caption=details.get("name", ""), width="stretch")
    
    #Release info, rating ja metacritic
    info = []
    if details.get("released"):
        info.append(f"**Released:** {details['released']}")
    if details.get("rating"):
        info.append(f"**Rating:** {details['rating']}/5")
    if details.get("metacritic"):
        info.append(f"**Metacritic:** {details['metacritic']}/100")
    if info:
        st.markdown(" | ".join(info))
    
    #Kirjelduse kuvamine, 'description_raw' on lihttekst
    description = (details.get("description_raw") or "").strip()
    if description:
        st.markdown("### Kirjeldus")
        st.markdown(description)
    else:
        st.info("Kirjeldus puudub")
    
    #Lisainfo
    if details.get("genres"):
        genres = ", ".join([g.get("name", "") for g in details["genres"]])
        st.markdown(f"**Žanrid:** {genres}")
    
    if details.get("platforms"):
        platforms = ", ".join([p.get("platform", {}).get("name", "") for p in details["platforms"]])
        st.markdown(f"**Platvormid:** {platforms}")

except ValueError:
    st.error("Vigane mängu ID formaat")
except Exception as e:
    st.error(f"Viga mängu andmete laadimisel: {str(e)}")

#Tagasinupp
if st.button("Tagasi mängude lehele"):
    if category:
        st.query_params.update(cat=category, page="1")
    st.switch_page("pages/01_Mangud.py")