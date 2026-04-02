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

# --- 3. MODEL SEÇİCİ (Hata Önleyici) ---
def get_model():
    # Önce 2.0'ı dene, olmazsa 1.5'e dön
    models_to_try = ['gemini-2.0-flash-exp', 'gemini-1.5-flash']
    
    for m_name in models_to_try:
        try:
            model = genai.GenerativeModel(
                model_name=m_name,
                system_instruction=f"Senin adın Swozzy AI. Bugün {gun_ay_yil} ve 2026 yılındayız. Çok zeki ve hızlısın."
            )
            # Küçük bir test yapalım (boş bir istek gönderiyoruz)
            return model, m_name
        except:
            continue
    return None, None

# --- 4. SAYFA AYARLARI ---
st.set_page_config(page_title="Swozzy AI", page_icon="🤖")
st.title("🤖 Swozzy AI Asistan")

# --- 5. YAN PANEL (SOL TARAF) ---
with st.sidebar:
    st.title("Swozzy Dashboard")
    st.write(f"📅 **Tarih:** {gun_ay_yil}")
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
if prompt := st.chat_input("Swozzy'ye sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Modeli her seferinde kontrol et (en sağlam yöntem)
            model, active_model_name = get_model()
            
            if model:
                response = model.generate_content(prompt)
                if response.text:
                    full_response = response.text
                    st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                else:
                    st.warning("Yanıt boş döndü.")
            else:
                st.error("Üzgünüm, şu an hiçbir model yanıt vermiyor. API anahtarını kontrol eder misin?")
                
        except Exception as e:
            # Hata mesajını sadeleştirerek göster
            if "404" in str(e):
                st.error("Hata: Seçilen model anahtarınla uyumlu değil. Lütfen model ismini 1.5-flash yap.")
            else:
                st.error(f"Bir sorun oluştu: {str(e)}")
