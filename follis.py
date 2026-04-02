import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# --- 1. AYARLAR ---
st.set_page_config(page_title="Swozzy AI 2.5", page_icon="🚀", layout="centered")

api_keys = []
for i in range(1, 11):
    key_name = f"GOOGLE_API_KEY_{i}"
    if key_name in st.secrets:
        api_keys.append(st.secrets[key_name])

if "key_index" not in st.session_state:
    st.session_state.key_index = 0
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 2. ARAYÜZ ---
st.markdown("# 🚀 Swozzy AI v2.5")
st.divider()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. AKILLI CEVAP MOTORU ---
def ask_gemini_balanced(user_query):
    for _ in range(len(api_keys)):
        idx = st.session_state.key_index
        current_key = api_keys[idx]
        
        try:
            genai.configure(api_key=current_key)
            
            # Kelime sayısına göre internet ihtiyacını belirle
            words = user_query.lower().split()
            # Bilgi isteme anahtar kelimeleri veya uzun sorular
            needs_search = len(words) > 4 or any(k in user_query.lower() for k in ["nedir", "kimdir", "haber", "saat", "hava", "kaç"])

            model_config = {"model_name": 'gemini-2.0-flash-exp'}
            if needs_search:
                model_config["tools"] = [{'google_search_retrieval': {}}]
            
            model = genai.GenerativeModel(**model_config)
            
            simdi = datetime.now().strftime("%d %B %Y, %A")
            prompt = (
                f"Sen Swozzy AI v2.5'sin. Bugün: {simdi}. "
                "Arkadaşça, hızlı ve doğru yanıt ver. "
                f"\nKullanıcı: {user_query}"
            )
            
            response = model.generate_content(prompt)
            
            if response and hasattr(response, 'text') and response.text:
                return response.text, "SUCCESS"
            else:
                # Eğer yanıt boşsa diğer anahtara geçmek için hata fırlat
                raise Exception("EmptyResponse")
                
        except:
            st.session_state.key_index = (idx + 1) % len(api_keys)
            time.sleep(0.2)
            continue
            
    return None, "ERROR"

# --- 4. AKIŞ ---
if prompt := st.chat_input(placeholder="Swozzy'ye bir şeyler sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(" "): 
            answer, status = ask_gemini_balanced(prompt)

        if status == "SUCCESS":
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.info("Şu an biraz yoğunum, lütfen tekrar dener misin?")
