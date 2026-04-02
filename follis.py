import streamlit as st
import google.generativeai as genai

# --- 1. API AYARI ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Secrets kısmında API anahtarı yok!")
    st.stop()

# --- 2. MODEL TANIMLAMA (0.7.0 UYUMLU) ---
# 404 hatasını bitirmek için en stabil ismi kullanıyoruz
try:
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction="Adın Swozzy AI. 2.5-Flash sürümüsün. Matematik sorularını adım adım çöz."
    )
except Exception as e:
    st.error(f"Model yüklenemedi: {e}")

# --- 3. ARAYÜZ ---
st.set_page_config(page_title="Swozzy AI", page_icon="🤖")

with st.sidebar:
    st.title("2.5-Flash") # Sol taraf sadeleşti
    st.divider()
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

st.title("🤖 Swozzy AI Asistan")

# --- 4. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. MESAJ GÖNDERME ---
if prompt := st.chat_input("Swozzy'ye sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Yanıt alırken hata kontrolleri
            response = model.generate_content(prompt)
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("Cevap boş döndü.")
        except Exception as e:
            st.error(f"Yanıt Hatası: {str(e)}")
