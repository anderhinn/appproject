import streamlit as st

#Rakenduse avaleht
st.markdown('''
<style>
h1 {
    color: #ACEC00 !important;
    text-align: center;
    white-space:pre-line
}
p {
    color: #BCEC00 !important;
    }

</style>
''', unsafe_allow_html= True)



st.title('Valige kategooriad')

categories = [
    "Tulistamismängud",
    "Mälurimängud",
    "Seiklusmängud",
    "Strateegiamängud",
    "Spordimängud",
    "Õudusmängud",
    "Simulaatorid",
    "MMO-mängud",
    "Liivakastimängud",
    "Ellujäämismängud",
]

#Streamlit sessiooni seisundi kasutamine valitud kategooria salvestamiseks
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None

for i, cat in enumerate(categories, start=1):
    with st.container(border=True):
        st.subheader(cat)
        st.write(f"Otsib:")
        if st.button("Otsi", key=f"otsing_{i}"):
            st.session_state.selected_category = cat
            st.query_params.update(cat=cat, page="1")
            st.switch_page("pages/01_Mangud.py")