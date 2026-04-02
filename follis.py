import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="Swozzy AI Ultra", page_icon="⚡")

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
st.title("⚡ Swozzy AI Ultra")
st.divider()

# Geçmiş mesajları ekrana bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. CEVAP MOTORU (EN SAĞLAM VERSİYON) ---
def ask_gemini(user_query):
    # Anahtar sayısı kadar deneme yap
    for _ in range(len(api_keys)):
        idx = st.session_state.key_index
        current_key = api_keys[idx]
        
        try:
            genai.configure(api_key=current_key)
            
            # NOT: Eğer hala cevap gelmezse 'gemini-1.5-flash' olarak değiştirebilirsin
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            simdi = datetime.now().strftime("%d %B %Y, %A")
            # Modele kimliğini ve bugünün tarihini net bir şekilde söylüyoruz
            system_prompt = f"Sen Swozzy AI v2.5 sürümüsün. Bugünün tarihi: {simdi}. Her türlü soruya samimi ve doğru cevap ver."
            
            response = model.generate_content(f"{system_prompt}\n\nKullanıcı: {user_query}")
            
            if response and response.text:
                return response.text, "SUCCESS"
            else:
                raise Exception("Empty")

        except Exception:
            # Hata olduğunda sessizce sonraki anahtara geç
            st.session_state.key_index = (idx + 1) % len(api_keys)
            continue
                
    return None, "ERROR"

# --- 5. AKIŞ ---
if prompt := st.chat_input("Swozzy'ye bir şeyler sor..."):
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Asistan cevabı
    with st.chat_message("assistant"):
        loading = st.empty()
        with loading.container():
            with st.spinner(" "): 
                answer, status = ask_gemini(prompt)
        loading.empty()

        if status == "SUCCESS":
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.error("Şu an yanıt verilemiyor. Lütfen anahtarlarını kontrol et veya biraz bekle.")
