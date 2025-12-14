from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import shutil
import base64
from concurrent.futures import ThreadPoolExecutor

from .services.elevenlabs_stt import ElevenLabsSTTService
from .services.elevenlabs_tts import ElevenLabsTTS
from .services.gemini_analyzer import GeminiAnalyzer
from .services.prosody_analyzer import ProsodyAnalyzer
from .core.risk_engine import RiskEngine
from .core.response_generator import ResponseGenerator
from .utils.audio_utils import AudioUtils

app = FastAPI(title="MindWell API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Services
stt_service = ElevenLabsSTTService()
tts_service = ElevenLabsTTS()
gemini_analyzer = GeminiAnalyzer()
prosody_analyzer = ProsodyAnalyzer()
risk_engine = RiskEngine()
response_generator = ResponseGenerator()

@app.post("/api/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    temp_filename = f"temp_{file.filename}"
    try:
        # 1. Save File for Librosa
        AudioUtils.save_upload_file(file, temp_filename)
        
        # 2. Parallel Processing? 
        # STT and Prosody can be parallel, but Logic needs both.
        # For simplicity, sequential or async await.
        
        # Read file bytes for STT
        with open(temp_filename, "rb") as f:
            audio_bytes = f.read()

        # Step A: STT
        transcript = await stt_service.transcribe(audio_bytes)
        print(f"Transcript: {transcript}")

        # Step B: Gemini Analysis
        text_analysis = await gemini_analyzer.analyze_text(transcript)
        print(f"Text Analysis: {text_analysis}")

        # Step C: Prosody Analysis (CPU bound, maybe run in executor if needed, but here simple)
        prosody_metrics = prosody_analyzer.analyze(temp_filename)
        print(f"Prosody: {prosody_metrics}")

        # Step D: Risk Calculation
        risk_result = risk_engine.calculate_risk(text_analysis, prosody_metrics)

        # Step E: Generate Empathic Response Text
        ai_response_text = await response_generator.generate_response(risk_result, text_analysis)
        
        # Step F: TTS
        try:
            audio_response_bytes = tts_service.speak(ai_response_text)
            audio_base64 = base64.b64encode(audio_response_bytes).decode('utf-8')
        except Exception as e:
            print(f"TTS Error: {e}")
            audio_base64 = None

        return {
            "transcript": transcript,
            "risk_data": risk_result,
            "ai_response_text": ai_response_text,
            "audio_response_base64": audio_base64, # Frontend will play this
            "analysis_details": {
                "text": text_analysis,
                "prosody": prosody_metrics
            }
        }

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
