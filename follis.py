import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# --- 1. 11'Lİ API ANAHTAR HAVUZU ---
api_keys = []
for i in range(1, 12):
    key_name = f"GOOGLE_API_KEY_{i}"
    if key_name in st.secrets:
        api_keys.append(st.secrets[key_name])

if not api_keys:
    st.error("Sistem yapılandırması eksik (API Keys).")
    st.stop()

if "key_index" not in st.session_state:
    st.session_state.key_index = 0

# --- 2. SAYFA AYARLARI ---
st.set_page_config(page_title="Swozzy AI", page_icon="⚡", layout="centered")

# --- 3. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("⚡ Swozzy AI")
st.divider()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. CEVAP ÜRETME FONKSİYONU ---
def generate_ai_response(user_prompt):
    for _ in range(len(api_keys)):
        current_key = api_keys[st.session_state.key_index]
        try:
            genai.configure(api_key=current_key)
            simdi = datetime.now().strftime("%d %m %Y")
            model = genai.GenerativeModel(
                model_name='gemini-2.5-flash',
                system_instruction=f"Adın Swozzy AI. 2026 yılındayız. Bugün: {simdi}."
            )
            response = model.generate_content(user_prompt)
            return response.text, None
            
        except Exception as e:
            if "429" in str(e):
                st.session_state.key_index = (st.session_state.key_index + 1) % len(api_keys)
                continue
            else:
                return None, str(e)
            
    return None, "QUOTA_ALL"

# --- 5. MESAJLAŞMA AKIŞI ---
if prompt := st.chat_input("Bir şeyler yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Yanıt alanı oluşturuluyor
    with st.chat_message("assistant"):
        # "Düşünüyorum..." yazısını sadece işlem sürerken gösteren alan
        status_placeholder = st.empty()
        
        with status_placeholder.container():
            with st.spinner("Düşünüyorum..."):
                answer, error_msg = generate_ai_response(prompt)
        
        # İşlem bittiğinde "Düşünüyorum..." yazısını kaldırıyoruz
        status_placeholder.empty()

        if answer:
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        elif error_msg == "QUOTA_ALL":
            # Geri sayım başladığında "Düşünüyorum" yazısı zaten yukarıda empty() ile silindi
            countdown_placeholder = st.empty()
            for i in range(60, 0, -1):
                countdown_placeholder.error(f"⚠️ Limit doldu! Tekrar denemek için {i} saniye bekleyin...")
                time.sleep(1)
            countdown_placeholder.success("Süre doldu! Şimdi tekrar yazabilirsiniz.")
        else:
            st.error(f"Bir hata oluştu: {error_msg}")

# --- 6. YAN PANEL ---
with st.sidebar:
    st.title("Swozzy AI")
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.caption("© 2026 Swozzy")
