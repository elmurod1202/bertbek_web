import streamlit as st
import requests

st.set_page_config(page_title="Niqobli Til Modeli", layout="wide")

API_URL = "https://api-inference.huggingface.co/models/elmurod1202/bertbek-news-big-cased"
headers = {"Authorization": f"Bearer " + st.secrets['HF_TOKEN']}

def query_mlm(text):
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": text}, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error("Xatolik yuz berdi.")
        st.warning(e)
        return []

st.title("🤖 Niqobli Til Modeli")
st.markdown("Model `[MASK]` o‘rnidagi so‘zni taxmin qiladi. Masalan: `Oʻzbekiston Futbol boʻyicha [MASK] chempionatiga mezbonlik qiladi.`")

# Input
text = st.text_input("Matn kiriting:", "Oʻzbekiston Futbol boʻyicha [MASK] chempionatiga mezbonlik qiladi.")

if st.button("📤 Submit"):
    if text.strip():
        if "[MASK]" in text:
            with st.spinner("⏳ Model ishlamoqda..."):
                result = query_mlm(text)

            if result:
                st.subheader("🔮 Natijalar:")
                mask_parts = text.split("[MASK]")
                prefix = mask_parts[0].strip()
                suffix = mask_parts[1].strip() if len(mask_parts) > 1 else ""

                for pred in result:
                    full = pred["sequence"]

                    # Try to isolate the filled-in part
                    try:
                        start = len(prefix)
                        end = len(full) - len(suffix)
                        inserted = full[start:end].strip()
                    except:
                        inserted = "?"

                    # Highlight the predicted word(s)
                    highlighted = full.replace(inserted, f"**:green[{inserted}]**", 1)
                    st.markdown(f"👉 {highlighted} _(aniqlik: `{pred['score']:.4f}`)_")
        else:
            st.warning("❗ Matnda [MASK] niqobi qatnashishi shart.")
    else:
        st.warning("❗ Matnni kiriting.")
