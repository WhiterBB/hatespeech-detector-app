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
* ![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=node-dot-js&logoColor=white)
* ![Whisper](https://img.shields.io/badge/Whisper-555?style=for-the-badge)
* ![XLM-RoBERTa](https://img.shields.io/badge/XLM--RoBERTa-ffcc00?style=for-the-badge&logo=huggingface&logoColor=black)

---

### 📦 Features

- 🎥 Upload and analyze video content locally or via browser
- 🧠 Real-time Whisper-based transcription
- 🔍 Hate speech detection in Spanish, English, and French
- 📊 Probability-based classification (non-hate, light, moderate, severe)
- 🕒 Timestamp tagging of hateful segments for timeline rendering
- 📦 Dockerized for local development and easy deployment

---
