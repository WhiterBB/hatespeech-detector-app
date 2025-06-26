from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import shutil
import os
import uuid

from .whisper_transcribe import transcribe
from .predict import predict_text

app = FastAPI()

@app.post("/analyze-video")
async def analyze_video(file: UploadFile = File(...)):
    try:
        # Create temporary directory for uploads
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        video_id = str(uuid.uuid4())
        temp_video_path = os.path.join(temp_dir, f"{video_id}_{file.filename}")

        # Save the uploaded file to a temporary location
        with open(temp_video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Step 1: Video transcription
        segments = transcribe(temp_video_path)

        # Step 2: Text classification
        results = []
        for segment in segments:
            text = segment["text"]
            pred_label, prob = predict_text(text)
            results.append({
                "id": segment["id"],
                "start": segment["start"],
                "end": segment["end"],
                "text": text.strip(),
                "class_predicted": pred_label,
                "probability": round(prob, 4)
            })

        # Clean up the temporary video file
        os.remove(temp_video_path)

        return JSONResponse(content=results)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
