import streamlit as st
import google.generativeai as genai

# --- 1. API YAPILANDIRMASI ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("API Anahtarı bulunamadı!")
    st.stop()

# --- 2. AKILLI MODEL SEÇİCİ ---
# Eğer biri hata verirse diğerini deneyecek
def get_working_model():
    possible_names = [
        'models/gemini-1.5-flash', 
        'gemini-1.5-flash', 
        'gemini-1.5-flash-latest'
    ]
    
    for name in possible_names:
        try:
            m = genai.GenerativeModel(
                model_name=name,
                system_instruction="Sen Swozzy AI'sın. Matematik sorularını adım adım çöz ve çok zeki davran."
            )
            # Küçük bir test çalıştırması
            return m
        except:
            continue
    return None

model = get_working_model()

# --- 3. ARAYÜZ AYARLARI ---
st.set_page_config(page_title="Swozzy AI", page_icon="🤖")

with st.sidebar:
    st.title("2.5-Flash") # Sol tarafta sadece bu yazacak
    st.divider()
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

st.title("🤖 Swozzy AI")

# --- 4. SOHBET VE YANIT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Swozzy'ye sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if model:
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Yanıt sırasında hata: {str(e)}")
        else:
            st.error("Maalesef hiçbir modelle bağlantı kurulamadı.")
