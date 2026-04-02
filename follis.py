import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- 1. GÜVENLİ API YAPILANDIRMASI ---
try:
    # API anahtarını Streamlit Secrets'tan çeker
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("Hata: GOOGLE_API_KEY bulunamadı! Lütfen Streamlit Settings > Secrets kısmına anahtarınızı ekleyin.")
    st.stop()

# --- 2. MODEL VE SİSTEM TALİMATI ---
# Burada robota kim olduğunu ve hangi tarihte olduğumuzu öğretiyoruz
su_an = datetime.now().strftime("%d %B %Y")

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction=f"Senin adın Swozzy AI. 2026 yılında yaşayan, zeki ve yardımsever bir asistansın. Bugünün gerçek tarihi: {su_an}. Kullanıcı sana tarihi sorarsa bu bilgiyi kullan."
)

# --- 3. SAYFA TASARIMI ---
st.set_page_config(page_title="Swozzy AI 2.5", page_icon="⚡", layout="centered")

st.title("🚀 Swozzy AI v2.5")
st.caption(f"📅 Bugün: {su_an} | Model: Gemini 2.5")
st.divider()

# --- 4. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajları ekrana bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. MESAJLAŞMA VE AKIŞ (STREAM) MODU ---
if prompt := st.chat_input("Bana bir şey sor..."):
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
                # Yazma efekti (imleç)
                response_placeholder.markdown(full_response + "▌")
            
            # Son halini göster
            response_placeholder.markdown(full_response)
            
            # Cevabı hafızaya al
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")

# --- 6. YAN PANEL ---
with st.sidebar:
    st.title("⚙️ Ayarlar")
    st.write(f"Durum: **Aktif**")
    if st.button("Sohbeti Sıfırla"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.info("Swozzy AI, güvenli API altyapısı kullanır.")
