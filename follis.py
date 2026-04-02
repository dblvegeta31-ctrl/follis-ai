import streamlit as st
import google.generativeai as genai

# --- 1. SİSTEM AYARLARI ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Lütfen Secrets kısmına API anahtarını ekleyin!")
    st.stop()

# --- 2. SWOZZY'NİN "BEYİN" AYARLARI ---
# Burada modele senin gibi (Gemini gibi) davranması için derin talimat veriyoruz
model = genai.GenerativeModel(
    model_name='models/gemini-1.5-flash',
    system_instruction=(
        "Senin adın Swozzy AI. Tıpkı Gemini gibi profesyonel, zeki ve empatik bir asistansın. "
        "Matematiksel (EBOB, EKOK vb.) veya mantıksal bir soru geldiğinde: "
        "1. Önce soruyu anladığını belirt. "
        "2. İşlemi adım adım, ilkokul seviyesinde anlatır gibi açıkla. "
        "3. Sonucu en sonda kalın puntoyla belirt. "
        "Asla konudan sapma ve kullanıcıya karşı bir dost gibi davran."
    )
)

# --- 3. GÖRSEL ARAYÜZ (SADE VE ŞIK) ---
st.set_page_config(page_title="Swozzy AI", page_icon="🧠")

# Sol Kenar (Sidebar) - Sadece istediğin o yazı
with st.sidebar:
    st.markdown("# 2.5-Flash")
    st.divider()
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
    st.caption("Swozzy AI Engine v2.5")

st.title("🧠 Swozzy AI")
st.info("Benimle her konuyu konuşabilirsin, özellikle matematik sorularında sana adım adım yardım edebilirim!")

# --- 4. HAFIZA VE SOHBET ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. MESAJLAŞMA MOTORU ---
if prompt := st.chat_input("Swozzy'ye sor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Benim gibi "yazıyor..." hissi vermesi için spinner
        with st.spinner("Düşünüyorum..."):
            try:
                # Modeli çalıştır
                response = model.generate_content(prompt)
                
                if response and response.text:
                    full_text = response.text
                    st.markdown(full_text)
                    st.session_state.messages.append({"role": "assistant", "content": full_text})
                else:
                    st.error("Bir şeyler ters gitti, yanıt alamadım.")
            except Exception as e:
                st.error(f"Teknik bir sorun çıktı: {str(e)}")
