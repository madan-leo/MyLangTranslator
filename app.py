import streamlit as st
import pageConfig as PC
import translation_apis as my_api
import LogTable as LogTable
import tempfile, os, time
from pathlib import Path
import pandas as pd
from azure.data.tables import TableClient
from azure.storage.blob import BlobServiceClient

languageShortcuts = {'Afrikaans': 'af','Albanian': 'sq','Amharic': 'am','Arabic': 'ar','Armenian': 'hy','Assamese': 'as','Azerbaijani (Latin)': 'az','Bangla': 'bn','Bashkir': 'ba','Basque': 'eu','Bosnian (Latin)': 'bs','Bulgarian': 'bg','Cantonese (Traditional)': 'yue','Catalan': 'ca','Chinese (Literary)': 'lzh','Chinese Simplified': 'zh-Hans','Chinese Traditional': 'zh-Hant','Croatian': 'hr','Czech': 'cs','Danish': 'da','Dari': 'prs','Divehi': 'dv','Dutch': 'nl','English': 'en','Estonian': 'et','Faroese': 'fo','Fijian': 'fj','Filipino': 'fil','Finnish': 'fi','French': 'fr','French (Canada)': 'fr-ca','Galician': 'gl','Georgian': 'ka','German': 'de','Greek': 'el','Gujarati': 'gu','Haitian Creole': 'ht','Hebrew': 'he','Hindi': 'hi','Hmong Daw (Latin)': 'mww','Hungarian': 'hu','Icelandic': 'is','Indonesian': 'id','Interlingua': 'ia','Inuinnaqtun': 'ikt','Inuktitut': 'iu','Inuktitut (Latin)': 'iu-Latn','Irish': 'ga','Italian': 'it','Japanese': 'ja','Kannada': 'kn','Kazakh (Cyrillic)': 'kk, kk-cyrl','Kazakh (Latin)': 'kk-latn','Khmer': 'km','Klingon': 'tlh-Latn','Klingon (plqaD)': 'tlh-Piqd','Korean': 'ko','Kurdish (Arabic) (Central)': 'ku-arab,ku','Kurdish (Latin) (Northern)': 'ku-latn, kmr','Kyrgyz (Cyrillic)': 'ky','Lao': 'lo','Latvian': 'lv','Lithuanian': 'lt','Macedonian': 'mk','Malagasy': 'mg','Malay (Latin)': 'ms','Malayalam': 'ml','Maltese': 'mt','Maori': 'mi','Marathi': 'mr','Mongolian (Cyrillic)': 'mn-Cyrl','Mongolian (Traditional)': 'mn-Mong','Myanmar (Burmese)': 'my','Nepali': 'ne','Norwegian': 'nb','Odia': 'or','Pashto': 'ps','Persian': 'fa','Polish': 'pl','Portuguese (Brazil)': 'pt, pt-br','Portuguese (Portugal)': 'pt-pt','Punjabi': 'pa','Queretaro Otomi': 'otq','Romanian': 'ro','Russian': 'ru','Samoan (Latin)': 'sm','Serbian (Cyrillic)': 'sr-Cyrl','Serbian (Latin)': 'sr, sr-latn','Slovak': 'sk','Slovenian': 'sl','Somali': 'so','Spanish': 'es','Swahili (Latin)': 'sw','Swedish': 'sv','Tahitian': 'ty','Tamil': 'ta','Tatar (Latin)': 'tt','Telugu': 'te','Thai': 'th','Tibetan': 'bo','Tigrinya': 'ti','Tongan': 'to','Turkish': 'tr','Turkmen (Latin)': 'tk','Ukrainian': 'uk','Upper Sorbian': 'hsb','Urdu': 'ur','Uyghur (Arabic)': 'ug','Uzbek (Latin)': 'uz','Vietnamese': 'vi','Welsh': 'cy','Yucatec Maya': 'yua','Zulu': 'zu'}
def reverseLanguageLookup(lang):
    for i in languageShortcuts:
        if languageShortcuts[i] == lang:
            return i

# Set Page layouts and colors
PC.pageconfig()
PC.sidebarconfig()
PC.mainpageconfig()

# Declare session state variable
if "totranslate" not in st.session_state:
    st.session_state.totranslate = ""
if "detlang" not in st.session_state:
    st.session_state.detlang = "Auto"
if "tolanguage" not in st.session_state:
    st.session_state.tolanguage = ""
if "dtolanguage" not in st.session_state:
    st.session_state.dtolanguage = ""
if "displayoutput" not in st.session_state:
    st.session_state.displayoutput = ""
if "download_btn" not in st.session_state:
    st.session_state.download_btn = ""
if "filename" not in st.session_state:
    st.session_state.filename = ""
if "translation_status" not in st.session_state:
    st.session_state.translation_status = ""

tab1,tab2,tab3 = st.tabs(["**Translate Text**","**Translate Documents**","**Translation History**"])

