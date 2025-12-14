# MindWell 🧠
**Voice-First AI Mental Health Screening Assistant**
*Built for the ElevenLabs x Google Cloud Hackathon*

MindWell is an AI-powered screening tool that estimates depression and anxiety risk by analyzing **what** you say (text) and **how** you say it (prosody).

## 🚀 Features
- **Voice-Native**: Speak naturally; no typing required.
- **Multi-Modal Analysis**: Combines Gemini Pro text analysis with Librosa audio feature extraction (pitch, tempo, pauses).
- **Empathetic AI**: Uses ElevenLabs TTS to provide soothing, non-robotic responses.
- **Privacy First**: No permanent audio storage. Immediate helpline escalation for high-risk users.

## 🛠️ Tech Stack
- **Frontend**: HTML5, CSS3 (Glassmorphism), Vanilla JS
- **Backend**: FastAPI (Python)
- **AI/ML**: 
  - **ElevenLabs**: Speech-to-Text & Text-to-Speech
  - **Vertex AI (Gemini Pro)**: Clinical sentiment analysis
  - **Librosa**: Audio signal processing
- **Deployment**: Google Cloud Run + Docker

## 📂 Structure
```
mindwell/
├── backend/        # FastAPI App
├── frontend/       # Web Interface
├── deploy/         # Docker & Cloud Run Config
└── prompts/        # System Prompts for Gemini
```

## 🔧 Setup & Run
1. **Prerequisites**: Python 3.9+, Google Cloud SDK, ElevenLabs API Key.
2. **Install Dependencies**:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. **Configure Environment**:
   Update `backend/config.py` with your `ELEVENLABS_API_KEY` and Google Cloud Project ID.
4. **Run Backend**:
   ```bash
   uvicorn backend.main:app --reload
   ```
5. **Run Frontend**:
   Open `frontend/index.html` in your browser.

## ⚠️ Disclaimer
MindWell is **NOT** a diagnostic tool. It provides screening estimates only.
**Helplines (India):**
- Tele-MANAS: 14416
- iCALL: 022-2552-1111
