import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# --- 1. GÜVENLİ API YAPILANDIRMASI ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Lütfen Streamlit Secrets kısmına GOOGLE_API_KEY ekleyin!")
    st.stop()

# --- 2. MODEL VE TARİH AYARI ---
simdi = datetime.now()
gun_ay_yil = simdi.strftime("%d %m %Y")

# Modeli tanımlıyoruz
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction=f"Senin adın Swozzy AI. Bugünün tarihi {gun_ay_yil} ve biz 2026 yılındayız."
)

# --- 3. SAYFA AYARLARI ---
st.set_page_config(page_title="Swozzy AI", page_icon="🤖")
st.title("🤖 Swozzy AI")
st.caption(f"📅 {gun_ay_yil} | Ücretsiz Sürüm (Limitli)")

# --- 4. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. MESAJLAŞMA ---
if prompt := st.chat_input("Mesajınızı yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Yanıt oluşturma
            response = model.generate_content(prompt)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
        except Exception as e:
            if "429" in str(e):
                st.error("⚠️ Çok hızlı gidiyorsun! Google'ın ücretsiz limitine takıldık. Lütfen 1 dakika bekleyip tekrar dene.")
            else:
                st.error(f"Bir sorun oluştu: {str(e)}")

# --- 6. YAN PANEL ---
with st.sidebar:
    st.write("### Bilgilendirme")
    st.warning("Ücretsiz API kullandığın için Google günde sadece 20-50 soruya izin verir.")
    if st.button("Sohbeti Sıfırla"):
        st.session_state.messages = []
        st.rerun()
