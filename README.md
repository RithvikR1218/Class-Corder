# 🎥 Classroom Video Recorder with Google Drive Integration

This is a simple Flask-based web app that allows you to record short classroom videos using your webcam, save them locally, and optionally upload them to Google Drive. Videos are listed on the homepage and can be played, downloaded, or deleted.

## 📦 Features

- 🎬 Record 10-second webcam videos using FFmpeg
- 💾 Store videos locally
- ☁️ Upload and sync with Google Drive
- 🎥 View, download, or delete recordings via a clean web interface
- 🔐 OAuth2-based authentication with Google Drive

## 🛠️ Tech Stack

- Python (Flask)
- FFmpeg (for webcam recording)
- Google Drive API (via `google-api-python-client`)
- HTML/CSS/JS frontend

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/classroom-video-recorder.git
cd classroom-video-recorder
```

### 2. Install Dependencies
 ```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Install Ubuntu Dependencies
```bash
chmod +x install.sh
./install.sh
```

### 4. Setup .env
```bash
cp .env.example .env
```

### 5. Start Application
```bash
python3 run.py
```