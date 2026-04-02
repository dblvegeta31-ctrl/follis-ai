import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- 1. 11'Lİ API ANAHTAR HAVUZU ---
api_keys = []
for i in range(1, 12):
    key_name = f"GOOGLE_API_KEY_{i}"
    if key_name in st.secrets:
        api_keys.append(st.secrets[key_name])

if not api_keys:
    st.error("Hiç API anahtarı bulunamadı! Secrets kısmını kontrol edin.")
    st.stop()

# Aktif anahtar sırasını başlat
if "key_index" not in st.session_state:
    st.session_state.key_index = 0

# --- 2. SAYFA AYARLARI ---
st.set_page_config(page_title="Swozzy AI Ultra v11", page_icon="🔥")
st.title("🔥 Swozzy AI Ultra v11")
st.caption(f"Toplam Kapasite: {len(api_keys)} Anahtar | 2026 Güncel Sürüm")

# --- 3. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. ANA FONKSİYON: CEVAP ÜRETME VE ANAHTAR DÖNDÜRME ---
def generate_ai_response(user_prompt):
    """Bütün anahtarları sırayla döner, biri çalışana kadar durmaz."""
    # Toplam anahtar sayısı kadar deneme hakkı veriyoruz
    for _ in range(len(api_keys)):
        current_key = api_keys[st.session_state.key_index]
        try:
            genai.configure(api_key=current_key)
            simdi = datetime.now().strftime("%d %m %Y")
            model = genai.GenerativeModel(
                model_name='gemini-2.5-flash',
                system_instruction=f"Adın Swozzy AI. 2026 yılındayız. Bugün: {simdi}."
            )
            
            response = model.generate_content(user_prompt)
            return response.text # Başarılıysa metni döndür
            
        except Exception as e:
            # Eğer hata kota hatasıysa (429) veya model bulunamadıysa (404/500 vb.)
            # Bir sonraki anahtara geç ve döngü devam etsin
            st.session_state.key_index = (st.session_state.key_index + 1) % len(api_keys)
            continue 
            
    return None # Hiçbir anahtar çalışmadıysa

# --- 5. MESAJLAŞMA AKIŞI ---
if prompt := st.chat_input("Mesajınızı yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"Anahtar {st.session_state.key_index + 1} deneniyor..."):
            answer = generate_ai_response(prompt)
            
            if answer:
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error("⚠️ Maalesef 11 anahtarın tamamı şu an limit aşımında! Lütfen 1 dakika sonra tekrar deneyin.")

# --- 6. YAN PANEL ---
with st.sidebar:
    st.header("Sistem Paneli")
    st.info(f"Şu an aktif kullanılan: {st.session_state.key_index + 1}. Anahtar")
    if st.button("Sohbeti Sıfırla"):
        st.session_state.messages = []
        st.rerun()
