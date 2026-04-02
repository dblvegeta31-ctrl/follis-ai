import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="Swozzy AI Ultra", page_icon="⚡", layout="centered")

# --- 2. 10'LU ANAHTAR HAVUZU ---
api_keys = []
for i in range(1, 11):
    key_name = f"GOOGLE_API_KEY_{i}"
    if key_name in st.secrets:
        api_keys.append(st.secrets[key_name])

if not api_keys:
    st.error("⚠️ Hata: Secrets kısmında API anahtarı bulunamadı!")
    st.stop()

if "key_index" not in st.session_state:
    st.session_state.key_index = 0
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. ARAYÜZ ---
st.title("⚡ Swozzy AI Ultra")
st.divider()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. CEVAP MOTORU (2.5 FLASH GÜNCELLEMESİ) ---
def ask_gemini(user_query):
    for _ in range(len(api_keys)):
        current_key = api_keys[st.session_state.key_index]
        try:
            genai.configure(api_key=current_key)
            
            # MODEL İSMİ GÜNCELLENDİ
            # Eğer 'gemini-2.5-flash' 404 verirse, Google henüz bu ismi tanımlamamış demektir.
            # Bu durumda en kararlı yeni sürüm olan 'gemini-2.0-flash' denenebilir.
            model = genai.GenerativeModel('gemini-2.0-flash') 
            
            response = model.generate_content(user_query)
            
            if response and response.text:
                return response.text, "SUCCESS"
            else:
                raise Exception("Yanıt metni boş.")
                
        except Exception as e:
            err_msg = str(e).upper()
            # Hangi anahtarın ne hatası verdiğini sağ altta göster
            st.toast(f"Anahtar {st.session_state.key_index + 1} denendi: {err_msg[:30]}...", icon="⚠️")
            
            # Bir sonraki anahtara geç
            st.session_state.key_index = (st.session_state.key_index + 1) % len(api_keys)
            continue
                
    return None, "ALL_LIMITS_HIT"

# --- 5. MESAJLAŞMA AKIŞI ---
if prompt := st.chat_input("Bir şeyler yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        status_placeholder = st.empty()
        
        with status_placeholder.container():
            with st.spinner("Swozzy AI yanıtlıyor..."):
                answer, status = ask_gemini(prompt)
        
        status_placeholder.empty()

        if status == "SUCCESS":
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        elif status == "ALL_LIMITS_HIT":
            st.error("⚠️ Şu an tüm anahtarlar 404 (Model Bulunamadı) hatası veriyor. Model ismini 'gemini-pro' olarak değiştirmeyi deneyebilirsiniz.")
