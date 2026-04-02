import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# --- 1. 11'Lİ API ANAHTAR HAVUZU YAPILANDIRMASI ---
# Secrets kısmından GOOGLE_API_KEY_1'den 11'e kadar olanları listeye alıyoruz
api_keys = []
for i in range(1, 12):
    key_name = f"GOOGLE_API_KEY_{i}"
    if key_name in st.secrets:
        api_keys.append(st.secrets[key_name])

if not api_keys:
    st.error("Sistem Hatası: Hiç API anahtarı bulunamadı. Lütfen Secrets ayarlarını kontrol edin.")
    st.stop()

# Hangi anahtarda kaldığımızı hatırlaması için session_state
if "key_index" not in st.session_state:
    st.session_state.key_index = 0

# --- 2. SAYFA AYARLARI ---
st.set_page_config(page_title="Swozzy AI Ultra", page_icon="⚡", layout="centered")

# --- 3. SOHBET HAFIZASI ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("⚡ Swozzy AI Ultra")
st.caption("2026 Güncel Sürüm | 11x Güçlendirilmiş Altyapı")
st.divider()

# Eski mesajları ekrana bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. AKILLI CEVAP ÜRETİCİ (ANAHTAR DÖNDÜRÜCÜ) ---
def get_ai_response(user_input):
    # Elimizdeki anahtar sayısı kadar deneme yapma hakkı veriyoruz
    for _ in range(len(api_keys)):
        current_key = api_keys[st.session_state.key_index]
        try:
            genai.configure(api_key=current_key)
            
            # Tarih ve Model Ayarı
            simdi = datetime.now().strftime("%d %m %Y")
            model = genai.GenerativeModel(
                model_name='gemini-2.5-flash',
                system_instruction=f"Senin adın Swozzy AI. 2026 yılındayız. Bugünün tarihi: {simdi}."
            )
            
            response = model.generate_content(user_input)
            return response.text, None # Başarılıysa metni dön
            
        except Exception as e:
            err_msg = str(e).upper()
            # Eğer anahtar geçersizse (Expired/Invalid) veya kota dolmuşsa (429)
            if "EXPIRED" in err_msg or "INVALID" in err_msg or "429" in err_msg:
                # Bir sonraki anahtara geç ve döngüyü devam ettir
                st.session_state.key_index = (st.session_state.key_index + 1) % len(api_keys)
                continue
            else:
                # Başka bir teknik hata varsa bildir
                return None, str(e)
                
    return None, "ALL_KEYS_LIMIT" # 11 anahtarın tamamı başarısız olduysa

# --- 5. MESAJLAŞMA AKIŞI ---
if prompt := st.chat_input("Swozzy AI'ya bir şeyler sor..."):
    # Kullanıcı mesajını kaydet ve göster
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Yanıt beklerken "Düşünüyorum..." yazısı için geçici alan
        loading_area = st.empty()
        
        with loading_area.container():
            with st.spinner("Düşünüyorum..."):
                answer, error = get_ai_response(prompt)
        
        # İşlem bitince spinner'ı kaldır
        loading_area.empty()

        if answer:
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        elif error == "ALL_KEYS_LIMIT":
            # Tüm anahtarlar dolduğunda geri sayım başlar
            countdown_area = st.empty()
            for i in range(60, 0, -1):
                countdown_area.error(f"⚠️ Limitler doldu! Tekrar denemek için {i} saniye bekleyin...")
                time.sleep(1)
            countdown_area.empty()
            st.info("Süre doldu! Lütfen mesajınızı tekrar göndermeyi deneyin.")
        else:
            st.error(f"Teknik bir sorun çıktı: {error}")

# --- 6. YAN PANEL ---
with st.sidebar:
    st.title("Swozzy AI")
    if st.button("Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.caption("© 2026 Swozzy | Kesintisiz Mod")
