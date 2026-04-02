import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- 1. API YAPILANDIRMASI ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Secrets kısmında API anahtarı bulunamadı!")
    st.stop()

# --- 2. MODEL VE TALİMATLAR ---
# Modelin açıklayıcı olması için talimatı güçlendirdik
model = genai.GenerativeModel(
    model_name='models/gemini-1.5-flash',
    system_instruction=(
        "Senin adın Swozzy AI. Versiyonun 2.5-Flash. 2026 yılındayız. "
        "Bir matematik veya mantık sorusu sorulduğunda sadece sonucu verme; "
        "adım adım nasıl çözdüğünü açıkla. Nazik, zeki ve yardımcı ol."
    )
)

# --- 3. SAYFA AYARLARI ---
st.set_page_config(page_title="Swozzy AI", page_icon="🤖")
st.title("🤖 Swozzy AI Asistan")

# --- 4. SOL PANEL (SIDEBAR) ---
with st.sidebar:
    # Sadece senin istediğin o sade yazı
    st.title("2.5-Flash") 
    st.divider()
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
    st.write("Swozzy AI")

# --- 5. SOHBET GEÇMİŞİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. MESAJLAŞMA ---
if prompt := st.chat_input("Swozzy'ye sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Akışı bozmamak için doğrudan yanıt alıyoruz
            response = model.generate_content(prompt)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("Cevap üretilemedi.")
        except Exception as e:
            st.error(f"Hata: {str(e)}")
