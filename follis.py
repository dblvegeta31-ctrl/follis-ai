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
simdi = datetime.now()
gun_ay_yil = simdi.strftime("%d %m %Y")

# 404 hatasını önlemek için en güvenli model yolu
model = genai.GenerativeModel(
    model_name='models/gemini-1.5-flash',
    system_instruction=f"Senin adın Swozzy AI. Versiyonun 2.5-Flash. Bugünün tarihi {gun_ay_yil} ve biz 2026 yılındayız. Çok zeki ve hızlı bir asistansın."
)

# --- 3. SAYFA AYARLARI ---
st.set_page_config(page_title="Swozzy AI", page_icon="🤖")
st.title("🤖 Swozzy AI Asistan")

# --- 4. YAN PANEL (SIDEBAR) ---
with st.sidebar:
    # Sol kenarda sadece bu yazacak
    st.title("2.5-Flash")
    st.divider()
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
    st.write("Swozzy AI")

# --- 5. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. MESAJLAŞMA VE YANIT ---
if prompt := st.chat_input("Swozzy'ye sor..."):
    # Kullanıcı mesajı
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Yanıt üretme
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            if response.text:
                full_response = response.text
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.warning("Boş yanıt döndü.")
        except Exception as e:
            st.error(f"Bir sorun oluştu: {str(e)}")
