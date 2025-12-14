from vertexai.generative_models import GenerativeModel
from ..config import settings

class ResponseGenerator:
    def __init__(self):
        # Ensure initialized (idempotent)
        try:
            vertexai.init(project=settings.PROJECT_ID, location=settings.LOCATION)
        except:
            pass
            
        self.model = GenerativeModel(settings.GEMINI_MODEL_NAME)
        with open("d:/projects/devpost/mindwell/prompts/empathy_response_prompt.txt", "r") as f:
            self.prompt_template = f.read()

    async def generate_response(self, risk_data: dict, text_analysis: dict) -> str:
        symptoms = ", ".join(text_analysis.get("key_symptoms", []))
        risk_category = risk_data["risk_category"]
        
        prompt = self.prompt_template.format(
            risk_category=risk_category,
            symptoms=symptoms
        )
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception:
            return "I hear you, and I want you to know you are not alone. Please take a moment to breathe."
