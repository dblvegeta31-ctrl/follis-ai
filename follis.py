import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="Swozzy AI 2.5 Ultra", page_icon="🚀", layout="centered")

# Anahtar Havuzu (Secrets'tan çekilir)
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
st.caption("Kesintisiz Veri Hattı | 2026 Güncelliği")
st.divider()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. 2.5 ZEKA MOTORU (GÜÇLENDİRİLMİŞ) ---
def ask_gemini_25(user_query):
    # 10 anahtarı da gerekirse 2 kez dön (toplam 20 deneme)
    for _ in range(len(api_keys) * 2):
        idx = st.session_state.key_index
        current_key = api_keys[idx]
        
        try:
            genai.configure(api_key=current_key)
            
            # En gelişmiş 2.5 seviyesi model
            model = genai.GenerativeModel(
                model_name='gemini-2.0-flash-exp',
                tools=[{'google_search_retrieval': {}}] # CANLI İNTERNET
            )
            
            # Tarih Hatasını Bitiren Kesin Komut
            simdi = datetime.now().strftime("%d %B %Y, %A, Saat: %H:%M:%S")
            full_prompt = (
                f"KİMLİK: Sen Swozzy AI v2.5'sin. \n"
                f"GÜNCEL ZAMAN: {simdi}. \n"
                f"TALİMAT: Aşağıdaki soruyu yanıtlamak için MUTLAKA Google Search kullan. "
                f"Eski verileri unut, sadece bugünün (2026) verilerine odaklan. \n\n"
                f"SORU: {user_query}"
            )
            
            # Yanıtı al
            response = model.generate_content(full_prompt)
            
            if response and response.text:
                return response.text, "SUCCESS"
            else:
                raise Exception("BOŞ_YANIT")
                
        except Exception as e:
            # Hata durumunda anında diğer anahtara zıpla
            st.toast(f"Hat {idx + 1} meşgul, yedek hatta (Hat {((idx + 1) % len(api_keys)) + 1}) geçiliyor...", icon="⚡")
            st.session_state.key_index = (idx + 1) % len(api_keys)
            time.sleep(0.4) # Google spam koruması için milisaniyelik es
            continue
            
    return None, "TIMEOUT"

# --- 4. AKIŞ ---
if prompt := st.chat_input(placeholder="Swozzy'ye bir şeyler sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        container = st.empty()
        with container.container():
            with st.spinner("Swozzy 2.5 interneti tarıyor ve doğruluyor..."):
                answer, status = ask_gemini_25(prompt)
        container.empty()

        if status == "SUCCESS":
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.error("⚠️ Şu an Google sunucuları çok yoğun veya 10 anahtarın saniyelik kotası bitti.")
            st.info("Lütfen 10-15 saniye bekleyip tekrar sormayı deneyin. 2.5 sürümü interneti tararken çok fazla güç harcar.")
