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

# --- 3. ZEKA MOTORU (SESSİZ VE İNATÇI) ---
def ask_gemini_25(user_query):
    # 10 anahtarı sessizce dön
    for _ in range(len(api_keys) * 2):
        idx = st.session_state.key_index
        current_key = api_keys[idx]
        
        try:
            genai.configure(api_key=current_key)
            model = genai.GenerativeModel(
                model_name='gemini-2.0-flash-exp',
                tools=[{'google_search_retrieval': {}}]
            )
            
            simdi = datetime.now().strftime("%d %B %Y, %H:%M")
            prompt = (
                f"Sistem: Sen Swozzy AI v2.5'sin. Bugünün tarihi: {simdi}. "
                "Google Search kullanarak en güncel veriyi bul ve tarafsızca yanıtla. "
                f"\nSoru: {user_query}"
            )
            
            response = model.generate_content(prompt)
            
            if response and hasattr(response, 'text') and response.text:
                return response.text, "SUCCESS"
                
        except:
            # Hata olduğunda hiçbir şey yazmadan sonraki anahtara geç
            st.session_state.key_index = (idx + 1) % len(api_keys)
            time.sleep(0.5)
            continue
            
    return None, "FAILED"

# --- 4. AKIŞ ---
if prompt := st.chat_input(placeholder="Swozzy'ye bir şeyler sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        container = st.empty()
        with container.container():
            with st.spinner(" "): # Spinner metnini boş bıraktım, sadece animasyon döner
                answer, status = ask_gemini_25(prompt)
        container.empty()

        if status == "SUCCESS":
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.warning("Şu an yanıt oluşturulamıyor, lütfen kısa bir süre sonra tekrar deneyin.")
