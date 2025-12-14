import requests
from ..config import settings

class ElevenLabsTTS:
    def __init__(self):
        self.api_key = settings.ELEVENLABS_API_KEY
        # Use a calm, soothing voice ID
        self.voice_id = "mVew17pFWlMo6436Hze1" # Example: 'Mimi' or similar calm voice
        self.url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"

    def speak(self, text: str) -> bytes:
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }
        response = requests.post(self.url, json=data, headers=headers)
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"ElevenLabs TTS Error: {response.text}")
