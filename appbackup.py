import streamlit as st
import pageConfig as PC
import translation_apis as my_api
from azure.storage.blob import BlobServiceClient
import tempfile
import os
import time
from pathlib import Path
import LogTable as AzTable
import pandas as pd
from sqlalchemy import create_engine
from azure.data.tables import TableClient

# Set Page layouts and colors
PC.pageconfig()
PC.sidebarconfig()
PC.mainpageconfig()

# Declare session state variable
if "totranslate" not in st.session_state:
    st.session_state.totranslate = []
if "detlang" not in st.session_state:
    st.session_state.detlang = []
if "tolanguage" not in st.session_state:
    st.session_state.tolanguage = []
if "dtolanguage" not in st.session_state:
    st.session_state.dtolanguage = []
if "displayoutput" not in st.session_state:
    st.session_state.displayoutput = []
if "download_btn" not in st.session_state:
    st.session_state.download_btn = ""
if "filename" not in st.session_state:
    st.session_state.filename = ""
if "translation_status" not in st.session_state:
    st.session_state.translation_status = ""

tab1,tab2,tab3 = st.tabs(["**Translate Text**","**Translate Documents**","**History**"])

# Tab 1 for text translations
with tab1:
    col1, col2, col3 = st.columns([0.45,0.1,0.45])
    with col2:
        st.markdown(2*"<br />", unsafe_allow_html=True)
        btntranslate = st.button("Translate")
    # Call text translation api, and display output
    if btntranslate:
        output = my_api.texttranslator_api(st.session_state.totranslate, st.session_state.tolanguage)
        st.session_state.displayoutput = output[0]["translations"][0]["text"]
        st.session_state.detlang = output[0]["detectedLanguage"]["language"]

        # Create row in Azure table as audit trial
        AzTable.connect_azure_table()
        AzTable.create_entity("Text","madan.jalari",st.session_state.detlang,st.session_state.tolanguage,st.session_state.totranslate,st.session_state.displayoutput,"","")

    # Display each column: This code runs every time an action happens on UI, so store the variable in session state
    with col1:
        st.session_state.totranslate = st.text_area("***Text to Translate***", placeholder="Enter Text Here...")
        st.write("Detected Language: ")
        st.write(st.session_state.detlang)
    with col3:
        translated = st.text_area("***Translated Text***", st.session_state.displayoutput, disabled=True)
        st.session_state.tolanguage = st.selectbox('To Language', ('', 'ar','en', 'es', 'fr', 'hi', 'it','ja','ko','pt','sv','ta','te','yue'))

# Tab 2 for Document translations
with tab2:
    dcol1, dcol2, dcol3 = st.columns([0.4,0.2,0.4])
    with dcol1:
        file = st.file_uploader("Pick a file to translate")#,accept_multiple_files=True)
    with dcol2:
        st.markdown("<br />", unsafe_allow_html=True)
        doc_btntranslate = st.button("Translate Document")

    # When Translate button is clicked
    if doc_btntranslate:
        # Write uploaded file to a temp directory, and retrieve path
        st.session_state.filename = file.name.split('.')[0] + file.file_id + "." + file.name.split('.')[1]
        temp_dir = tempfile.mkdtemp()
        path = os.path.join(temp_dir,st.session_state.filename)
        with open(path, "wb") as f:
            f.write(file.getvalue())

        # Upload blob to the Azure container, into Original files folder
        account_url="https://mjstorageaccount1980.blob.core.windows.net/?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2025-02-16T05:28:50Z&st=2024-02-15T21:28:50Z&spr=https,http&sig=zRsJZQKojcLl1TkxGTevgF%2FL4YqC2eSgHyDJx%2BX%2Fkus%3D"
        container_name = "original-files"
        blob_service_client = BlobServiceClient(account_url=account_url)
        container_client=blob_service_client.get_container_client(container= container_name)
        with open(path,mode="rb") as f:
            container_client.upload_blob(name=st.session_state.filename, data=f)

        # Call document translation API, and write output to Translated container
        resp = my_api.doctranslation_api(st.session_state.filename,st.session_state.dtolanguage)
        with dcol3:
            with st.spinner('Translation in Progress'):
                time.sleep(20)
        st.session_state.translation_status = "Translated"

        # Write a Audit log into Azure tables
        AzTable.connect_azure_table()
        AzTable.create_entity("Document","madan.jalari","Auto",st.session_state.dtolanguage,"","",st.session_state.filename,st.session_state.filename)

    # When Download translation button is clicked. This is displayed based on transaltion_status session state set while displaying columns data
    if st.session_state.download_btn:
        # Connect to translated-files container via SAS url
        daccount_url = "https://mjstorageaccount1980.blob.core.windows.net/?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2025-02-16T05:28:50Z&st=2024-02-15T21:28:50Z&spr=https,http&sig=zRsJZQKojcLl1TkxGTevgF%2FL4YqC2eSgHyDJx%2BX%2Fkus%3D"
        translated_container_name = "translated-files"
        blob_client = BlobServiceClient(account_url=daccount_url)
        dcontainer_client = blob_client.get_blob_client(container=translated_container_name, blob=st.session_state.filename)
        # Get local downloads folder
        downloads_path = str(Path.home() / "Downloads")
        downloadedfile = os.path.join(downloads_path, st.session_state.filename)
        # Retrieve blob from container and write to local download folder
        with open(downloadedfile, mode="wb") as sample_blob:
            download_stream = dcontainer_client.download_blob()
            sample_blob.write(download_stream.readall())
        st.session_state.translation_status = "Download Complete"

    # Display columns. This script runs everytime there is an action on UI
    # Before translation display first if condition, after translation next condition to display download button
    # After download translation is clicked go through last condition. Its all controlled by session state translation_status
    with dcol3:
        if not st.session_state.translation_status:
            st.markdown("<br />", unsafe_allow_html=True)
            st.write("Translation not started")
            st.session_state.dtolanguage = st.selectbox('Doc To Language', ('', 'ar', 'en', 'es', 'fr', 'hi', 'it', 'ja', 'ko', 'pt', 'sv', 'ta', 'te', 'yue'))
        elif st.session_state.translation_status=="Translated":
            st.markdown("<br />", unsafe_allow_html=True)
            st.session_state.download_btn = st.button("Download Translation")
            st.session_state.dtolanguage = st.selectbox('Doc To Language', ('', 'ar', 'en', 'es', 'fr', 'hi', 'it', 'ja', 'ko', 'pt', 'sv', 'ta', 'te', 'yue'))
        elif st.session_state.translation_status == "Download Complete":
            st.markdown("<br />", unsafe_allow_html=True)
            st.write("Download Complete")
            st.session_state.dtolanguage = st.selectbox('Doc To Language', ('', 'ar', 'en', 'es', 'fr', 'hi', 'it', 'ja', 'ko', 'pt', 'sv', 'ta', 'te', 'yue'))

# Tab 3 to display all history of translations for the user
with tab3:
    my_filter = "User eq 'madan.jalari'"
    table_client = TableClient.from_connection_string(conn_str="DefaultEndpointsProtocol=https;AccountName=mjstorageaccount1980;AccountKey=bF+CK6B6ZyeIWUJkEEHxP4FxARHQqYDYxlDn9ukVnADisezX1vtIu/u4ZbqO5iugPkUG2N7zwB6C+ASti7ycVw==;EndpointSuffix=core.windows.net",table_name="translationaudit")
    entities = table_client.query_entities(my_filter)
    df = pd.DataFrame(entities).sort_values(by=["RowKey"],ascending=False)
    st.write(df)