FROM node:20 AS frontend-builder

ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

WORKDIR /app/frontend
COPY frontend/ ./
RUN npm install && npm run build

FROM python:3.10-slim

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN mkdir -p /app/backend/model_cache

COPY backend/ ./backend
COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/.env.production ./backend/.env.production

ENV ENV_MODE=production

RUN python3 -c "from faster_whisper import WhisperModel; WhisperModel('Systran/faster-whisper-small', device='cpu', compute_type='int8')"

ENV TRANSFORMERS_CACHE=/app/backend/model_cache
RUN python3 -c 'from transformers import AutoTokenizer, AutoModelForSequenceClassification; \
AutoTokenizer.from_pretrained("WhiterBB/multilingual-hatespeech-detection", cache_dir="/app/backend/model_cache"); \
AutoModelForSequenceClassification.from_pretrained("WhiterBB/multilingual-hatespeech-detection", cache_dir="/app/backend/model_cache")'

COPY --from=frontend-builder /app/frontend/dist ./backend/app/dist

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
