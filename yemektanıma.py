from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import io
from PIL import Image

app = FastAPI()

# Model yükleniyor
model = ResNet50(weights='imagenet')

def preprocess_image(file) -> np.ndarray:
    img = Image.open(file).convert("RGB")
    img = img.resize((224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x

@app.post("/tahmin")
async def tahmin_et(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        processed_image = preprocess_image(io.BytesIO(contents))
        preds = model.predict(processed_image)
        results = decode_predictions(preds, top=3)[0]

        tahminler = [
            {"etiket": etiket, "isim": etiket, "olasilik": float(f"{oran*100:.2f}")}
            for (_, etiket, oran) in results
        ]

        return JSONResponse(content={"tahminler": tahminler})
    
    except Exception as e:
        return JSONResponse(content={"hata": str(e)}, status_code=500)

