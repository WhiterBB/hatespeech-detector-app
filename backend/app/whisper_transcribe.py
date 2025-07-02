from faster_whisper import WhisperModel
import os
import psutil
import time

WHISPER_MODEL = "small"  
DEVICE = "cpu"
PRECISION = "int8"

model = WhisperModel(WHISPER_MODEL, device=DEVICE, compute_type=PRECISION)

def transcribe(video_path: str):
    print(f"Transcribing: {video_path} with model: {WHISPER_MODEL}")

    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / (1024 ** 2)
    t0 = time.perf_counter()

    segments, _ = model.transcribe(video_path)

    result = []
    for i, segment in enumerate(segments):
        result.append({
            "id": i,
            "start": segment.start,
            "end": segment.end,
            "text": segment.text
        })

    t1 = time.perf_counter()
    mem_after = process.memory_info().rss / (1024 ** 2)

    print(f"Transcription completed in {t1 - t0:.2f}s")
    print(f"Memory used by Whisper: {mem_after - mem_before:.2f} MB")

    return result
