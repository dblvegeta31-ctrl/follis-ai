import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="Swozzy AI 2.5 Ultra", page_icon="🚀", layout="centered")

# --- 2. ANAHTAR HAVUZU ---
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
st.markdown("# :streamlit: Swozzy AI v2.5 Ultra")
st.divider()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. AKILLI CEVAP MOTORU (HIZLI ROTASYON) ---
def ask_gemini(user_query):
    # Elimizdeki anahtar sayısı kadar dön
    for attempt in range(len(api_keys)):
        current_key = api_keys[st.session_state.key_index]
        try:
            genai.configure(api_key=current_key)
            
            # KOTA DOSTU YAPILANDIRMA
            # Flash modeli ücretsiz kotada en dayanıklı olanıdır.
            model = genai.GenerativeModel(
                model_name='gemini-1.5-flash', # 2.0-flash-exp çok hızlı kota bitirir, 1.5 daha stabil.
                tools=[{'google_search_retrieval': {}}] 
            )
            
            simdi = datetime.now().strftime("%d %B %Y, %H:%M")
            prompt = f"Tarih: {simdi}. Sen Swozzy AI v2.5'sin. Güncel ve doğru bilgi ver. Soru: {user_query}"
            
            response = model.generate_content(prompt)
            
            if response and response.text:
                return response.text, "SUCCESS"
        
        except Exception as e:
            err = str(e).upper()
            # Eğer hata kota (429) ise hemen diğerine geç
            if "429" in err:
                st.toast(f"Anahtar {st.session_state.key_index + 1} dolu, diğerine geçiliyor...", icon="⏳")
            else:
                st.toast(f"Hata: {err[:20]}", icon="⚠️")
            
            # Sıradaki anahtara geç
            st.session_state.key_index = (st.session_state.key_index + 1) % len(api_keys)
            time.sleep(1) # Google'ı tetiklememek için kısa bekleme
            continue
                
    return None, "LIMIT"

# --- 5. MESAJLAŞMA AKIŞI ---
if prompt := st.chat_input(placeholder="Swozzy'ye bir şeyler sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        loading = st.empty()
        with loading.container():
            with st.spinner("Swozzy yanıtlıyor..."):
                answer, status = ask_gemini(prompt)
        loading.empty()

        if status == "SUCCESS":
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        elif status == "LIMIT":
            st.error("⚠️ Tüm anahtarların dakikalık kotası doldu. Google ücretsiz kullanımda saniyede çok fazla isteğe izin vermez. Lütfen 30 saniye sonra tekrar deneyin.")
