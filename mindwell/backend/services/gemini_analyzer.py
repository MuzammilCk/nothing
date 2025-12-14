import json
import vertexai
from vertexai.generative_models import GenerativeModel
from ..config import settings

class GeminiAnalyzer:
    def __init__(self):
        try:
            vertexai.init(project=settings.PROJECT_ID, location=settings.LOCATION)
        except Exception as e:
            print(f"Vertex AI Init Warning: {e}")
            
        self.model = GenerativeModel(settings.GEMINI_MODEL_NAME)
        
        # Load prompt
        with open("d:/projects/devpost/mindwell/prompts/mental_health_system_prompt.txt", "r") as f:
            self.system_prompt_template = f.read()

    async def analyze_text(self, transcript: str) -> dict:
        prompt = self.system_prompt_template.replace("{transcript}", transcript)
        
        try:
            response = self.model.generate_content(prompt)
            # Parse JSON from response
            cleaned_text = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned_text)
        except Exception as e:
            print(f"Gemini Analysis Error: {e}")
            # Fallback safe response
            return {
                "depression_score": 0,
                "anxiety_score": 0,
                "suicide_risk_flag": False,
                "key_symptoms": ["error_analyzing"],
                "recommended_action": "gentle_support"
            }
