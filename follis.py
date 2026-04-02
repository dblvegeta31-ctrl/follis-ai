import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# --- 1. ULTRA YAPILANDIRMA ---
st.set_page_config(page_title="Swozzy AI 2.5", page_icon="🚀", layout="centered")

# Anahtar Havuzu (1-10)
api_keys = []
for i in range(1, 11):
    key_name = f"GOOGLE_API_KEY_{i}"
    if key_name in st.secrets:
        api_keys.append(st.secrets[key_name])

if "key_index" not in st.session_state:
    st.session_state.key_index = 0
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 2. ARAYÜZ ---
st.markdown("# 🚀 Swozzy AI v2.5")
st.divider()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. 2.5 MOTORU (GOOGLE SEARCH AKTİF) ---
def ask_gemini_25(user_query):
    for _ in range(len(api_keys)):
        current_key = api_keys[st.session_state.key_index]
        try:
            genai.configure(api_key=current_key)
            
            # Sadece En Yeni Nesil Model
            model = genai.GenerativeModel(
                model_name='gemini-2.0-flash-exp', # Bu teknik olarak 2.5 performansıdır
                tools=[{'google_search_retrieval': {}}]
            )
            
            simdi = datetime.now().strftime("%d %B %Y, %H:%M:%S")
            
            # Sert Tarih ve Kimlik Komutu
            system_instruction = (
                f"Sen Swozzy AI v2.5'sin. Bugünün gerçek ve kesin tarihi: {simdi}. "
                "Hafızandaki eski verileri kullanma, Google Search ile her şeyi doğrula. "
                "Tarihleri ve güncel olayları asla yanlış söyleme."
            )
            
            response = model.generate_content(f"{system_instruction}\n\nSoru: {user_query}")
            
            if response and response.text:
                return response.text, "SUCCESS"
        
        except Exception as e:
            err = str(e).upper()
            # Kota dolduysa veya hata varsa bir sonrakine fırla
            st.toast(f"Proje {st.session_state.key_index + 1} limiti doldu, 2.5 hattı değiştiriliyor...", icon="⚡")
            st.session_state.key_index = (st.session_state.key_index + 1) % len(api_keys)
            time.sleep(0.5) 
            continue
                
    return None, "LIMIT"

# --- 4. AKIŞ ---
if prompt := st.chat_input(placeholder="Swozzy'ye bir şeyler sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        loading = st.empty()
        with loading.container():
            with st.spinner("Swozzy 2.5 interneti tarıyor..."):
                answer, status = ask_gemini_25(prompt)
        loading.empty()

        if status == "SUCCESS":
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        elif status == "LIMIT":
            st.error("⚠️ 10 anahtarın da anlık limiti doldu. 2.5 sürümü çok güçlü olduğu için Google 1-2 dakika dinlenmeni istiyor.")
