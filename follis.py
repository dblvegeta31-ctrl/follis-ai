import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# --- 1. SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="Swozzy AI 2.5 Ultra", page_icon=":rocket:", layout="centered")

# --- 2. 10'LU PROJE ANAHTAR HAVUZU ---
api_keys = []
for i in range(1, 11):
    key_name = f"GOOGLE_API_KEY_{i}"
    if key_name in st.secrets:
        api_keys.append(st.secrets[key_name])

if "key_index" not in st.session_state:
    st.session_state.key_index = 0
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. GÖRSEL ARAYÜZ (Markdown Destekli) ---
st.markdown("# :streamlit: Swozzy AI v2.5 Ultra")
st.markdown("### *Gerçek Zamanlı Veri ve Google Search Entegrasyonu*")
st.divider()

# Sohbet Geçmişini Görüntüle
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. AKILLI CEVAP MOTORU (Search & 2026 Focus) ---
def ask_gemini(user_query):
    for _ in range(len(api_keys)):
        current_key = api_keys[st.session_state.key_index]
        try:
            genai.configure(api_key=current_key)
            
            # Google'ın en güçlü deneysel modeli (2.5 seviyesi)
            model = genai.GenerativeModel(
                model_name='gemini-2.0-flash-exp',
                tools=[{'google_search_retrieval': {}}] # Canlı internet erişimi
            )
            
            # Tarihi saniye hassasiyetinde veriyoruz
            simdi = datetime.now().strftime("%d %B %Y, %A, Saat: %H:%M:%S")
            
            system_instruction = (
                f"Sen Swozzy AI v2.5'sin. Bugünün kesin tarihi: {simdi}. "
                "Hafızandaki eski bilgiler yerine Google Search kullanarak en güncel veriyi sunmalısın. "
                "Kesinlikle yanlış veya taraflı bilgi verme. Tarihleri milimetrik doğrula."
            )
            
            response = model.generate_content(f"{system_instruction}\n\nKullanıcı Sorusu:
