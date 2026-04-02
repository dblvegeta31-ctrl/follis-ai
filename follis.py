import streamlit as st
import google.generativeai as genai

# --- 1. AYARLAR VE API YAPILANDIRMASI ---
# Buraya Google AI Studio'dan aldığın anahtarı yapıştır
API_KEY = "AIzaSyAHRwxMLFwEri593oYdMMCdCJ1_pECKyeA" 
genai.configure(api_key=API_KEY)

# Gemini 2.5 Modelini Tanımla (Senin sisteminde bu model aktif)
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 2. SAYFA TASARIMI ---
st.set_page_config(page_title="Swozzy AI 2.5", page_icon="⚡", layout="centered")

# Görsel stil için küçük bir dokunuş
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Swozzy AI v2.5")
st.subheader("En Güncel Yapay Zeka Deneyimi")
st.divider()

# --- 3. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajları ekrana bas (Sayfa yenilense de gitmez)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. MESAJLAŞMA VE DONMAYI ÖNLEYEN AKIŞ (STREAM) MODU ---
if prompt := st.chat_input("Bir şeyler sor..."):
    # Kullanıcı mesajını göster ve kaydet
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Yapay zeka yanıt alanı
    with st.chat_message("assistant"):
        # Boş bir alan oluşturuyoruz, kelimeler buraya tek tek dolacak
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # stream=True sayesinde yapay zeka düşünürken donmaz, yazdıkça ekrana basar
            response = model.generate_content(prompt, stream=True)
            
            for chunk in response:
                full_response += chunk.text
                # Yazma efekti için imleç ekliyoruz
                response_placeholder.markdown(full_response + "▌")
            
            # Yazma işlemi bittiğinde son hali göster (imleci kaldır)
            response_placeholder.markdown(full_response)
            
            # Cevabı hafızaya kaydet
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Hata: {e}")

# --- 5. YAN PANEL AYARLARI ---
with st.sidebar:
    st.title("⚙️ Kontrol Paneli")
    st.write("Model: **Gemini 2.5 Flash**")
    st.write("Durum: **Çevrimiçi**")
    
    if st.button("Sohbet Geçmişini Sil"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.info("Swozzy AI, 2026'nın en hızlı yapay zeka altyapısını kullanır.")
