import whisper
from typing import List, Dict

print("🔊 Loading model Whisper...")
model = whisper.load_model("medium") 

def transcribe(video_path: str) -> List[Dict]:
    """
    Transcribe the given video file and return a list of segments.
    
    Each segment is a dictionary with keys like: id, start, end, text.
    """
    print(f"📼 Transcribing: {video_path}")
    result = model.transcribe(video_path)
    return result["segments"]
