from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import google.generativeai as genai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Geliştirme için izin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(api_key="AIzaSyC2QuojBfhcjIsooviAeVVkmhugfdZrlQc")

@app.post("/ara")
async def analiz(
    prompt: str = Form(""),  # Kullanıcı yazmasa da boş string
    image: List[UploadFile] = File(None)  # Çoklu resim desteği
):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")

        # AI promptu, hep şef modu açık olacak şekilde
        user_prompt = f"""
Aşağıdaki görselleri incele ve Türkçe olarak bir yemek tarifi oluştur.
- Sen bir Michelin yıldızlı şefsın
- Tarif sadece yemekle alakalı olmalı.
- Eğer görseller yemekle alakalı değilse "Üzgünüm, bu görsellere uygun bir yemek tarifi oluşturamıyorum." şeklinde cevap ver.
- Tüm resimlerdeki malzemeleri birleştirerek tek bir tarif oluştur.
- Tarif adım adım yazılsın, malzeme listesi ve hazırlanış adımları numaralandırılsın.
- Tarif 150 kelimeyi geçmesin.
- Kullanıcının eklediği ek açıklama: {prompt}
"""

        content_list = [user_prompt]

        # Resimler varsa ekle
        if image:
            for img in image:
                img_bytes = await img.read()
                content_list.append({"mime_type": img.content_type, "data": img_bytes})

        response = model.generate_content(content_list)

        return JSONResponse({"result": response.text})

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/")
async def root():
    return {"message": "Gemini AI FastAPI aktif! POST /ara kullan."}
