import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# --- 1. AYARLAR ---
st.set_page_config(page_title="Swozzy AI 2.5", page_icon="🚀")

# Anahtarları Secrets'tan çek
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

# --- 3. İNATÇI CEVAP MOTORU ---
def ask_swozzy_nonstop(user_input):
    # Tüm anahtarları 2 tur döner (Toplam 20 deneme)
    for _ in range(len(api_keys) * 2):
        idx = st.session_state.key_index
        try:
            genai.configure(api_key=api_keys[idx])
            
            # 1.5 Flash en hızlı ve en az meşguliyet uyarısı veren modeldir
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            simdi = datetime.now().strftime("%d %B %Y")
            context = f"Sen Swozzy AI'sın. Bugün {simdi}. Arkadaşça ve kısa yanıt ver."
            
            # API isteğini yap
            response = model.generate_content(f"{context}\n\nSoru: {user_input}")
            
            if response and response.text:
                return response.text
                
        except Exception:
            # Hata varsa (Meşguliyet dahil) HİÇBİR ŞEY YAZMA, diğer anahtara geç
            st.session_state.key_index = (idx + 1) % len(api_keys)
            # Google'ı korumak için milisaniyelik bir ara ver
            time.sleep(0.1)
            continue
            
    return "Şu an tüm dünya genelinde bir yoğunluk var, lütfen 10 saniye sonra tekrar sormayı dene."

# --- 4. AKIŞ ---
if prompt := st.chat_input("Swozzy'ye sorun..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Kullanıcı beklerken sadece boş bir spinner döner
        with st.spinner(""):
            answer = ask_swozzy_nonstop(prompt)
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
