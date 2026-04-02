import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- 1. GÜVENLİ API YAPILANDIRMASI ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Lütfen Streamlit Secrets kısmına GOOGLE_API_KEY ekleyin!")
    st.stop()

# --- 2. TARİH VE MODEL AYARI ---
# Bugünün tarihini alıyoruz
simdi = datetime.now()
gun_ay_yil = simdi.strftime("%d %m %Y")

# Modeli "System Instruction" ile 2026'ya sabitliyoruz
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash', # 2.5 hata verirse 1.5-flash en stabilidir
    system_instruction=f"Senin adın Swozzy AI. Bugünün tarihi {gun_ay_yil} ve biz 2026 yılındayız. Bu bilgiyi asla unutma."
)

# --- 3. SAYFA AYARLARI ---
st.set_page_config(page_title="Swozzy AI", page_icon="🤖")
st.title("🤖 Swozzy AI Asistan")
st.info(f"📅 Sistem Tarihi: {gun_ay_yil} | Yıl: 2026")

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
            # Akış modunu (stream) hata payını azaltmak için kapattım veya kontrol ekledim
            response = model.generate_content(prompt)
            answer = response.text
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Bir sorun oluştu, lütfen tekrar deneyin. Hata: {str(e)}")

# --- 6. TEMİZLEME BUTONU ---
if st.sidebar.button("Sohbeti Temizle"):
    st.session_state.messages = []
    st.rerun()
