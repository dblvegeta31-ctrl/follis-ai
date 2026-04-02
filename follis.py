import streamlit as st
import google.generativeai as genai

# --- 1. YAPILANDIRMA ---
# Kendi API anahtarını buraya yapıştır
API_KEY = "AIzaSyAHRwxMLFwEri593oYdMMCdCJ1_pECKyeA" 
genai.configure(api_key=API_KEY)

# --- 2. MODEL SEÇİMİ ---
# 2026'nın en güncel modellerini sırayla dener, bulamazsa hata vermez
def get_working_model():
    # Denemek istediğin modeller (En yeni en üstte)
    check_list = [
        'models/gemini-2.5-flash', 
        'models/gemini-1.5-flash', 
        'models/gemini-pro'
    ]
    
    try:
        # Senin API anahtarının izin verdiği gerçek modelleri listele
        allowed_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Eğer listede 2.5 varsa direkt onu al
        for target in check_list:
            if target in allowed_models or target.replace('models/', '') in allowed_models:
                return target
        return allowed_models[0] # Hiçbiri yoksa listedeki ilkini al
    except:
        return 'models/gemini-1.5-flash' # Hata çıkarsa güvenli liman

target_model = get_working_model()
model = genai.GenerativeModel(target_model)

# --- 3. SAYFA AYARLARI ---
st.set_page_config(page_title="Swozzy AI", page_icon="⚡", layout="centered")

# Sayfa Başlığı
st.title("🤖 Swozzy AI Asistan")
st.caption(f"Şu an aktif olan model: {target_model}")
st.divider()

# --- 4. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajları ekranda göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. MESAJLAŞMA MANTIĞI ---
if prompt := st.chat_input("Bana bir soru sor..."):
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Yapay zeka cevabı üretme
    with st.chat_message("assistant"):
        status_text = st.empty()
        status_text.markdown(" *Düşünüyorum...*")
        
        try:
            # API'den yanıt al
            response = model.generate_content(prompt)
            final_answer = response.text
            
            # Cevabı yazdır
            status_text.markdown(final_answer)
            
            # Hafızaya kaydet
            st.session_state.messages.append({"role": "assistant", "content": final_answer})
            
        except Exception as e:
            status_text.empty()
            st.error(f"Hata oluştu: {e}")

# --- 6. YAN PANEL (SIDEBAR) ---
with st.sidebar:
    st.header("Swozzy AI Kontrol")
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
    st.write("---")
    st.info("Bu uygulama Streamlit ve Google Gemini 2.5 altyapısıyla çalışmaktadır.")