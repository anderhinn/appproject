import streamlit as st

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



st.title('Valige kategooriad')

with st.container(border=True):
    st.subheader('Tulistamismängud')
    st.write('Otsib: ')
    clicked1= st.button('Otsi', key='otsing_1')
    
with st.container(border=True):
    st.subheader('Mälurimängud')
    st.write('Otsib: ')
    clicked2= st.button('Otsi', key= 'otsing_2')
    
with st.container(border=True):
    st.subheader('Seiklusmängud')
    st.write('Otsib: ')
    clicked3= st.button('Otsi', key='otsing_3')

with st.container(border=True):
    st.subheader('Strateegiamängud')
    st.write('Otsib: ')
    clicked3= st.button('Otsi', key='otsing_4')

with st.container(border=True):
    st.subheader('Spordimängud')
    st.write('Otsib: ')
    clicked3= st.button('Otsi', key='otsing_5')

with st.container(border=True):
    st.subheader('Õudusmängud')
    st.write('Otsib: ')
    clicked3= st.button('Otsi', key='otsing_6')

with st.container(border=True):
    st.subheader('Simulaatorid')
    st.write('Otsib: ')
    clicked3= st.button('Otsi', key='otsing_7')

with st.container(border=True):
    st.subheader('MMO-mängud')
    st.write('Otsib: ')
    clicked3= st.button('Otsi', key='otsing_8')

with st.container(border=True):
    st.subheader('Liivakastimängud')
    st.write('Otsib: ')
    clicked3= st.button('Otsi', key='otsing_9')

with st.container(border=True):
    st.subheader('Ellujäämismängud')
    st.write('Otsib: ')
    clicked3= st.button('Otsi', key='otsing_10')
