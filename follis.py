import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# --- 1. AYARLAR VE ANAHTAR HAVUZU ---
st.set_page_config(page_title="Swozzy AI Ultra", page_icon="⚡", layout="centered")

# Secrets içindeki GOOGLE_API_KEY_1'den 11'e kadar olanları tara
api_keys = []
for i in range(1, 12):
    key_name = f"GOOGLE_API_KEY_{i}"
    if key_name in st.secrets:
        api_keys.append(st.secrets[key_name])

# Anahtar bulunamazsa durdur
if not api_keys:
    st.error("⚠️ Hata: API anahtarları bulunamadı! Lütfen Streamlit Secrets kısmına GOOGLE_API_KEY_1...11 şeklinde ekleme yapın.")
    st.stop()

# Hangi anahtarda kaldığımızı session_state ile takip et
if "key_index" not in st.session_state:
    st.session_state.key_index = 0

# --- 2. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("⚡ Swozzy AI Ultra")
st.caption("2026 Sürümü | 11 Kat Daha Güçlü")
st.divider()

# Mesajları ekrana yansıt
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. AKILLI CEVAP ÜRETME FONKSİYONU ---
def get_ai_response(user_input):
    """Bozuk anahtarları atlar ve kota bitene kadar döner."""
    for _ in range(len(api_keys)):
        current_key = api_keys[st.session_state.key_index]
        try:
            genai.configure(api_key=current_key)
            
            # Güncel Tarih ve Sistem Talimatı
            simdi = datetime.now().strftime("%d %m %Y")
            model = genai.GenerativeModel(
                model_name='gemini-2.5-flash',
                system_instruction=f"Adın Swozzy AI. 2026 yılındayız. Bugün: {simdi}."
            )
            
            response = model.generate_content(user_input)
            return response.text, None
            
        except Exception as e:
            err = str(e).upper()
            # Eğer anahtar geçersiz (Expired), yanlış (Invalid) veya kota doluysa (429)
            if "EXPIRED" in err or "INVALID" in err or "429" in err or "API_KEY_INVALID" in err:
                # Bir sonraki anahtara geç ve tekrar dene
                st.session_state.key_index = (st.session_state.key_index + 1) % len(api_keys)
                continue
            else:
                # Beklenmedik başka bir hata varsa dur
                return None, str(e)
                
    return None, "LIMIT_REACHED"

# --- 4. MESAJLAŞMA MOTORU ---
if prompt := st.chat_input("Swozzy AI'ya bir şeyler yaz..."):
    # Kullanıcı mesajı
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Asistan yanıtı
    with st.chat_message("assistant"):
        loading_placeholder = st.empty()
        
        # Düşünüyorum yazısını göster
        with loading_placeholder.container():
            with st.spinner("Düşünüyorum..."):
                answer, error_detail = get_ai_response(prompt)
        
        # İşlem bitince "Düşünüyorum..." yazısını SİL
        loading_placeholder.empty()

        if answer:
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        elif error_detail == "LIMIT_REACHED":
            # Tüm anahtarlar dolduğunda geri sayım yap
            timer_box = st.empty()
            for i in range(60, 0, -1):
                timer_box.error(f"⚠️ Çok yoğunum! Limitlerin sıfırlanması için {i} saniye beklemelisin...")
                time.sleep(1)
            timer_box.empty()
            st.info("Süre doldu, şimdi tekrar sorabilirsin!")
        else:
            st.error(f"❌ Teknik bir sorun oluştu: {error_detail}")

# --- 5. YAN PANEL ---
with st.sidebar:
    st.title("Swozzy AI")
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.caption("© 2026 Swozzy")
