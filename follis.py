import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- 1. 11'Lİ API ANAHTAR HAVUZU YAPILANDIRMASI ---
# Secrets kısmından GOOGLE_API_KEY_1'den 11'e kadar olanları toplar
api_keys = []
for i in range(1, 12):
    key_name = f"GOOGLE_API_KEY_{i}"
    if key_name in st.secrets:
        api_keys.append(st.secrets[key_name])

if not api_keys:
    st.error("Hiç API anahtarı bulunamadı! Lütfen Streamlit Secrets kısmına anahtarları ekleyin.")
    st.stop()

# Aktif anahtarın sırasını session_state içinde tut
if "key_index" not in st.session_state:
    st.session_state.key_index = 0

def get_configured_model():
    """Mevcut indexteki anahtarı yapılandırır ve modeli döner"""
    current_key = api_keys[st.session_state.key_index]
    genai.configure(api_key=current_key)
    
    # Güncel tarih bilgisini al
    simdi = datetime.now().strftime("%d %m %Y")
    
    return genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        system_instruction=f"Adın Swozzy AI. 2026 yılındayız. Bugünün tarihi: {simdi}. Sen 11 anahtarlı özel bir sistemle çalışıyorsun."
    )

# --- 2. SAYFA TASARIMI ---
st.set_page_config(page_title="Swozzy AI Ultra 11", page_icon="🔥", layout="centered")

st.title("🔥 Swozzy AI Ultra v11")
st.caption(f"Sistem Durumu: {len(api_keys)} Anahtar Aktif | Mod: Gemini 2.5")
st.divider()

# --- 3. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesaj geçmişini ekrana bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. AKILLI MESAJLAŞMA VE OTOMATİK KOTA GEÇİŞİ ---
if prompt := st.chat_input("Sorunuzu buraya yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_text = ""
        success = False
        
        # Elimizdeki tüm anahtarları sırayla deniyoruz
        for _ in range(len(api_keys)):
            try:
                model = get_configured_model()
                # Yanıtı al
                response = model.generate_content(prompt)
                
                if response.text:
                    full_text = response.text
                    response_placeholder.markdown(full_text)
                    st.session_state.messages.append({"role": "assistant", "content": full_text})
                    success = True
                    break # Başarılı olduysa döngüden çık
                
            except Exception as e:
                # Eğer "Too Many Requests" (429) hatası alırsak anahtar değiştir
                if "429" in str(e):
                    # Bir sonraki anahtara geç (modülo aritmetiği ile başa döner)
                    st.session_state.key_index = (st.session_state.key_index + 1) % len(api_keys)
                    continue 
                else:
                    st.error(f"Hata oluştu: {str(e)}")
                    break
        
        if not success:
            st.error("⚠️ Maalesef 11 anahtarın da dakikalık veya günlük kotası doldu. Lütfen biraz bekleyin.")

# --- 5. YAN PANEL BİLGİLERİ ---
with st.sidebar:
    st.header("⚙️ Sistem Bilgisi")
    st.write(f"Kullanılan Anahtar: **{st.session_state.key_index + 1} / {len(api_keys)}**")
    st.progress((st.session_state.key_index + 1) / len(api_keys))
    
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.info("Bu sürüm 11 farklı API anahtarı ile sınırları zorlar.")
