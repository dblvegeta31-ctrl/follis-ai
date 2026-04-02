import streamlit as st
import google.generativeai as genai

# --- 1. AYARLAR ---
st.set_page_config(page_title="Swozzy AI", page_icon="🚀")

# Anahtarları Secrets'tan güvenli bir şekilde çek
api_keys = [st.secrets[f"GOOGLE_API_KEY_{i}"] for i in range(1, 11) if f"GOOGLE_API_KEY_{i}" in st.secrets]

if "key_index" not in st.session_state:
    st.session_state.key_index = 0
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 2. GÖRÜNÜM ---
st.title("🚀 Swozzy AI v2.5")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. CEVAP ÜRETİCİ ---
def get_response(user_input):
    # Elimizdeki 10 anahtarı sırayla zorla denetiyoruz
    for _ in range(len(api_keys)):
        idx = st.session_state.key_index
        try:
            genai.configure(api_key=api_keys[idx])
            # En stabil model olan 1.5-flash'ı kullanalım ki "yanıt vermiyor" demesin
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            response = model.generate_content(f"Sen Swozzy AI'sın. Arkadaşça yanıt ver: {user_input}")
            
            if response.text:
                return response.text
        except:
            # Eğer bu anahtar patlarsa, bir sonrakine geç ve döngü devam etsin
            st.session_state.key_index = (idx + 1) % len(api_keys)
            continue
    return "Üzgünüm, şu an tüm hatlarımda bir bağlantı sorunu var. Lütfen biraz sonra tekrar dene."

# --- 4. AKIŞ ---
if prompt := st.chat_input("Swozzy'ye sorun..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Benim (Gemini) zekamı kullanarak cevap üretiliyor
        full_response = get_response(prompt)
        st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
