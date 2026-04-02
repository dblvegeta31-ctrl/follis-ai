import streamlit as st
import google.generativeai as genai

# API Yapılandırması
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("API Key Eksik!")
    st.stop()

# Model Tanımı
model = genai.GenerativeModel('gemini-1.5-flash')

# Arayüz
st.set_page_config(page_title="Swozzy")

with st.sidebar:
    st.title("2.5-Flash")
    if st.button("Temizle"):
        st.session_state.messages = []
        st.rerun()

st.title("Swozzy AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

if p := st.chat_input("Swozzy'ye sor..."):
    st.session_state.messages.append({"role": "user", "content": p})
    with st.chat_message("user"):
        st.write(p)
    
    with st.chat_message("assistant"):
        try:
            r = model.generate_content(p)
            st.write(r.text)
            st.session_state.messages.append({"role": "assistant", "content": r.text})
        except Exception as e:
            st.error(f"Hata: {e}")
