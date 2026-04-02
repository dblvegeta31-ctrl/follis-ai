import streamlit as st
import google.generativeai as genai

# --- 1. AYARLAR VE API YAPILANDIRMASI ---
# Kendi API anahtarını buraya yapıştır
API_KEY = "AIzaSyC8oymUWa1yMICFe0EL0DBDnOMX6Htr7Hk" 
genai.configure(api_key=API_KEY)

# Gemini 2.5 Modelini Tanımla
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 2. SAYFA TASARIMI (STANDART AYDINLIK TEMA) ---
st.set_page_config(page_title="Swozzy AI 2.5", page_icon="⚡", layout="centered")

st.title("🚀 Swozzy AI v2.5")
st.subheader("Akıllı Yapay Zeka Asistanı")
st.divider()

# --- 3. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajları ekranda göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. MESAJLAŞMA VE AKIŞ (STREAM) MODU ---
if prompt := st.chat_input("Bir şeyler yaz..."):
    # Kullanıcı mesajını kaydet ve göster
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Yapay zeka yanıt alanı
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # Yapay zeka cevabını üretirken donmayı engelleyen akış
            response = model.generate_content(prompt, stream=True)
            
            for chunk in response:
                full_response += chunk.text
                # Yazma efekti (imleç) ekleyerek ekrana bas
                response_placeholder.markdown(full_response + "▌")
            
            # Tamamlanmış hali göster
            response_placeholder.markdown(full_response)
            
            # Cevabı hafızaya al
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Hata oluştu: {e}")

# --- 5. YAN PANEL (SIDEBAR) ---
with st.sidebar:
    st.title("⚙️ Ayarlar")
    st.write("Model: **Gemini 2.5 Flash**")
    
    if st.button("Sohbeti Sıfırla"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.write("Swozzy AI © 2026")