# Tab 1 for text translations
with tab1:
    col1, col2, col3 = st.columns([0.45,0.1,0.45])
    with col2:
       st.markdown(2 * "<br/>", unsafe_allow_html=True)
       btntranslate = st.button("Translate")
    # If Translate Text button is clicked, call text translation api and display output
    if btntranslate:
        if st.session_state.tolanguage and st.session_state.totranslate:
            output = my_api.texttranslator_api(st.session_state.totranslate, languageShortcuts.get(st.session_state.tolanguage))
            st.session_state.displayoutput = output[0]["translations"][0]["text"]
            st.session_state.detlang = reverseLanguageLookup(output[0]["detectedLanguage"]["language"])

            # Create row in Azure table as audit trial
            LogTable.connect_azure_table()
            LogTable.create_entity("Text","madan.jalari",st.session_state.detlang,st.session_state.tolanguage,st.session_state.totranslate,st.session_state.displayoutput,"","")
        elif not st.session_state.totranslate:
            st.error("Please enter text to translate")
        else:
            st.error("Please pick a translation language")
    # Display each column: This code runs every time an action happens on UI, so store the variable in session state
    with col1:
        st.session_state.totranslate = st.text_area("**Text to Translate**", placeholder="Enter Text Here...")
        st.write("Detected Language: ")
        st.write(st.session_state.detlang)
    with col3:
        translated = st.text_area("***Translated Text***", st.session_state.displayoutput, disabled=True)
        st.session_state.tolanguage = st.selectbox('To Language', ('', 'Arabic', 'English', 'Spanish', 'German', 'Italian', 'Spanish', 'Swedish'))

# Tab 2 for Document translations
with tab2:
    dcol1, dcol2, dcol3 = st.columns([0.4,0.2,0.4])
    with dcol1:
        files = st.file_uploader("Pick a file to translate",accept_multiple_files=True)#,accept_multiple_files=True)
    with dcol2:
        st.markdown("<br />", unsafe_allow_html=True)
        doc_btntranslate = st.button("Translate Document", use_container_width=True)
        st.session_state.dtolanguage = st.selectbox('To Language:', ('', 'Arabic', 'English', 'Spanish', 'German', 'Italian', 'Spanish', 'Swedish'))

    # When Translate button is clicked
    if doc_btntranslate:
        if st.session_state.dtolanguage and files:
            for file in files:
                # Write uploaded file to a temp directory, and retrieve path
                st.session_state.filename = file.name.split('.')[0] + "_" + file.file_id + "." + file.name.split('.')[1]
                temp_dir = tempfile.mkdtemp()
                path = os.path.join(temp_dir,st.session_state.filename)
                with open(path, "wb") as f:
                    f.write(file.getvalue())

                # Upload blob to the Azure container, into Original files folder
                account_url=os.environ["AZURE_ORIGINAL_FILES_CONTAINER_SAS_URI"]
                container_name = os.environ["AZURE_ORIGINAL_FILES_CONTAINER_NAME"]
                blob_service_client = BlobServiceClient(account_url=account_url)
                container_client=blob_service_client.get_container_client(container= container_name)
                with open(path,mode="rb") as f:
                    container_client.upload_blob(name=st.session_state.filename, data=f)

                # Call document translation API, and write output to Translated container
                resp = my_api.doctranslation_api(st.session_state.filename,languageShortcuts.get(st.session_state.dtolanguage))

                # Write a Audit log into Azure tables
                LogTable.connect_azure_table()
                LogTable.create_entity("Document","madan.jalari","Auto",st.session_state.dtolanguage,"","",st.session_state.filename,st.session_state.filename)
            with dcol3:
                with st.spinner('Translation in Progress'):
                    time.sleep(20)
            st.session_state.translation_status = "Translated"

        elif not files:
            st.error("Please pick a file to translate")
        else:
            st.error("Please pick a To Language")

    # When Download translation button is clicked. This is displayed based on transaltion_status session state set while displaying columns data
    if st.session_state.download_btn:
        for file in files:
            # Connect to translated-files container via SAS url
            st.session_state.filename = file.name.split('.')[0] + "_" + file.file_id + "." + file.name.split('.')[1]
            daccount_url = os.environ["AZURE_TRANSLATED_FILES_CONTAINER_SAS_URI"]
            translated_container_name = os.environ["AZURE_TRANSLATED_FILES_CONTAINER_NAME"]
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
            st.markdown("<h6 style='text-align: center; color: black;'>Translation not started</h6>", unsafe_allow_html=True)
            #st.text("     Translation not started")
        elif st.session_state.translation_status == "Translated":
            st.markdown("<br />", unsafe_allow_html=True)
            st.session_state.download_btn = st.button("Download Translations")
        elif st.session_state.translation_status == "Download Complete":
            st.markdown("<br />", unsafe_allow_html=True)
            st.markdown("<h5 style='text-align: center; color: Red;'><b>Download Complete</b></h5>",unsafe_allow_html=True)
            st.markdown("<h6 style='text-align: center; color: black;'>Please check your downloads folder</h6>", unsafe_allow_html=True)

 #Tab 3 to display all history of translations for the user
with tab3:
    my_filter = "User eq 'madan.jalari'"
    hh = os.getenv('AZURE_LOG_TABLE_CONN_STRING')
    table_client = TableClient.from_connection_string(conn_str=hh,table_name=os.getenv('AZURE_LOG_TABLE_NAME'))
    entities = table_client.query_entities(query_filter=my_filter)
    if entities:
        df = pd.DataFrame(entities).sort_values(by=["RowKey"],ascending=False)
        st.write(df)