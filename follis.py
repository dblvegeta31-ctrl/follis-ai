import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="Swozzy AI Ultra 2.5", page_icon="⚡", layout="centered")

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
st.title("⚡ Swozzy AI Ultra 2.5")
st.caption("Gelecek Nesil Model Yapılandırması Aktif")
st.divider()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. AKILLI CEVAP MOTORU ---
def ask_gemini(user_query):
    for _ in range(len(api_keys)):
        current_key = api_keys[st.session_state.key_index]
        try:
            genai.configure(api_key=current_key)
            
            # --- MODEL DENEME SIRALAMASI ---
            # Önce senin istediğin 2.5, olmazsa 2.0, olmazsa 1.5
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                response = model.generate_content(user_query)
            except:
                try:
                    model = genai.GenerativeModel('gemini-2.0-flash')
                    response = model.generate_content(user_query)
                except:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(user_query)
            
            if response and response.text:
                return response.text, "SUCCESS"
        
        except Exception as e:
            err = str(e).upper()
            if "429" in err:
                st.toast(f"Anahtar {st.session_state.key_index + 1} limiti doldu.", icon="⏳")
            else:
                st.toast(f"Anahtar {st.session_state.key_index + 1} hata verdi.", icon="⚠️")
            
            st.session_state.key_index = (st.session_state.key_index + 1) % len(api_keys)
            continue
                
    return None, "LIMIT"

# --- 5. MESAJLAŞMA AKIŞI ---
if prompt := st.chat_input("2.5 gücüyle bir şeyler yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        loading = st.empty()
        with loading.container():
            with st.spinner("2.5 Modeli Sorgulanıyor..."):
                answer, status = ask_gemini(prompt)
        loading.empty()

        if status == "SUCCESS":
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        elif status == "LIMIT":
            st.error("⚠️ Tüm anahtarların limiti doldu veya model henüz bu anahtarlar için tanımlı değil.")
