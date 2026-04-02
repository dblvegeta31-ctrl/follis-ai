import streamlit as st
import google.generativeai as genai

# --- 1. GÜVENLİ API YAPILANDIRMASI ---
# DİKKAT: API anahtarını buraya yazmıyoruz! 
# Streamlit Cloud panelindeki "Settings > Secrets" kısmına eklemelisin.
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Hata: API Anahtarı (Secrets) bulunamadı! Lütfen Streamlit ayarlarından GOOGLE_API_KEY tanımlayın.")
    st.stop()

# Gemini 2.5 Modelini Tanımla
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 2. SAYFA TASARIMI ---
st.set_page_config(page_title="Swozzy AI 2.5", page_icon="⚡", layout="centered")

st.title("🚀 Swozzy AI v2.5")
st.subheader("Güvenli ve Hızlı Yapay Zeka")
st.divider()

# --- 3. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajları ekranda göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. MESAJLAŞMA VE AKIŞ (STREAM) MODU ---
if prompt := st.chat_input("Bir şeyler yaz..."):
    # Kullanıcı mesajını kaydet ve göster
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Yapay zeka yanıt alanı
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # Akış modunda yanıt üretme
            response = model.generate_content(prompt, stream=True)
            
            for chunk in response:
                full_response += chunk.text
                # Yazma efekti
                response_placeholder.markdown(full_response + "▌")
            
            # Son hali göster
            response_placeholder.markdown(full_response)
            
            # Cevabı hafızaya al
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")

# --- 5. YAN PANEL ---
with st.sidebar:
    st.title("⚙️ Ayarlar")
    st.write("Model: **Gemini 2.5 Flash**")
    if st.button("Sohbeti Sıfırla"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.info("Bu sürümde API anahtarı güvenli bölgede (Secrets) saklanmaktadır.")
