import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="Swozzy AI Ultra", page_icon="⚡")

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
st.title("⚡ Swozzy AI Ultra")
st.divider()

# Mesaj geçmişini göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. CEVAP MOTORU (HER ŞEYE CEVAP VEREN VERSİYON) ---
def ask_gemini(user_query):
    # Anahtarları tek tek dene
    for _ in range(len(api_keys)):
        current_key = api_keys[st.session_state.key_index]
        try:
            genai.configure(api_key=current_key)
            
            # Hem zeki hem güncel olması için 2.0-flash ve arama aracı
            model = genai.GenerativeModel(
                model_name='gemini-2.0-flash-exp',
                tools=[{'google_search_retrieval': {}}]
            )
            
            simdi = datetime.now().strftime("%d %B %Y, %A")
            prompt = (
                f"Sen Swozzy AI v2.5'sin. Bugünün tarihi: {simdi}. "
                "Hem samimi bir sohbet arkadaşı ol hem de bilgi istendiğinde Google Search kullanarak en güncel veriyi ver. "
                f"\nSoru/Mesaj: {user_query}"
            )
            
            response = model.generate_content(prompt)
            
            if response and response.text:
                return response.text, "SUCCESS"
        
        except Exception as e:
            # Hata varsa sessizce bir sonraki anahtara geç
            st.session_state.key_index = (st.session_state.key_index + 1) % len(api_keys)
            continue
                
    return None, "LIMIT"

# --- 5. AKIŞ ---
if prompt := st.chat_input("Swozzy'ye bir şeyler sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        loading = st.empty()
        with loading.container():
            with st.spinner(" "): 
                answer, status = ask_gemini(prompt)
        loading.empty()

        if status == "SUCCESS":
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.error("Şu an tüm hatlar dolu, lütfen bir dakika sonra tekrar dene.")
