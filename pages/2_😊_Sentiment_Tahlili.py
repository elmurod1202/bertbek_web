import streamlit as st
import requests
import plotly.graph_objects as go

st.set_page_config(page_title="Sentiment Tahlili", layout="wide")

# Hugging Face API for sentiment
API_URL = "https://api-inference.huggingface.co/models/elmurod1202/BERTbek-news-big-cased-sentiment-apps"
headers = {"Authorization": f"Bearer {st.secrets['HF_TOKEN']}"}

# Label mapping
label_map = {
    "LABEL_0": "Salbiy",
    "LABEL_1": "Ijobiy"
}

def query_sentiment(text):
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": text}, timeout=15)
        if response.status_code == 503:
            st.warning("⏳ Model yuklanmoqda. Iltimos, qayta urinib ko‘ring.")
            return []
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error("Xatolik yuz berdi.")
        st.warning(e)
        return []

# App UI
st.title("😊 Sentiment Tahlili")
st.markdown("Matnni kiriting va model bahosini ko‘ring:")

text = st.text_input("Fikr matni:", "Bu xizmat menga juda yoqdi!")

if st.button("📤 Tahlilni boshlash"):
    if text.strip():
        with st.spinner("⏳ Tahlil qilinmoqda..."):
            result = query_sentiment(text)

        if result:
            r = result[0][0] if isinstance(result[0], list) else result[0]
            raw_label = r["label"]
            label = label_map.get(raw_label, raw_label)
            score = r["score"] * 100  # Convert to %

            st.markdown(f"### 🧠 Model natijasi: **{label}** (aniqlik: {score:.2f}%)")
                 # Build two gauges: one for each label
        negative_color_steps = [
            {'range': [0, 20], 'color': "lightcoral"},
            {'range': [20, 45], 'color': "tomato"},
            {'range': [45, 65], 'color': "red"},
            {'range': [65, 85], 'color': "darkred"},
            {'range': [85, 100], 'color': "maroon"},
        ]

        positive_color_steps = [
            {'range': [0, 20], 'color': "lightgreen"},
            {'range': [20, 45], 'color': "lime"},
            {'range': [45, 65], 'color': "limegreen"},
            {'range': [65, 85], 'color': "forestgreen"},
            {'range': [85, 100], 'color': "green"},
        ]

        # Negative gauge
        fig_neg = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score if raw_label == "LABEL_0" else 100.0-score,
            title={'text': "Salbiy ehtimoli (%)"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "grey"},
                'steps': negative_color_steps,
                'threshold': {
                    'line': {'color': "blue", 'width': 4},
                    'thickness': 0.75,
                    'value': score if raw_label == "LABEL_0" else 100.0-score
                }
            }
        ))

        # Positive gauge
        fig_pos = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score if raw_label == "LABEL_1" else 100.0-score,
            title={'text': "Ijobiy ehtimoli (%)"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "grey"},
                'steps': positive_color_steps,
                'threshold': {
                    'line': {'color': "blue", 'width': 4},
                    'thickness': 0.75,
                    'value': score if raw_label == "LABEL_1" else 100.0-score
                }
            }
        ))

        # Show side-by-side
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_neg, use_container_width=True)
        with col2:
            st.plotly_chart(fig_pos, use_container_width=True)

    else:
        st.warning("❗ Iltimos, fikr matnini kiriting.")

   