import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="Swozzy AI - v1beta")

# 1. API YAPILANDIRMASI
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("API Anahtarı bulunamadı!")
    st.stop()

# 2. v1beta ve FLASH İÇİN ÖZEL TANIMLAMA
# 404 hatasını kırmak için tam yolu (full path) kullanıyoruz
try:
    # Model adını 'models/gemini-1.5-flash' olarak tam yazıyoruz
    model = genai.GenerativeModel(
        model_name='models/gemini-1.5-flash'
    )
except Exception as e:
    st.error(f"Model Kurulum Hatası: {e}")

st.title("⚡ Swozzy AI (v1beta Flash)")

# 3. SOHBET SİSTEMİ
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

if prompt := st.chat_input("Flash ile konuş..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # v1beta üzerinden üretim denemesi
            response = model.generate_content(prompt)
            if response.text:
                st.write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Hata devam ederse teknik detayı göster
            st.error(f"v1beta/Flash Hatası: {str(e)}")
