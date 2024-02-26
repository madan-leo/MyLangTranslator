import streamlit as st
# For browser bar - title, logo etc. & to keep side bar expanded
def pageconfig():
    st.set_page_config(
        page_title="GetTranslate",
        page_icon="icon.jpg",
        layout="wide",
        initial_sidebar_state="expanded"
    )
# Set sidebar logo and color
def sidebarconfig():
    st.sidebar.image("logo.jpg", width=250)
    st.markdown("""
    <style>
        [data-testid=stSidebar] {
            background-color: #19274A;
        }
    </style>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("<h2 style='text-align: left; color: white;'>Translation App</h2>", unsafe_allow_html=True)
    #st.sidebar.markdown("<h6 style='text-align: left; color: white;'>App to translate text and documents</h6>", unsafe_allow_html=True)
    st.sidebar.selectbox("Pick a Translation Service",('Bing Translate','Google Translate','DeepL'))

# Set Main Page config
def mainpageconfig():
    st.markdown("""
        <style>
        .stTextArea [data-baseweb=base-input] {
            background-color: #CFCFCF;
            -webkit-text-fill-color: black;
        }
    
        .stTextArea [data-baseweb=base-input] [disabled=""]{
            background-color: #CFCFCF;
            -webkit-text-fill-color: black;
        }
        div.stButton > button:first-child {
            background-color: #19274A;
            -webkit-text-fill-color: white;
        }
        .stSelectbox:first-of-type > div[data-baseweb="select"] > div {
            background-color: #CFCFCF;
            adding: 0px;
        }
        [data-testid='stFileUploader'] {
            background-color: #CFCFCF;
            width: max-content;
        }
        </style>
    """,unsafe_allow_html=True)
