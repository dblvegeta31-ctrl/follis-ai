import google.generativeai as genai

# 1. API Anahtarını Yapılandır
# Kendi API anahtarını 'AIza...' kısmına yapıştır
genai.configure(api_key="YOUR_API_KEY")

# 2. Modeli Başlat
# Aldığın 404 hatasını önlemek için doğru isimlendirme:
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Sohbet Oturumunu Başlat (Hafıza için history kullanılır)
chat = model.start_chat(history=[])

print("--- Gemini ile Sohbet Başladı (Çıkmak için 'exit' yazın) ---")

while True:
    user_input = input("Siz: ")
    
    if user_input.lower() in ["exit", "çıkış", "quit"]:
        break

    try:
        # Mesajı gönder ve yanıtı al
        response = chat.send_message(user_input)
        
        print(f"\nGemini: {response.text}\n")
        
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

print("Sohbet sonlandırıldı.")
