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
simdi = datetime.now()
gun_ay_yil = simdi.strftime("%d %m %Y")

# --- 3. MODEL TANIMLAMA ---
# En kararlı ve hızlı çalışan 1.5-flash modelini kullanıyoruz
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=f"Senin adın Swozzy AI. Bugünün tarihi {gun_ay_yil} ve biz 2026 yılındayız. Çok zeki ve hızlı bir asistansın."
)

# --- 4. SAYFA AYARLARI ---
st.set_page_config(page_title="Swozzy AI", page_icon="🤖")
st.title("🤖 Swozzy AI Asistan")

# --- 5. YAN PANEL (SOL TARAF) ---
with st.sidebar:
    st.write(f"📅 **Tarih:** {gun_ay_yil}") # Tarih sadece burada yazacak
    st.write("🚀 **Versiyon:** 2.5-Flash")
    st.divider()
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.write("Swozzy AI v2.5")

# --- 6. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 7. MESAJLAŞMA VE YANIT ÜRETME ---
# Arama yerine "Swozzy'ye sor..." yazısı eklendi
if prompt := st.chat_input("Swozzy'ye sor..."):
    # Kullanıcı mesajını göster
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
                st.warning("Modelden boş yanıt döndü, lütfen tekrar deneyin.")
                
        except Exception as e:
            st.error(f"Bir sorun oluştu. Teknik detay: {str(e)}")
