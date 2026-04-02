import streamlit as st
import google.generativeai as genai

# --- 1. SAYFA AYARLARI (JavaScript hatalarını önlemek için en üstte) ---
st.set_page_config(page_title="Swozzy AI", page_icon="⚡", layout="centered")

# --- 2. API VE MODEL YAPILANDIRMASI ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Hata: Streamlit Secrets kısmına 'GOOGLE_API_KEY' eklenmemiş!")
    st.stop()

# 404 hatasını bitiren "v1beta" uyumlu model tanımı
@st.cache_resource
def load_model():
    try:
        # En güncel ve v1beta destekleyen tam model ismi
        return genai.GenerativeModel(
            model_name='models/gemini-1.5-flash-latest',
            system_instruction="Senin adın Swozzy AI. 2.5-Flash sürümüsün. Matematik ve teknik soruları adım adım çözersin."
        )
    except Exception as e:
        st.error(f"Model yüklenirken hata oluştu: {e}")
        return None

model = load_model()

# --- 3. SOHBET GEÇMİŞİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. ARAYÜZ (SIDEBAR) ---
with st.sidebar:
    st.title("Swozzy AI")
    st.subheader("Sürüm: 2.5-Flash")
    if st.button("Sohbeti Sıfırla"):
        st.session_state.messages = []
        st.rerun()

# --- 5. ANA EKRAN ---
st.title("🤖 Swozzy AI Asistan")

# Mesajları ekrana bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı girişi
if prompt := st.chat_input("Swozzy'ye bir şey sor..."):
    # Kullanıcı mesajını kaydet ve göster
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Modelden yanıt al
    with st.chat_message("assistant"):
        try:
            if model:
                # v1beta üzerinden üretim
                response = model.generate_content(prompt)
                
                if response and response.text:
                    output = response.text
                    st.markdown(output)
                    st.session_state.messages.append({"role": "assistant", "content": output})
                else:
                    st.warning("Modelden boş yanıt döndü. API anahtarını kontrol et.")
            else:
                st.error("Model hazır değil.")
        except Exception as e:
            # Buradaki hata 404 ise API Key kesinlikle bu modeli desteklemiyordur
            st.error(f"Ba
