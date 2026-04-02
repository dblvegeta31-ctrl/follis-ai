import streamlit as st
import google.generativeai as genai

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="Swozzy AI", page_icon="⚡")

# --- 2. API YAPILANDIRMASI ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Secrets kısmına GOOGLE_API_KEY eklenmemiş!")
    st.stop()

# --- 3. MODEL TANIMLAMA ---
try:
    # 404 hatasını önlemek için 'models/' öneki ve 'latest' takısı
    model = genai.GenerativeModel(
        model_name='models/gemini-1.5-flash-latest'
    )
except Exception as e:
    st.error(f"Model başlatma hatası: {e}")

# --- 4. SOHBET GEÇMİŞİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 5. ARAYÜZ (SIDEBAR) ---
with st.sidebar:
    st.title("Swozzy AI")
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

# --- 6. ANA EKRAN ---
st.title("🤖 Swozzy AI")

# Mesajları ekrana bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı girişi
if prompt := st.chat_input("Bir şey sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            if response.text:
                ans = response.text
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
        except Exception as e:
            st.error(f"Hata oluştu: {str(e)}")
