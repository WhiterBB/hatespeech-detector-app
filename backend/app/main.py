from fastapi import FastAPI, File, UploadFile, Request, Path
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import RequestValidationError
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
import traceback
import shutil
import os
import uuid
import json
import time

from .whisper_transcribe import transcribe
from .predict import predict_text

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


@app.post("/analyze")
async def analyze_video(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file was uploaded.")

    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="Unsupported file format. Please upload a video.")
    
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)
    cleanup_old_results(results_dir, expiration_minutes=30)

    try:
        # Create a temporary directory to store the uploaded video
        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        video_id = str(uuid.uuid4())
        temp_video_path = os.path.join(temp_dir, f"{video_id}_{file.filename}")

        with open(temp_video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Step 1: Transcribe the video
        segments = transcribe(temp_video_path)

        # Step 2: Predict hate speech on each segment
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

        # Delete the uploaded video after processing
        os.remove(temp_video_path)

        final_output = {
            "status": "success",
            "message": "Video analyzed successfully",
            "video_id": video_id,
            "data": results
        }
        results_dir = "results"
        os.makedirs(results_dir, exist_ok=True)
        results_file_path = os.path.join(results_dir, f"{video_id}.json")
        with open(results_file_path, "w") as results_file:
            json.dump(final_output, results_file, indent=2)

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
        results_path = os.path.join("results", f"{video_id}.json")

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