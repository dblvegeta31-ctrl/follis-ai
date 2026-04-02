import streamlit as st
import google.generativeai as genai

# API Ayarı
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("API Key Eksik!")
    st.stop()

# MODEL TANIMLAMA (404 hatasını çözen doğru isimler)
# 'models/gemini-1.5-flash' veya sadece 'gemini-1.5-flash'
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Model yükleme hatası: {e}")

st.title("Swozzy AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

if prompt := st.chat_input("Mesajını yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    try:
        # Yanıt alma
        response = model.generate_content(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.chat_message("assistant").write(response.text)
    except Exception as e:
        # Eğer hala 404 verirse buraya düşecek
        st.error(f"Hala 404 mü? Detay: {e}")
