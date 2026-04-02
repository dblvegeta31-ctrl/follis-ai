import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# --- 1. AYARLAR ---
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
st.caption("Kesintisiz 2.5 Hattı | Google Search Aktif")
st.divider()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. 2.5 MOTORU (AGRESİF ROTASYON) ---
def ask_gemini_25(user_query):
    # 10 anahtarı da gerekirse defalarca tara
    for attempt in range(len(api_keys) * 2): 
        idx = st.session_state.key_index
        current_key = api_keys[idx]
        
        try:
            genai.configure(api_key=current_key)
            
            # Sadece 2.5 (2.0-flash-exp) ve İnternet Erişimi
            model = genai.GenerativeModel(
                model_name='gemini-2.0-flash-exp',
                tools=[{'google_search_retrieval': {}}]
            )
            
            simdi = datetime.now().strftime("%d %B %Y, %A, %H:%M:%S")
            prompt = (
                f"Sistem: Sen Swozzy AI v2.5'sin. Bugün: {simdi}. "
                "MUTLAKA Google Search kullanarak en güncel ve doğru bilgiyi ver. "
                f"Soru: {user_query}"
            )
            
            response = model.generate_content(prompt)
            
            if response and response.text:
                return response.text, "SUCCESS"
                
        except Exception as e:
            err = str(e).upper()
            # Eğer kota dolduysa (429) veya başka hata varsa anında sonraki anahtara geç
            st.toast(f"Hat: {idx + 1} yoğun, diğerine bağlanılıyor...", icon="⚡")
            st.session_state.key_index = (idx + 1) % len(api_keys)
            # Çok kısa bekle ki Google banlamasın
            time.sleep(0.3)
            continue
            
    return None, "LIMIT"

# --- 4. AKIŞ ---
if prompt := st.chat_input(placeholder="Swozzy'ye bir şeyler sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        loading = st.empty()
        with loading.container():
            with st.spinner("Swozzy 2.5 interneti tarıyor ve doğruluyor..."):
                answer, status = ask_gemini_25(prompt)
        loading.empty()

        if status == "SUCCESS":
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.error("⚠️ 10 anahtarın da saniyelik kotası tükendi! Google Search çok güç harcıyor. Lütfen 15 saniye sonra tekrar basın.")
