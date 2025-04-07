import streamlit as st
from PIL import Image
import base64

# Set page configuration
st.set_page_config(
    page_title="BERTbek til modeli",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Ushbu dasturiy taqdimot BERTbek modeli asosida yaratilgan.",
    }
)


# Sidebar Logo
st.sidebar.image("assets/bertbek.png", use_container_width =True)


# # Sidebar title
# st.sidebar.title("🧠 BERTbek til modeli")

# Footer links with proper icon sizes
st.sidebar.markdown("---")
st.sidebar.markdown("<small>📌 Barcha til modellari quyidagi HuggingFace sahifada mavjud: <a href=\"https://huggingface.co/elmurod1202\" target=\"_blank\"><img src=\"https://huggingface.co/front/assets/huggingface_logo-noborder.svg\" style=\"width:18px; vertical-align:middle; margin-right:6px;\"> Hugging Face</a></small>", unsafe_allow_html=True)
st.sidebar.markdown("<small>📌 Ushbu dasturiy vosita kodi ochiq va quyidagi GitHub sahifada joylashgan: <a href='https://github.com/elmurod1202/bertbek_web' target='_blank'><img src=\"https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png\" style=\"width:22px; vertical-align:middle; margin-right:6px;\">GitHub</a></small>", unsafe_allow_html=True)



# Main page
st.markdown("<h1 style='text-align: center;'>BERTbek til modeli</h1>", unsafe_allow_html=True)
st.markdown("### ", unsafe_allow_html=True)  # Spacer

# Centered layout with four task buttons
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    st.image("assets/mlm.png", width=150)
    if st.button("🧩 Niqobli Til Modeli"):
        st.switch_page("pages/1_🧩_Niqobli_Til_Modeli.py")

with col2:
    st.image("assets/sentiment.png", width=150)
    if st.button("😊 Sentiment Tahlili"):
        st.switch_page("pages/2_😊_Sentiment_Tahlili.py")

with col3:
    st.image("assets/classification.png", width=150)
    if st.button("🔎 Matnlarni Tasniflash"):
        st.switch_page("pages/3_🔎_Matnlarni_Tasniflash.py")

with col4:
    st.image("assets/ner.png", width=150)
    if st.button("🕵️ Atoqli Otlarni Tanish"):
        st.switch_page("pages/4_🕵️_Atoqli_Otlarni_Tanish.py")
