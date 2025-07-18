<!-- Header -->

<div align="center">

  <img src="https://cdn-icons-png.flaticon.com/256/3587/3587105.png" alt="logo" width="180" height="auto" />
  <h1>Multilingual Hate Speech Detector – Web App</h1>
  
  <p>
    Full-stack web application for detecting hate speech in multilingual videos. Built with FastAPI, React, and Docker.
  </p>

<!-- Badges -->
<p>
  <a href="https://github.com/WhiterBB/hatespeech-detector-app/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/WhiterBB/hatespeech-detector-app" alt="contributors" />
  </a>
  <a href="https://github.com/WhiterBB/hatespeech-detector-app/commits/main">
    <img src="https://img.shields.io/github/last-commit/WhiterBB/hatespeech-detector-app" alt="last update" />
  </a>
  <a href="https://github.com/WhiterBB/hatespeech-detector-app/network/members">
    <img src="https://img.shields.io/github/forks/WhiterBB/hatespeech-detector-app" alt="forks" />
  </a>
  <a href="https://github.com/WhiterBB/hatespeech-detector-app/stargazers">
    <img src="https://img.shields.io/github/stars/WhiterBB/hatespeech-detector-app" alt="stars" />
  </a>
  <a href="https://github.com/WhiterBB/hatespeech-detector-app/issues/">
    <img src="https://img.shields.io/github/issues/WhiterBB/hatespeech-detector-app" alt="open issues" />
  </a>
</p>

</div>

<br />

## 🧠 About the Project

**Multilingual Hate Speech Detector Web App** is the front-facing platform that allows users to upload videos, transcribe them using Whisper, and analyze the text for hate speech using a fine-tuned XLM-RoBERTa model. This project connects the core ML engine with a visual interface for interaction, review, and visualization.

> The full ML engine and training pipeline is available in the [core repository](https://github.com/WhiterBB/multilingual-hate-speech).

---

### 🚀 Tech Stack

* ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)
* ![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
* ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
* ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
* ![Whisper](https://img.shields.io/badge/Whisper-555?style=for-the-badge)
* ![XLM-RoBERTa](https://img.shields.io/badge/XLM--RoBERTa-ffcc00?style=for-the-badge&logo=huggingface&logoColor=black)
* ![Hugging Face](https://img.shields.io/badge/Hugging--Face-FFBF00?style=for-the-badge&logo=huggingface&logoColor=black)

---

### 📦 Features

- 🎥 Upload and analyze video content locally or via browser
- 🧠 Real-time Whisper-based transcription
- 🔍 Hate speech detection in Spanish, English, and French
- 📊 Probability-based classification (non-hate, light, moderate, severe)
- 🕒 Timestamp tagging of hateful segments for timeline rendering
- 📦 Dockerized for local development and easy deployment

---

## 🚀 Getting Started (Docker)

### 🔧 Requirements

- Docker Engine (v20+)
- Git

### 📁 Clone & Run

```bash
# Clone the repository
git clone https://github.com/WhiterBB/hatespeech-detector-app.git
cd hatespeech-detector-app

# Build the image
docker build -t h8less-final .

# Run the container
docker run -p 8000:8000 h8less-final
```

Visit [http://localhost:8000](http://localhost:8000) in your browser.

---

## 🔐 Environment Variables

The system is configured with separate `.env` files for production and development.

### Backend

| File               | Purpose                      |
| ------------------ | ---------------------------- |
| `.env.production`  | Used automatically in Docker |
| `.env.development` | Optional for local dev       |

Example:

```env
ENV_MODE=production
```

### Frontend

| File               | Purpose                       |
| ------------------ | ----------------------------- |
| `.env.production`  | Sets VITE\_API\_URL for prod  |
| `.env.development` | Sets VITE\_API\_URL for local |

Example:

```env
VITE_API_URL=http://localhost:8000
```

---

## 🧬 Model Details

This project uses a fine-tuned [`XLM-RoBERTa-base`](https://huggingface.co/WhiterBB/multilingual-hatespeech-detection) model trained to detect hate speech in Spanish, English, and French. It was trained on a combination of curated hate speech datasets and bias-balanced samples to provide robust multilingual predictions.

**Model repository:**\
🔗 [https://huggingface.co/WhiterBB/multilingual-hatespeech-detection](https://huggingface.co/WhiterBB/multilingual-hatespeech-detection)

**Classes:**

- `non-hate`
- `hate`

**Training highlights:**

- Fine-tuned from `xlm-roberta-base`
- Balanced \~60k samples across three languages
- Evaluated on hate speech severity and class confidence

---

## 🏗️ Project Structure

```
hatespeech-detector-app/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI entrypoint
│   │   ├── predict.py               # XLM-R prediction logic
│   │   ├── whisper_transcribe.py    # Whisper transcription handler
│   ├── results/                     # Stores JSON analysis outputs
│   ├── temp_uploads/                # Temporary video storage
│   ├── model_cache/                 # Hugging Face cache directory
│   └── tests/                       # Pytest test cases
├── frontend/
│   ├── src/
│   ├── .env.production              # VITE_API_URL for production
│   ├── .env.development             # VITE_API_URL for local
├── Dockerfile
├── LICENSE
├── README.md
```

---

## 🧪 Testing

The backend includes `pytest` test cases for local development.
To run them manually:

```bash
cd backend
pytest tests -v
```

Tests include:

- ✅ Video upload and analysis
- ✅ Retrieval of JSON results

---

## 🚰 Cleaning Up

To remove the image and container:

```bash
# Stop container
docker ps
# docker stop <container_id>

# Remove container and image
docker rm <container_id>
docker rmi h8less-final
```

## 📄 License

MIT License – feel free to use for academic and non-commercial projects.

## ✍️ Author

Made with ❤️ by [WhiterBB](https://github.com/WhiterBB) as part of a final master's thesis (TFM) in Artificial Intelligence.
