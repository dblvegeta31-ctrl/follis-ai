import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# --- 1. SAYFA VE ANAHTAR AYARLARI ---
st.set_page_config(page_title="Swozzy AI 2.5", page_icon="🚀", layout="centered")

# Secrets'tan 10 anahtarı güvenli bir şekilde listeye alıyoruz
api_keys = [st.secrets[f"GOOGLE_API_KEY_{i}"] for i in range(1, 11) if f"GOOGLE_API_KEY_{i}" in st.secrets]

if "key_index" not in st.session_state:
    st.session_state.key_index = 0
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 2. GÖRSEL ARAYÜZ ---
st.title("🚀 Swozzy AI v2.5")
st.caption("Gemini 1.5 Flash Teknolojisi ile Güçlendirildi")
st.divider()

# Sohbet geçmişini ekranda göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. 1.5 FLASH MOTORU (KESİNTİSİZ MOD) ---
def ask_swozzy(user_input):
    # Anahtarları 2 tur (toplam 20 deneme) boyunca zorla
    for _ in range(len(api_keys) * 2):
        idx = st.session_state.key_index
        try:
            genai.configure(api_key=api_keys[idx])
            
            # 1.5 Flash: En hızlı ve kota dostu model
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            simdi = datetime.now().strftime("%d %B %Y")
            # Sisteme kimlik tanımlıyoruz
            context = f"Sen Swozzy AI'sın. Bugünün tarihi: {simdi}. Arkadaş canlısı, zeki ve çok hızlı yanıt ver."
            
            # Yanıtı al
            response = model.generate_content(f"{context}\n\nKullanıcı: {user_input}")
            
            if response and response.text:
                return response.text
                
        except Exception:
            # Hata (Kota dolması vb.) durumunda sessizce sonraki anahtara geç
            st.session_state.key_index = (idx + 1) % len(api_keys)
            time.sleep(0.1) # Kısa bir es vererek Google'ı yorma
            continue
            
    return "Şu an tüm hatlar çok yoğun, lütfen 10 saniye bekleyip tekrar sormayı dene."

# --- 4. SOHBET AKIŞI ---
if prompt := st.chat_input("Swozzy'ye bir şeyler sor..."):
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Swozzy yanıtını üret
    with st.chat_message("assistant"):
        with st.spinner(""): # Yazısız, sade yükleme simgesi
            answer = ask_swozzy(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
