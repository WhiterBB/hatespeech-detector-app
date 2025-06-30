# FASE 1: Build del frontend
FROM node:20 AS frontend-builder

WORKDIR /app/frontend
COPY frontend/ ./
RUN npm install
RUN npm run build

# FASE 2: Backend con Python + FFmpeg
FROM python:3.10-slim

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*
WORKDIR /app

COPY backend/ ./backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
