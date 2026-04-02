import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="Swozzy AI Ultra", page_icon="⚡")

# --- 2. ANAHTAR HAVUZU (MAX 10) ---
api_keys = []
for i in range(1, 11):
    key_name = f"GOOGLE_API_KEY_{i}"
    if key_name in st.secrets:
        api_keys.append(st.secrets[key_name])

# Gerekli değişkenleri tanımla
if "key_index" not in st.session_state:
    st.session_state.key_index = 0
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. ARAYÜZ ---
st.title("⚡ Swozzy AI Ultra")
st.divider()

# Mesaj geçmişini ekrana bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. CEVAP MOTORU ---
def ask_gemini(user_query):
    # Toplam anahtar sayısı kadar deneme yap
    for _ in range(len(api_keys)):
        current_key = api_keys[st.session_state.key_index]
        try:
            genai.configure(api_key=current_key)
            
            # En yüksek kotalı model 1.5-flash
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            response = model.generate_content(user_query)
            
            if response and response.text:
                return response.text, "SUCCESS"
            else:
                raise Exception("BOŞ_CEVAP")

        except Exception as e:
            err = str(e).upper()
            # 429: Kota doldu, 400/INVALID: Anahtar bozuk
            if "429" in err or "INVALID" in err or "EXPIRED" in err or "BOŞ_CEVAP" in err:
                st.toast(f"Anahtar {st.session_state.key_index + 1} atlanıyor...", icon="⏳")
                # Bir sonraki anahtara geç (mod alma ile başa döner)
                st.session_state.key_index = (st.session_state.key_index + 1) % len(api_keys)
                continue
            else:
                # Beklenmedik başka bir hata varsa bildir ve bir sonrakine geç
                st.toast(f"Hata oluştu: {err[:20]}", icon="❌")
                st.session_state.key_index = (st.session_state.key_index + 1) % len(api_keys)
                continue
                
    return None, "LIMIT"

# --- 5. MESAJLAŞMA AKIŞI ---
if prompt := st.chat_input("Mesajınızı buraya yazın..."):
    # Kullanıcı mesajını kaydet ve göster
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Asistan yanıt alanı
    with st.chat_message("assistant"):
        loading_area = st.empty()
        with loading_area.container():
            with st.spinner("Swozzy AI düşünüyor..."):
                answer, status = ask_gemini(prompt)
        
        loading_area.empty() # Spinner'ı kaldır

        if status == "SUCCESS":
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        elif status == "LIMIT":
            # Tüm anahtarların limit uyarısı
            countdown_area = st.empty()
            for i in range(180, 0, -1):
                countdown_area.error(f"⚠️ Tüm anahtarlar doldu. Google kısıtlaması nedeniyle {i} saniye beklemelisiniz...")
                time.sleep(1)
            countdown_area.empty()
            st.info("Süre doldu. Şimdi tekrar sormayı deneyebilirsin!")
