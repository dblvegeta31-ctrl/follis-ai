import streamlit as st
import google.generativeai as genai

# Sayfa yapılandırması (Hata payını sıfıra indirmek için en üste)
st.set_page_config(page_title="Swozzy AI")

# Sol menü (Sidebar)
st.sidebar.title("2.5-Flash")

# API Anahtarı Kontrolü
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Hata: Secrets kısmında 'GOOGLE_API_KEY' bulunamadı!")
    st.stop()

# Model Kurulumu
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("Swozzy AI")

# Basit mesajlaşma
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

if prompt := st.chat_input("Buraya yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    try:
        response = model.generate_content(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.chat_message("assistant").write(response.text)
    except Exception as e:
        st.error(f"Teknik Hata: {e}")
