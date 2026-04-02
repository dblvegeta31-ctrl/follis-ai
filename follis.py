import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- 1. 11'Lİ API ANAHTAR HAVUZU ---
api_keys = []
for i in range(1, 12):
    key_name = f"GOOGLE_API_KEY_{i}"
    if key_name in st.secrets:
        api_keys.append(st.secrets[key_name])

if not api_keys:
    st.error("Sistem yapılandırması eksik (API Keys).")
    st.stop()

# Aktif anahtar sırasını hafızada tut
if "key_index" not in st.session_state:
    st.session_state.key_index = 0

# --- 2. SAYFA AYARLARI ---
st.set_page_config(page_title="Swozzy AI", page_icon="⚡", layout="centered")

# --- 3. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Başlık ve Arayüz
st.title("⚡ Swozzy AI")
st.divider()

# Mesaj geçmişini göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. CEVAP ÜRETME FONKSİYONU ---
def generate_ai_response(user_prompt):
    # Tüm anahtarları sırayla dene
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
            return response.text
            
        except Exception:
            # Hata (Kota vb.) durumunda bir sonraki anahtara geç
            st.session_state.key_index = (st.session_state.key_index + 1) % len(api_keys)
            continue 
            
    return None

# --- 5. MESAJLAŞMA AKIŞI ---
if prompt := st.chat_input("Bir şeyler yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Kullanıcı anahtar değişimini görmesin diye sade bir yükleniyor simgesi
        with st.spinner("Düşünüyorum..."):
            answer = generate_ai_response(prompt)
            
            if answer:
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error("Şu an çok yoğunum, lütfen 1 dakika sonra tekrar deneyin.")

# --- 6. YAN PANEL (SADELEŞTİRİLMİŞ) ---
with st.sidebar:
    st.title("Swozzy AI")
    st.write("Versiyon 2.5")
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.caption("© 2026 Swozzy")
