import os
import google.generativeai as genai

# 1. API Anahtarını Sır (Secret) kısmından çekiyoruz
# Bu yöntem anahtarının kodda görünmesini engeller
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("Hata: GEMINI_API_KEY bulunamadı! Lütfen Secrets kısmına ekleyin.")
else:
    # 2. Yapılandırma
    genai.configure(api_key=api_key)

    # 3. Model Ayarları (Hata almamak için güncel isim)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 4. Sohbeti başlat
    chat = model.start_chat(history=[])

    print("--- Sistem Aktif: Gemini ile Konuşabilirsiniz ---")
    
    try:
        while True:
            user_msg = input("Siz: ")
            if user_msg.lower() in ["exit", "kapat", "quit"]:
                break
            
            # Yanıt oluşturma
            response = chat.send_message(user_msg)
            print(f"\nGemini: {response.text}\n")
            
    except Exception as e:
        print(f"Bir sorun oluştu: {e}")
