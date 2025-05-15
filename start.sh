#!/bin/bash

# Gerekli paketleri kur
pip install -r requirements.txt

# Ana uygulamayı başlat
uvicorn main:app --host 0.0.0.0 --port 8000 --reload