import google.generativeai as genai

# ANAHTARINI BURAYA YAPIŞTIR
genai.configure(api_key="BURAYA_API_ANAHTARINI_YAZ")

try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Merhaba, çalışıyor musun?")
    print("Sistem Yanıtı:", response.text)
except Exception as e:
    print("Hata oluştu, mesaj şu:", e)
