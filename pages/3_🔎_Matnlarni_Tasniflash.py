import streamlit as st
import requests
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Matnlarni Tasniflash", page_icon="🔎")
st.title("🔎 Matnlarni Tasniflash")

API_URL = "https://api-inference.huggingface.co/models/elmurod1202/bertbek-news-classifier"
API_TOKEN = st.secrets['HF_TOKEN']  # Replace with your real token or use secrets
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

def query_classification(text):
    payload = {"inputs": text}
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Xatolik yuz berdi: {e}")
        return None

# UI
st.markdown("""
Bu model **O'zbek tilidagi matnni** quyidagi klass/kategoriyalardan biriga tegishli ekanini aniqlab beradi:
**Local** (Mahalliy),
    **World** (Dunyo),
    **Sport** (Sport),
    **Society** (Jamiyat),
    **Law** (Qonunchilik),
    **Tech** (Texnologiya),
    **Culture** (Madaniyat),
    **Politics** (Siyosat),
    **Economics** (Iqtisodiyot),
    **Auto** (Avto),
    **Health** (Salomatlik),
    **Crime** (Jinoyat),
    **Photo** (Foto),
    **Women** (Ayollar),
    **Culinary** (Pazandachilik)
            
""")
text_input = st.text_area("📝 Matn kiriting:", height=200, placeholder="Masalan: Bugun O'zbekiston Prezidenti yangi qaror qabul qildi.")

labels = {
    "Local": "Mahalliy",
    "World": "Dunyo",
    "Sport": "Sport",
    "Society": "Jamiyat",
    "Law": "Qonunchilik",
    "Tech": "Texnologiya",
    "Culture": "Madaniyat",
    "Politics": "Siyosat",
    "Economics": "Iqtisodiyot",
    "Auto": "Avto",
    "Health": "Salomatlik",
    "Crime": "Jinoyat",
    "Photo": "Foto",
    "Women": "Ayollar",
    "Culinary": "Pazandachilik"
}

if st.button("📊 Tasniflash"):
    if not text_input.strip():
        st.warning("Iltimos, matn kiriting.")
    else:
        with st.spinner("⏳ Tasniflanmoqda..."):
            result = query_classification(text_input)

        if result and isinstance(result, list):
            predictions = result[0] if isinstance(result[0], list) else result

            # 🔝 Top prediction
            top_pred = max(predictions, key=lambda x: x["score"])
            top_label_raw = top_pred["label"].replace("LABEL_", "")
            top_label = labels.get(top_label_raw, top_label_raw)
            top_score = top_pred["score"] * 100

            st.success(f"🧠 **Eng ehtimolli kategoriya**: {top_label}")
            st.write(f"📈 Aniqlik: `{top_score:.2f}%`")

                       
            # 📊 All predictions
            st.markdown("### 📋 Barcha kategoriyalar ehtimolliklari:")
            top_n = 4
            top_preds = sorted(predictions, key=lambda x: x["score"], reverse=True)[:top_n]

            # Create columns
            cols = st.columns(top_n)

            for i, pred in enumerate(top_preds):
                label_key = pred["label"].replace("LABEL_", "")
                label = labels.get(label_key, label_key)
                score = pred["score"] * 100

                with cols[i]:
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=score,
                        title={'text': f"{label}"},
                        domain={'x': [0, 1], 'y': [0, 1]},
                        gauge={
                            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkgray"},
                            'bar': {'color': "gray"},
                            'steps': [
                                {'range': [0, 20], 'color': "darkred"},
                                {'range': [20, 45], 'color': "orangered"},
                                {'range': [45, 55], 'color': "yellow"},
                                {'range': [55, 70], 'color': "yellowgreen"},
                                {'range': [70, 85], 'color': "limegreen"},
                                {'range': [85, 100], 'color': "lime"}
                            ],
                            'threshold': {
                                'line': {'color': "blue", 'width': 4},
                                'thickness': 0.75,
                                'value': score
                            }
                        }
                    ))
                    fig.update_layout(height=250, margin=dict(t=40, b=20, l=20, r=20))
                    st.plotly_chart(fig, use_container_width=True)

                        

