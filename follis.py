import streamlit as st
import google.generativeai as genai

# --- 1. API YAPILANDIRMASI ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("API anahtarı bulunamadı!")
    st.stop()

# --- 2. MODELİ HAZIRLA ---
# 0.7.0 sürümüyle en uyumlu çağırma yöntemi
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="Adın Swozzy AI. Versiyon 2.5-Flash. Matematik sorularını adım adım çöz."
)

# --- 3. ARAYÜZ ---
st.set_page_config(page_title="Swozzy AI")

# Sol Panel (Sidebar)
with st.sidebar:
    st.write("# 2.5-Flash")
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

st.title("🤖 Swozzy AI")

# --- 4. SOHBET SİSTEMİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları listele
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Giriş Kutusu
if prompt := st.chat_input("Swozzy'ye sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            if response.text:
                st.write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Hata oluştu: {e}")
