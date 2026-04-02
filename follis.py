import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Swozzy AI Ultra", page_icon="⚡")

# --- ANAHTARLARI ÇEK ---
api_keys = []
for i in range(1, 11):
    key_name = f"GOOGLE_API_KEY_{i}"
    if key_name in st.secrets:
        api_keys.append(st.secrets[key_name])

if not api_keys:
    st.error("Secrets kısmında hiç anahtar yok!")
    st.stop()

if "key_index" not in st.session_state:
    st.session_state.key_index = 0
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("⚡ Swozzy AI Ultra")
st.divider()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CEVAP MOTORU ---
def ask_gemini(user_query):
    for _ in range(len(api_keys)):
        current_key = api_keys[st.session_state.key_index]
        try:
            genai.configure(api_key=current_key)
            # Model ismini en yalın haliyle deniyoruz
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            response = model.generate_content(user_query)
            return response.text, "SUCCESS"
            
        except Exception as e:
            # HATAYI GÖRMEK İÇİN BURASI ÇOK ÖNEMLİ:
            st.toast(f"Anahtar {st.session_state.key_index + 1} hatası: {str(e)[:50]}", icon="⚠️")
            st.session_state.key_index = (st.session_state.key_index + 1) % len(api_keys)
            time.sleep(0.5) # Google'ı yormamak için kısa bir es
            continue
                
    return None, "ALL_LIMITS_HIT"

# --- AKIŞ ---
if prompt := st.chat_input("Bir şeyler yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        loading_box = st.empty()
        with loading_box.container():
            with st.spinner("Düşünüyorum..."):
                answer, status = ask_gemini(prompt)
        loading_box.empty()

        if status == "SUCCESS":
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        elif status == "ALL_LIMITS_HIT":
            st.error("Şu an tüm anahtarlar yanıt vermiyor. Lütfen 1 dakika sonra tekrar dene.")
