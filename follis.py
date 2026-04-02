import streamlit as st
import google.generativeai as genai

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Swozzy AI", page_icon="⚡")

# --- API ANAHTARI KONTROLÜ ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Lütfen Streamlit Secrets kısmına GOOGLE_API_KEY ekleyin!")
    st.stop()

# --- MODEL TANIMLAMA (v1beta ve Flash Uyumlu) ---
# 404 hatasını önlemek için 'latest' takısını kullanıyoruz
try:
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash-latest',
        system_instruction="Senin adın Swozzy AI. 2.5-Flash sürümü gibi davran ve matematik sorularını adım adım çöz."
    )
except Exception as e:
    st.error(f"Model başlatılamadı: {e}")

# --- SOL PANEL (SIDEBAR) ---
with st.sidebar:
    st.title("Swozzy AI")
    st.write("Sürüm: 2.5-Flash (v1beta)")
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

# --- ANA EKRAN ---
st.title("🤖 Swozzy AI Asistan")

# Sohbet geçmişini başlat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Geçmiş mesajları ekrana yazdır
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- MESAJ GÖNDERME VE YANIT ALMA ---
if prompt := st.chat_input("Bir soru sor..."):
    # Kullanıcı mesajını ekle ve göster
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Asistan yanıtını oluştur
    with st.chat_message("assistant"):
        try:
            # Yanıt üretimi
            response = model.generate_content(prompt)
            
            if response.text:
                full_response = response.text
                st.markdown(full_response)
                # Yanıtı hafızaya ekle
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.warning("Model boş bir yanıt döndürdü.")
                
        except Exception as e:
            # 404 veya diğer hataları burada yakalayıp kullanıcıya gösteriyoruz
            st.error(f"Bir hata oluştu: {str(e)}")
            st.info("İpucu: Eğer 404 hatası devam ediyorsa, lütfen Google AI Studio'dan yeni bir API Key alıp Secrets kısmını güncelleyin.")
