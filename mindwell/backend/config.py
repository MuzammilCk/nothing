import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # REPLACE WITH YOUR ACTUAL PROJECT ID
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "mindwell-hackathon")
    LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "sk_520ca88016f7fc3c3f6caa5aec27049ae0d730a0adc2cbca")
    GEMINI_MODEL_NAME = "gemini-1.5-flash-001" # Or latest avail
    
    # Risk Calculation Weights
    TEXT_RISK_WEIGHT = 0.65
    PROSODY_RISK_WEIGHT = 0.35

settings = Config()
