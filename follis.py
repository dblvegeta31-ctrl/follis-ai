import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- 1. SİSTEM YAPILANDIRMASI ---
st.set_page_config(page_title="Swozzy AI", page_icon="🚀", layout="centered")

# Secrets'tan 10 adet anahtarı temiz bir şekilde çekiyoruz
api_keys = [st.secrets[f"GOOGLE_API_KEY_{i}"] for i in range(1, 11) if f"GOOGLE_API_KEY_{i}" in st.secrets]

# Anahtar bulunamazsa durdur
if not api_keys:
    st.error("Lütfen Streamlit Secrets kısmına GOOGLE_API_KEY_1... anahtarlarını ekle.")
    st.stop()

# Hafıza ve Anahtar Sırası Yönetimi
if "key_index" not in st.session_state:
    st.session_state.key_index = 0
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 2. ARAYÜZ TASARIMI ---
st.title("🚀 Swozzy AI v2.5")
st.markdown("---")

# Sohbet geçmişini ekranda tut
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. ZEKA MOTORU (BENİM ÇALIŞMA MANTIĞIM) ---
def ask_swozzy(user_input):
    # 10 anahtarı sırayla döner, biri hata verirse diğerine geçer
    for _ in range(len(api_keys)):
        idx = st.session_state.key_index
        try:
            genai.configure(api_key=api_keys[idx])
            
            # En hızlı ve samimi yanıt veren model (1.5 Flash)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Kimlik tanımı ve tarih bilgisi
            simdi = datetime.now().strftime("%d %B %Y")
            context = f"Sen Swozzy AI'sın. Bugün {simdi}. Çok hızlı, zeki ve samimi bir arkadaş gibi yanıt ver."
            
            response = model.generate_content(f"{context}\n\nKullanıcı: {user_input}")
            
            if response.text:
                return response.text
        except:
            # Hata anında sessizce sonraki anahtara zıpla
            st.session_state.key_index = (idx + 1) % len(api_keys)
            continue
            
    return "Şu an tüm hatlarım meşgul, lütfen bir saniye sonra tekrar dene."

# --- 4. KULLANICI ETKİLEŞİMİ ---
# Arama yerine senin istediğin metni yazdık
if prompt := st.chat_input("Swozzy'ye sorun..."):
    # Kullanıcının yazdığını hafızaya al ve göster
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Benim (Gemini) zekamla cevap üret
    with st.chat_message("assistant"):
        with st.spinner(""): # Yazısız, hızlı animasyon
            answer = ask_swozzy(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
