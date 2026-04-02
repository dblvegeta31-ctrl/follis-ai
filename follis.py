import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# --- SAYFA TASARIMI ---
st.set_page_config(page_title="Swozzy AI Ultra", page_icon="⚡")

# --- 10'LU ANAHTAR HAVUZUNU TOPLA ---
api_keys = []
for i in range(1, 11):
    key_name = f"GOOGLE_API_KEY_{i}"
    if key_name in st.secrets:
        api_keys.append(st.secrets[key_name])

if not api_keys:
    st.error("Secrets kısmında hiç anahtar bulunamadı!")
    st.stop()

# Hangi anahtarda kaldığımızı hatırla
if "key_index" not in st.session_state:
    st.session_state.key_index = 0

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- ARAYÜZ ---
st.title("⚡ Swozzy AI Ultra")
st.caption(f"10 Proje Modu Aktif | Toplam Anahtar: {len(api_keys)}")
st.divider()

# Eski mesajları göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- ZEKA MOTORU (ANAHTAR ROTASYONU) ---
def ask_gemini(user_query):
    # Elimizdeki 10 anahtarı da deniyoruz
    for _ in range(len(api_keys)):
        current_key = api_keys[st.session_state.key_index]
        try:
            genai.configure(api_key=current_key)
            
            # Sistem Talimatı ve Model
            simdi = datetime.now().strftime("%d %m %Y")
            model = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                system_instruction=f"Adın Swozzy AI. Yıl 2026. Bugün: {simdi}."
            )
            
            response = model.generate_content(user_query)
            return response.text, "SUCCESS"
            
        except Exception as e:
            error_msg = str(e).upper()
            # Eğer limit (429) veya geçersiz anahtar hatası gelirse bir sonrakine geç
            if "429" in error_msg or "INVALID" in error_msg or "EXPIRED" in error_msg:
                st.session_state.key_index = (st.session_state.key_index + 1) % len(api_keys)
                continue
            else:
                return None, f"HATA: {str(e)}"
                
    return None, "ALL_LIMITS_HIT"

# --- MESAJLAŞMA AKIŞI ---
if prompt := st.chat_input("Buraya yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # "Düşünüyorum" yazısı için geçici kutu
        loading_box = st.empty()
        
        with loading_box.container():
            with st.spinner("Düşünüyorum..."):
                answer, status = ask_gemini(prompt)
        
        # Cevap gelince veya hata olunca "Düşünüyorum" yazısını kaldır
        loading_box.empty()

        if status == "SUCCESS":
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        elif status == "ALL_LIMITS_HIT":
            # Geri sayım
            timer_box = st.empty()
            for i in range(60, 0, -1):
                timer_box.error(f"⏳ 10 anahtarın da limiti doldu! {i} saniye sonra tekrar deneyebilirsin.")
                time.sleep(1)
            timer_box.empty()
        else:
            st.error(status)

# --- YAN PANEL ---
with st.sidebar:
    st.title("Swozzy AI")
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.info(f"Şu anki Aktif Anahtar: {st.session_state.key_index + 1}")
