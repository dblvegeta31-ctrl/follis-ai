import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="Swozzy AI Ultra", page_icon="⚡", layout="centered")

# --- 2. 10'LU ANAHTAR HAVUZU ---
api_keys = []
for i in range(1, 11):
    key_name = f"GOOGLE_API_KEY_{i}"
    if key_name in st.secrets:
        api_keys.append(st.secrets[key_name])

if not api_keys:
    st.error("⚠️ Hata: Secrets kısmında API anahtarı bulunamadı!")
    st.stop()

# Hangi anahtarda kaldığımızı takip et
if "key_index" not in st.session_state:
    st.session_state.key_index = 0

# Sohbet geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. ARAYÜZ ---
st.title("⚡ Swozzy AI Ultra")
st.caption(f"Aktif Proje Sayısı: {len(api_keys)} | 2026 Versiyon")
st.divider()

# Eski mesajları göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. ZEKA MOTORU (MODEL HATASI DÜZELTİLDİ) ---
def ask_gemini(user_query):
    for _ in range(len(api_keys)):
        current_key = api_keys[st.session_state.key_index]
        try:
            genai.configure(api_key=current_key)
            
            # Tarih bilgisi
            simdi = datetime.now().strftime("%d %m %Y")
            
            # HATA DÜZELTMESİ: Model ismi güncellendi
            # 'gemini-1.5-flash' yerine 'models/gemini-1.5-flash' kullanımı daha garantidir.
            model = genai.GenerativeModel(
                model_name='models/gemini-1.5-flash',
                system_instruction=f"Adın Swozzy AI. Yıl 2026. Bugünün tarihi: {simdi}."
            )
            
            response = model.generate_content(user_query)
            return response.text, "SUCCESS"
            
        except Exception as e:
            err_msg = str(e).upper()
            # Eğer limit (429) veya model bulunamadı (404) hatası gelirse bir sonrakine geç
            if "429" in err_msg or "404" in err_msg or "INVALID" in err_msg:
                st.session_state.key_index = (st.session_state.key_index + 1) % len(api_keys)
                continue
            else:
                return None, f"Teknik Hata: {str(e)}"
                
    return None, "ALL_LIMITS_HIT"

# --- 5. MESAJLAŞMA AKIŞI ---
if prompt := st.chat_input("Mesajınızı yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        loading_box = st.empty()
        
        with loading_box.container():
            with st.spinner("Düşünüyorum..."):
                answer, status = ask_gemini(prompt)
        
        loading_box.empty()

        if status == "SUCCESS":
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        elif status == "ALL_LIMITS_HIT":
            timer_box = st.empty()
            for i in range(60, 0, -1):
                timer_box.error(f"⏳ Tüm projelerin limiti doldu! {i} saniye sonra tekrar deneyebilirsin.")
                time.sleep(1)
            timer_box.empty()
            st.info("Limitler sıfırlandı, şimdi tekrar yazabilirsin.")
        else:
            st.error(status)

# --- 6. YAN PANEL ---
with st.sidebar:
    st.title("Swozzy AI")
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.info(f"Kullanılan Aktif Anahtar: {st.session_state.key_index + 1}")
    st.caption("
