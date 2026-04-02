import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="Swozzy AI 2026", page_icon="🌐", layout="centered")

# --- 2. 10'LU ANAHTAR HAVUZU ---
api_keys = []
for i in range(1, 11):
    key_name = f"GOOGLE_API_KEY_{i}"
    if key_name in st.secrets:
        api_keys.append(st.secrets[key_name])

if "key_index" not in st.session_state:
    st.session_state.key_index = 0
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. ARAYÜZ ---
st.title("🌐 Swozzy AI Ultra 2026")
st.caption("Google Search Entegrasyonu & 2.0 Flash Altyapısı")
st.divider()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. AKILLI CEVAP MOTORU (ARAMA DESTEKLİ) ---
def ask_gemini(user_query):
    for _ in range(len(api_keys)):
        current_key = api_keys[st.session_state.key_index]
        try:
            genai.configure(api_key=current_key)
            
            # GÜNCEL BİLGİ İÇİN TOOLS EKLEDİK
            # Bu kısım modelin internete bağlanmasını sağlar
            model = genai.GenerativeModel(
                model_name='gemini-2.0-flash', # En güncel zeka
                tools=[{'google_search_retrieval': {}}] # CANLI İNTERNET ERİŞİMİ
            )
            
            simdi = datetime.now().strftime("%d %B %Y %H:%M")
            prompt = f"Bugünün gerçek tarihi: {simdi}. Sen güncel bilgilere sahip Swozzy AI'sın. Yanlış veya eski bilgi verme. Soru: {user_query}"
            
            response = model.generate_content(prompt)
            
            if response and response.text:
                return response.text, "SUCCESS"
        
        except Exception as e:
            err = str(e).upper()
            st.toast(f"Anahtar {st.session_state.key_index + 1} atlanıyor...", icon="⏳")
            st.session_state.key_index = (st.session_state.key_index + 1) % len(api_keys)
            continue
                
    return None, "LIMIT"

# --- 5. MESAJLAŞMA AKIŞI ---
if prompt := st.chat_input("2026 gündemini sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        loading = st.empty()
        with loading.container():
            with st.spinner("İnternet taranıyor ve yanıt üretiliyor..."):
                answer, status = ask_gemini(prompt)
        loading.empty()

        if status == "SUCCESS":
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        elif status == "LIMIT":
            st.error("⚠️ Limit doldu. Lütfen 1-2 dakika sonra tekrar deneyin.")
