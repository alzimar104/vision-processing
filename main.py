from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv

# Modülleri içe aktar
from calorie_backend.barcode_service import router as barcode_router
from calorie_backend.food_recognition_proxy import router as recognition_router
from calorie_backend.chatbot_service import router as chatbot_router

# .env dosyasını yükle
load_dotenv()

app = FastAPI(title="Calorie Tracker Backend API")

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tüm kaynaklara izin ver (geliştirme için)
    allow_credentials=True,
    allow_methods=["*"],  # Tüm HTTP metodlarına izin ver
    allow_headers=["*"],  # Tüm başlıklara izin ver
    expose_headers=["*"],  # Tüm başlıkları istemciye göster
    max_age=1800,  # Preflight isteklerini önbelleğe al (30 dakika)
)

# Ana sayfa
@app.get("/")
def read_root():
    return {"message": "Calorie Tracker API is running"}

# Router'ları ekle
app.include_router(barcode_router)
app.include_router(recognition_router)
app.include_router(chatbot_router)

# Doğrudan çalıştırma için
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)