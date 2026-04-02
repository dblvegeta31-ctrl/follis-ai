import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# --- 1. HIZLANDIRILMIŞ AYARLAR ---
st.set_page_config(page_title="Swozzy AI 2.5 Turbo", page_icon="⚡", layout="centered")

# Anahtarları havuzdan çek
api_keys = []
for i in range(1, 11):
    key_name = f"GOOGLE_API_KEY_{i}"
    if key_name in st.secrets:
        api_keys.append(st.secrets[key_name])

if "key_index" not in st.session_state:
    st.session_state.key_index = 0
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 2. TEMİZ ARAYÜZ ---
st.markdown("# 🚀 Swozzy AI v2.5 Turbo")
st.divider()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. TURBO MOTOR (SESSİZ VE HIZLI) ---
def ask_gemini_turbo(user_query):
    # Anahtarları çok hızlı bir şekilde dön
    for _ in range(len(api_keys)):
        idx = st.session_state.key_index
        current_key = api_keys[idx]
        
        try:
            genai.configure(api_key=current_key)
            
            # Hız için yapılandırma optimize edildi
            model = genai.GenerativeModel(
                model_name='gemini-2.0-flash-exp',
                tools=[{'google_search_retrieval': {}}]
            )
            
            simdi = datetime.now().strftime("%d %B %Y")
            prompt = f"Sen Swozzy AI v2.5'sin. Bugün {simdi}. Google Search kullanarak en hızlı ve en doğru cevabı ver. Soru: {user_query}"
            
            # Cevap üretimi
            response = model.generate_content(prompt)
            
            if response and hasattr(response, 'text') and response.text:
                return response.text, "SUCCESS"
                
        except:
            # Hata anında hiç beklemeden sonraki anahtara zıpla
            st.session_state.key_index = (idx + 1) % len(api_keys)
            continue
            
    return None, "ERROR"

# --- 4. AKIŞ ---
if prompt := st.chat_input(placeholder="Swozzy'ye bir şeyler sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Boş bir spinner (yazısız) sadece animasyon gösterir
        with st.spinner(" "): 
            answer, status = ask_gemini_turbo(prompt)

        if status == "SUCCESS":
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.error("Şu an yoğunluk var, lütfen bir saniye sonra tekrar deneyin.")
