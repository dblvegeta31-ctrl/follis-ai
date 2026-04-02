import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Swozzy AI Ultra", page_icon="⚡")

# --- 10'LU ANAHTAR HAVUZU ---
api_keys = []
for i in range(1, 11):
    key_name = f"GOOGLE_API_KEY_{i}"
    if key_name in st.secrets:
        api_keys.append(st.secrets[key_name])

if "key_index" not in st.session_state:
    st.session_state.key_index = 0
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- ARAYÜZ ---
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
            
            # EN YÜKSEK KOTALI MODEL: 1.5-flash
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            response = model.generate_content(user_query)
            if response and response.text:
                return response.text, "SUCCESS"
        except Exception as e:
            err = str(e).upper()
            # Kotan dolduysa (429) bir sonrakine geç
            if "429" in err:
                st.toast(f"Anahtar {st.session_state.key_index + 1} doldu, aktarılıyor...", icon="⏳")
                st.session_state.key_index = (st.session_state.key_index + 1) % len(api_keys)
                continue
            else:
                st.toast(f"Hata: {err[:30]}", icon="❌")
                st.session_state.key_index = (st.session_state.key_index + 1) % len(api_keys)
                continue
                
    return None, "LIMIT"

# --- AKIŞ ---
if prompt := st.chat_input("Mesajınızı yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        loading = st.empty()
        with loading.container():
            with st.spinner("Düşünüyorum..."):
                answer, status = ask_gemini(prompt)
        loading.empty()

        if status == "SUCCESS":
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        elif status == "LIMIT":
            # 3 Dakikalık Geri Sayım (Google'ın seni bloklamasını engeller)
            countdown = st.empty()
            for i in range(180, 0, -1):
                countdown.error(f"⚠️ Tüm anahtarların günlük/dakikalık limiti bitti. {i} saniye beklemeniz gerekiyor...")
                time.sleep(1)
            countdown.empty()
            st.info("Süre doldu, tekrar deneyebilirsiniz.")
