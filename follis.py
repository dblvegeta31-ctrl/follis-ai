import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="Swozzy AI 2.5 Ultra", page_icon="🚀", layout="centered")

# Anahtarları yükle
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
st.markdown("# 🚀 Swozzy AI v2.5 Ultra")
st.caption("Gelişmiş Arama ve Doğrulama Hattı")
st.divider()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. 2.5 MOTORU (DİRENÇLİ MOD) ---
def ask_gemini_25(user_query):
    # Anahtar havuzunu 2 tur dönecek kadar inatçı yapıyoruz
    for attempt in range(len(api_keys) * 2):
        idx = st.session_state.key_index
        current_key = api_keys[idx]
        
        try:
            genai.configure(api_key=current_key)
            
            # En üst segment model (2.5 gücü)
            model = genai.GenerativeModel(
                model_name='gemini-2.0-flash-exp',
                tools=[{'google_search_retrieval': {}}]
            )
            
            simdi = datetime.now().strftime("%d %B %Y, %A, %H:%M")
            # Modele kesin talimat
            full_prompt = (
                f"Sistem Talimatı: Sen Swozzy AI v2.5 sürümüsün. "
                f"Şu anki gerçek zaman: {simdi}. "
                "MUTLAKA Google Search aracını kullanarak en güncel bilgiyi bul ve tarafsızca aktar. "
                f"\n\nKullanıcı Sorusu: {user_query}"
            )
            
            # Yanıtı alırken güvenli bir bekleme ekle
            response = model.generate_content(full_prompt)
            
            if response and response.text:
                return response.text, "SUCCESS"
                
        except Exception as e:
            # Hata tipine göre kullanıcıyı bilgilendir
            err_msg = str(e).upper()
            st.toast(f"Hat {idx + 1} yanıt vermedi, sonrakine geçiliyor...", icon="⚡")
            
            # Bir sonraki anahtara geç
            st.session_state.key_index = (idx + 1) % len(api_keys)
            time.sleep(0.5) # Google'ın spam filtresine takılmamak için
            continue
            
    return None, "ALL_FAILED"

# --- 4. MESAJLAŞMA AKIŞI ---
if prompt := st.chat_input(placeholder="Swozzy'ye bir şeyler sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        loading_placeholder = st.empty()
        with loading_placeholder.container():
            with st.spinner("2.5 Motoru interneti tarıyor (Bu işlem 5-10 sn sürebilir)..."):
                answer, status = ask_gemini_25(prompt)
        loading_placeholder.empty()

        if status == "SUCCESS":
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.error("⚠️ Şu an tüm anahtarlar 'Cevap Bulunamadı' veya 'Limit Doldu' hatası veriyor.")
            st.info("İpucu: Ücretsiz kotalar 60 saniyede bir sıfırlanır. Lütfen biraz bekleyip tekrar deneyin.")
