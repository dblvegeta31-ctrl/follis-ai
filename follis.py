import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- 1. GÜVENLİ API YAPILANDIRMASI ---
if "GOOGLE_API_KEY" in st.secrets:
    # API Anahtarını yapılandır
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Lütfen Streamlit Secrets kısmına GOOGLE_API_KEY ekleyin!")
    st.stop()

# --- 2. TARİH AYARI ---
simdi = datetime.now()
gun_ay_yil = simdi.strftime("%d %m %Y")

# --- 3. MODEL TANIMLAMA (EN GARANTİ İSİM) ---
# 'gemini-1.5-flash' yerine 'gemini-1.5-flash-latest' kullanarak 404 hatasını bypass ediyoruz.
try:
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash-latest',
        system_instruction=f"Senin adın Swozzy AI. Versiyonun 2.5-Flash. Bugünün tarihi {gun_ay_yil} ve biz 2026 yılındayız. Çok zeki ve hızlı bir asistansın."
    )
except Exception as e:
    st.error(f"Model başlatılamadı: {e}")

# --- 4. SAYFA AYARLARI ---
st.set
