from fastapi import FastAPI, File, UploadFile, Request, Path
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import RequestValidationError
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
import traceback
import shutil
import os
import uuid
import json
import time

from .whisper_transcribe import transcribe
from .predict import predict_text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_UPLOADS_DIR = os.path.join(BASE_DIR, "..", "temp_uploads")
RESULTS_DIR = os.path.join(BASE_DIR, "..", "results")

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "message": exc.detail},
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"status": "error", "message": "Validation error: please check the input data"},
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"status": "error", "message": "Internal server error. Please try again later."},
    )

# Clean up old JSON files in /results based on expiration time
def cleanup_old_results(results_dir: str, expiration_minutes: int = 30):
    now = time.time()
    expiration_seconds = expiration_minutes * 60

    for filename in os.listdir(results_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(results_dir, filename)
            try:
                file_mtime = os.path.getmtime(file_path)
                file_age = now - file_mtime

                if file_age > expiration_seconds:
                    os.remove(file_path)
                    print(f"Deleted expired result: {filename}")
            except Exception as e:
                print(f"Error deleting {filename}: {str(e)}")

app = FastAPI()

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://h8less.up.railway.app"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze")
async def analyze_video(file: UploadFile = File(...)):
    start_total = time.perf_counter()
    if not file:
        raise HTTPException(status_code=400, detail="No file was uploaded.")

    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Unsupported file format. Please upload a video.")
    
    os.makedirs(RESULTS_DIR, exist_ok=True)
    cleanup_old_results(RESULTS_DIR, expiration_minutes=30)

    try:
        # Create a temporary directory to store the uploaded video
        t0 = time.perf_counter()
        os.makedirs(TEMP_UPLOADS_DIR, exist_ok=True)
        video_id = str(uuid.uuid4())
        temp_video_path = os.path.join(TEMP_UPLOADS_DIR, f"{video_id}_{file.filename}")

        with open(temp_video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        t1 = time.perf_counter()
        print(f"File {file.filename} uploaded successfully in {t1 - t0:.2f} seconds.")
        
        # Step 1: Transcribe the video
        t2 = time.perf_counter()
        segments = transcribe(temp_video_path)
        t3 = time.perf_counter()
        print(f"Transcription completed in {t3 - t2:.2f} seconds.")

        # Step 2: Predict hate speech on each segment
        t4 = time.perf_counter()
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
        t5 = time.perf_counter()
        print(f"Prediction completed in {t5 - t4:.2f} seconds.")

        # Delete the uploaded video after processing
        os.remove(temp_video_path)

        final_output = {
            "status": "success",
            "message": "Video analyzed successfully",
            "video_id": video_id,
            "data": results
        }
        os.makedirs(RESULTS_DIR, exist_ok=True)
        results_file_path = os.path.join(RESULTS_DIR, f"{video_id}.json")
        with open(results_file_path, "w") as results_file:
            json.dump(final_output, results_file, indent=2)
        
        t6 = time.perf_counter()
        print(f"Results saved in {results_file_path} in {t6 - t5:.2f} seconds.")
        print(f"Total processing time: {t6 - start_total:.2f} seconds.")

        # Return the final output as a JSON response    
        return JSONResponse(content=final_output)

    except Exception as e:
        # Raise an HTTP error
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during processing: {str(e)}. Please try again later."
        )

@app.get("/results/{video_id}")
async def get_analysis_result(video_id: str = Path(..., description="The UUID of the analyzed video")):
    try:
        # Construct the path to the saved result JSON file
        results_path = os.path.join(RESULTS_DIR, f"{video_id}.json")

        # Check if the file exists
        if not os.path.exists(results_path):
            raise HTTPException(status_code=404, detail="Analysis result not found.")

        # Load and return the saved JSON data
        with open(results_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return JSONResponse(content=data)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving the results: {str(e)}"
        )
    
# Serve static files from the 'frontend/dist' directory
app.mount("/", StaticFiles(directory="backend/app/dist", html=True), name="static")