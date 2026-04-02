import streamlit as st
import google.generativeai as genai

# --- 1. API AYARI ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("API Anahtarı Bulunamadı!")
    st.stop()

# --- 2. MODEL TANIMLAMA (Hata Önleyici Önbellek ile) ---
@st.cache_resource
def get_model():
    # En güvenli model ismini kullanıyoruz
    return genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction="Adın Swozzy AI. 2.5-Flash sürümüsün. Matematik sorularını adım adım çöz."
    )

model = get_model()

# --- 3. ARAYÜZ AYARLARI ---
st.set_page_config(page_title="Swozzy AI", page_icon="🤖")

# Sidebar (Sol Menü)
with st.sidebar:
    st.header("2.5-Flash")
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

st.title("🤖 Swozzy AI")

# --- 4. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları yazdırırken "key" kullanarak çakışmaları önleyelim
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. MESAJ GÖNDERME ---
if prompt := st.chat_input("Swozzy'ye sor..."):
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Yanıt üretme
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            if response and response.text:
                answer = response.text
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error("Yanıt alınamadı.")
        except Exception as e:
            st.error(f"Hata: {str(e)}")
