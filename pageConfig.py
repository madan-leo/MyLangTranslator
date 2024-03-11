import streamlit as st

# For browser bar - title, logo etc. & to keep side bar expanded
def pageconfig():
    st.set_page_config(
        page_title="GLOT - Translation Service",
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
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.markdown("<h5 style='text-align: left; color: white;'>Pick a Translation Service</h5>", unsafe_allow_html=True)
    st.sidebar.selectbox("Pick a Translation Service",('Bing Translate','Google Translate','DeepL'))

# Set Main Page config
def mainpageconfig():
    st.markdown("""
        <style>
        .stTextArea [data-baseweb=base-input] {
            background-color: #F2F2F2;
            -webkit-text-fill-color: black;
        }
    
        .stTextArea [data-baseweb=base-input] [disabled=""]{
            background-color: #F2F2F2;
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
