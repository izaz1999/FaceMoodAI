from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from deepface import DeepFace
import shutil, os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/analyze-emotion/")
async def analyze_emotion(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        result = DeepFace.analyze(img_path=file_path, actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']
    except Exception as e:
        return {"error": str(e)}

    os.remove(file_path)
    return {"emotion": emotion}