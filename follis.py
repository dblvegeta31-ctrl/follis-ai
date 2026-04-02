import streamlit as st
import google.generativeai as genai

# Sadece en gerekli ayarlar
st.set_page_config(page_title="Swozzy")

if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("API Anahtarı Eksik!")
    st.stop()

# Sol tarafta sadece yazı
st.sidebar.title("2.5-Flash")

st.title("Swozzy AI")

# Sohbeti başlat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları yazdır (En sade yöntemle)
for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

if prompt := st.chat_input("Mesaj yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.chat_message("assistant").write(response.text)
    except Exception as e:
        st.error(f"Hata: {e}")
