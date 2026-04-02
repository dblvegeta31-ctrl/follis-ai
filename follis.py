import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- 1. GÜVENLİ API YAPILANDIRMASI ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Lütfen Streamlit Secrets kısmına GOOGLE_API_KEY ekleyin!")
    st.stop()

# --- 2. TARİH AYARI ---
# Sistemden gerçek zamanlı tarih alıyoruz
simdi = datetime.now()
gun_ay_yil = simdi.strftime("%d %m %Y")

# --- 3. MODEL TANIMLAMA (2.5 FLASH) ---
# 404 hatasını önlemek için doğrudan çalışan 2.5 modelini kullanıyoruz
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction=f"Senin adın Swozzy AI. Bugünün tarihi {gun_ay_yil} ve biz 2026 yılındayız. Çok zeki ve hızlı bir asistansın."
)

# --- 4. SAYFA AYARLARI ---
st.set_page_config(page_title="Swozzy AI", page_icon="🤖")
st.title("🤖 Swozzy AI Asistan")
st.caption(f"📅 Tarih: {gun_ay_yil} | Versiyon: 2.5-Flash")

# --- 5. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. MESAJLAŞMA VE YANIT ÜRETME ---
if prompt := st.chat_input("Buraya yazın..."):
    # Kullanıcı mesajını göster
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Yanıt üretme
    with st.chat_message("assistant"):
        try:
            # Hata riskini azaltmak için en düz generateContent metodunu kullanıyoruz
            response = model.generate_content(prompt)
            
            if response.text:
                full_response = response.text
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.warning("Modelden boş yanıt döndü, lütfen tekrar deneyin.")
                
        except Exception as e:
            # Hata mesajını daha temiz gösterelim
            st.error(f"Bir sorun oluştu. Teknik detay: {str(e)}")

# --- 7. YAN PANEL ---
with st.sidebar:
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.write("Swozzy AI v2.5")   
