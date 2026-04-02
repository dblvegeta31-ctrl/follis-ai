import streamlit as st
import google.generativeai as genai

# --- 1. API YAPILANDIRMASI ---
if "GOOGLE_API_KEY" in st.secrets:
    # API anahtarını tanımla
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Secrets kısmında API anahtarı bulunamadı!")
    st.stop()

# --- 2. MODEL TANIMLAMA (HATA ÖNLEYİCİ) ---
# 404 hatasını geçmek için en sade ve doğrudan ismi kullanıyoruz
try:
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash', # Başına 'models/' eklemeden dene
        system_instruction="Sen Swozzy AI'sın. 2.5-Flash versiyonusun. Matematik sorularını adım adım açıkla."
    )
except Exception as e:
    st.error(f"Model yüklenirken hata: {e}")

# --- 3. ARAYÜZ ---
st.set_page_config(page_title="Swozzy AI", page_icon="🤖")

with st.sidebar:
    st.title("2.5-Flash") # Sol taraf sadece bu
    st.divider()
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

st.title("🤖 Swozzy AI Asistan")

# --- 4. SOHBET SİSTEMİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Swozzy'ye sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # ÖNEMLİ: Bazı durumlarda generate_content hata verirse stream kullanmak çözebilir
            response = model.generate_content(prompt)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("Model boş yanıt döndü.")
        except Exception as e:
            # Eğer yine 404 verirse, kütüphaneyi güncellememiz gerekebilir
            st.error(f"Yanıt Hatası: {str(e)}")
            st.info("İpucu: Eğer 404 devam ediyorsa, 'requirements.txt' dosyana 'google-generativeai>=0.7.0' yazmalısın.")
