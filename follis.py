import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Swozzy AI")

# API Yapılandırması
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Secrets kısmında API anahtarı yok!")
    st.stop()

# --- OTOMATİK MODEL SEÇİCİ ---
@st.cache_resource
def get_best_model():
    # 404 hatasını önlemek için mevcut modelleri tara
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            # Önce 1.5 Flash deniyoruz, yoksa herhangi birini alıyoruz
            if 'gemini-1.5-flash' in m.name:
                return genai.GenerativeModel(m.name)
    # Eğer Flash yoksa ilk bulduğunu al
    return genai.GenerativeModel('gemini-pro')

try:
    model = get_best_model()
    st.sidebar.success(f"Aktif Model: {model.model_name}")
except Exception as e:
    st.error(f"Model yüklenemedi: {e}")

st.title("Swozzy AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

if prompt := st.chat_input("Bir şeyler yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    try:
        # 404 riskine karşı doğrudan üretim
        response = model.generate_content(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.chat_message("assistant").write(response.text)
    except Exception as e:
        st.error(f"Hata detayı: {e}")
