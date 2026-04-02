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

# --- 4. CEVAP MOTORU (GÜNCELLENDİ) ---
def ask_gemini(user_query):
    for _ in range(len(api_keys)):
        current_key = api_keys[st.session_state.key_index]
        try:
            # Yapılandırmayı her seferinde sıfırla
            genai.configure(api_key=current_key)
            
            # MODEL İSMİ DÜZELTİLDİ: En yalın halini kullanıyoruz
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Kısa bir sistem mesajıyla dene
            response = model.generate_content(user_query)
            
            if response and response.text:
                return response.text, "SUCCESS"
            else:
                raise Exception("Boş cevap döndü.")
                
        except Exception as e:
            err_msg = str(e)
            # Hangi anahtarın ne hata verdiğini sağ altta ufakça göster
            st.toast(f"Anahtar {st.session_state.key_index + 1} denendi: {err_msg[:40]}...", icon="ℹ️")
            
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
        loading_box = st.empty()
        with loading_box.container():
            with st.spinner("Yanıt oluşturuluyor..."):
                answer, status = ask_gemini(prompt)
        loading_box.empty()

        if status == "SUCCESS":
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        elif status == "ALL_LIMITS_HIT":
            st.error("Şu an tüm projelerden 404/429 hatası dönüyor. Lütfen API anahtarlarınızın 'Gemini API' için oluşturulduğundan emin olun.")
