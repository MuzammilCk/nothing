import os
import sys
import requests
from backend.config import Settings

# Ensure we can import backend
sys.path.append(os.getcwd())
from backend.config import settings

def check_elevenlabs():
    print(f"🔍 Checking ElevenLabs API Key ({settings.ELEVENLABS_API_KEY[:4]}...)...")
    url = "https://api.elevenlabs.io/v1/user"
    headers = {"xi-api-key": settings.ELEVENLABS_API_KEY}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # safely get subscription info
            sub = data.get('subscription', {})
            char_count = sub.get('character_count', 0)
            char_limit = sub.get('character_limit', 0)
            print(f"✅ ElevenLabs Success! User: {sub.get('tier', 'Unknown')}")
            print(f"   Usage: {char_count}/{char_limit} characters used.")
            return True
        else:
            print(f"❌ ElevenLabs Failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ ElevenLabs Connection Error: {e}")
        return False

if __name__ == "__main__":
    el_ok = check_elevenlabs()
    
    if el_ok:
        print("\n🎉 API Key is WORKING.")
    else:
        print("\n⚠️ API Key Issues Found.")
