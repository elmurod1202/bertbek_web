import streamlit as st
import requests

st.set_page_config(page_title="Atoqli Otlarni Tanish", page_icon="🕵️")
st.title("🕵️ Atoqli Otlarni Tanish (NER)")

st.markdown("""
Bu model **Oʻzbek tilidagi matndan** shaxslar, joy nomlari, tashkilotlar, sanalar kabi **atoqli otlarni avtomatik aniqlaydi**.

**Masalan:** `"Shavkat Mirziyoyev 9-mart kuni Samarqandda nutq so‘zladi."`  
""")

# Hugging Face Inference API config
API_URL = "https://api-inference.huggingface.co/models/elmurod1202/bertbek-ner-uznews"
API_TOKEN = st.secrets["HF_TOKEN"]  # Or use your token directly for local testing
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

def query_ner(text):
    try:
        response = requests.post(API_URL, headers=HEADERS, json={"inputs": text})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Xatolik yuz berdi: {e}")
        return None

# Color theme for entity types
entity_colors = {
    "PERSON": "#f4cccc",
    "LOCATION": "#c9daf8",
    "ORG": "#d9ead3",
    "DATE": "#fff2cc",
    "TIME": "#e6b8af",
    "MISC": "#d0e0e3"
}

# User input
text_input = st.text_area("📝 Matn kiriting:", height=200, placeholder="Masalan: Shavkat Mirziyoyev 9-mart kuni Samarqandda nutq so‘zladi.")

if st.button("🔍 Tanish"):
    if not text_input.strip():
        st.warning("Iltimos, matn kiriting.")
    else:
        with st.spinner("⏳ Tahlil qilinmoqda..."):
            result = query_ner(text_input)

        if result and isinstance(result, list):
            # Merge adjacent tokens with the same entity group
            merged = []
            for ent in result:
                if not merged:
                    merged.append(ent)
                    continue

                last = merged[-1]
                # Merge if same entity group and touching
                if ent["entity_group"] == last["entity_group"] and ent["start"] == last["end"]:
                    merged[-1]["end"] = ent["end"]
                else:
                    merged.append(ent)

            # Highlight the merged entities
            styled_text = ""
            last_idx = 0
            for ent in merged:
                start = ent["start"]
                end = ent["end"]
                label = ent["entity_group"]
                color = entity_colors.get(label, "#eeeeee")

                # Add non-entity text before this
                styled_text += text_input[last_idx:start]

                # Add styled span
                styled_text += f"""<span style="background-color:{color}; padding:2px 4px; border-radius:4px;">{text_input[start:end]} <sup style="color:gray;">[{label}]</sup></span>"""
                last_idx = end

            # Add remaining text
            styled_text += text_input[last_idx:]

            # Show result
            st.markdown("### 🖍️ Atoqli otlar bilan ajratilgan matn:")
            st.markdown(styled_text, unsafe_allow_html=True)
