import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="Swozzy AI 2.5 Ultra", page_icon="🚀", layout="centered")

# --- 2. 10'LU ANAHTAR HAVUZU ---
api_keys = []
for i in range(1, 11):
    key_name = f"GOOGLE_API_KEY_{i}"
    if key_name in st.secrets:
        api_keys.append(st.secrets[key_name])

if "key_index" not in st.session_state:
    st.session_state.key_index = 0
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. ARAYÜZ ---
st.title("🚀 Swozzy AI v2.5 Ultra")
st.caption("Gerçek Zamanlı Veri & Google Search Entegrasyonu")
st.divider()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. AKILLI CEVAP MOTORU (2.5 HIZINDA VE GÜNCEL) ---
def ask_gemini(user_query):
    for _ in range(len(api_keys)):
        current_key = api_keys[st.session_state.key_index]
        try:
            genai.configure(api_key=current_key)
            
            # GOOGLE SEARCH (İnternet Erişimi) AKTİF EDİLDİ
            # Bu araç sayesinde model "bilmiyorum" demez, internete bakıp doğrular.
            model = genai.GenerativeModel(
                model_name='gemini-2.0-flash-exp', # Mevcut en gelişmiş zeka
                tools=[{'google_search_retrieval': {}}] 
            )
            
            # Tarih Hatasını Önleyen Özel Komut
            simdi = datetime.now().strftime("%d %B %Y, %A, Saat: %H:%M")
            system_prompt = f"""
            Sen Swozzy AI v2.5'sin. Bugünün kesin ve gerçek tarihi: {simdi}. 
            ASLA eski bilgi verme. Eğer emin değilsen mutlaka internetten (Google Search) kontrol et.
            Tarihleri ve güncel olayları milimetrik doğrulukla söyle.
            """
            
            response = model.generate_content(f"{system_prompt}\n\nKullanıcı Sorusu: {user_query}")
            
            if response and response.text:
                return response.text, "SUCCESS"
        
        except Exception as e:
            err = str(e).upper()
            st.toast(f"Anahtar {st.session_state.key_index + 1} atlanıyor...", icon="⏳")
            st.session_state.key_index = (st.session_state.key_index + 1) % len(api_keys)
            continue
                
    return None, "LIMIT"

# --- 5. MESAJLAŞMA AKIŞI ---
if prompt := st.chat_input("2026 yılına dair güncel bir şey sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown
