from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import httpx
import base64
from typing import Optional
from io import BytesIO

router = APIRouter(tags=["Food Recognition"])

# Render API URL for food recognition
RENDER_API_URL = "https://vision-processing.onrender.com/tahmin"

@router.post("/recognize_file")
async def recognize_food_file(file: UploadFile = File(...)):
    """
    Görüntüden yemek tanıma için Render API'ye proxy isteği yapar.
    """
    try:
        # Dosya içeriğini oku
        contents = await file.read()
        
        # Render API'ye istek gönder
        async with httpx.AsyncClient(timeout=60.0) as client:
            files = {"file": (file.filename, contents, file.content_type)}
            response = await client.post(RENDER_API_URL, files=files)
            
            # Yanıtı kontrol et
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "error": f"Render API hatası: {response.status_code}",
                    "detail": response.text
                }
    except Exception as e:
        return {
            "error": "Proxy hatası",
            "detail": str(e)
        }

@router.post("/recognize_base64")
async def recognize_food_base64(data: dict):
    """
    Base64 kodlanmış görüntüden yemek tanıma için Render API'ye proxy isteği yapar.
    Web uygulamaları için idealdir.
    """
    try:
        # Base64 kodlu veriyi al
        base64_image = data.get("image")
        if not base64_image:
            return {"error": "Base64 kodlu görüntü bulunamadı"}
        
        # Base64'ü ikili veriye dönüştür
        image_data = base64.b64decode(base64_image.split(",")[1] if "," in base64_image else base64_image)
        
        # Render API'ye istek gönder
        async with httpx.AsyncClient(timeout=60.0) as client:
            files = {"file": ("image.jpg", image_data, "image/jpeg")}
            response = await client.post(RENDER_API_URL, files=files)
            
            # Yanıtı kontrol et
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "error": f"Render API hatası: {response.status_code}",
                    "detail": response.text
                }
    except Exception as e:
        return {
            "error": "Proxy hatası",
            "detail": str(e)
        }