import streamlit as st
import google.generativeai as genai

# Arayüz Ayarı
st.set_page_config(page_title="Swozzy AI")

# API Bağlantısı
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-pro') # En stabil model ismi
else:
    st.error("Secrets kısmına GOOGLE_API_KEY ekle!")
    st.stop()

st.title("Swozzy AI (Güvenli Mod)")

# Basit Hafıza Sistemi
if "history" not in st.session_state:
    st.session_state.history = []

# Giriş Alanı
user_input = st.text_input("Sorunu buraya yaz ve Enter'a bas:", key="user_input")

if user_input:
    try:
        response = model.generate_content(user_input)
        st.session_state.history.append({"q": user_input, "a": response.text})
    except Exception as e:
        st.error(f"Hata: {e}")

# Mesajları Liste Halinde Yazdır (Chat balonu kullanmadan, en güvenli yol)
for chat in reversed(st.session_state.history):
    st.write(f"**Sen:** {chat['q']}")
    st.info(f"**Swozzy:** {chat['a']}")
    st.divider()
