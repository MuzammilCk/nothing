from ..config import settings

class RiskEngine:
    def calculate_risk(self, text_analysis: dict, prosody_metrics: dict) -> dict:
        # 1. Normalize Text Risk (0-1)
        # Gemini gives 0-9 scores. 
        # Max theoretical score sum = 9 (dep) + 9 (anx) = 18? Or just take max?
        # Let's average them normalized.
        dep_score = text_analysis.get("depression_score", 0)
        anx_score = text_analysis.get("anxiety_score", 0)
        
        # Normalize to 0-1 (assuming 0-9 scale)
        text_risk_raw = (dep_score + anx_score) / 18.0
        text_risk_raw = min(text_risk_raw, 1.0)
        
        # Suicide flag overrides to MAX risk
        if text_analysis.get("suicide_risk_flag"):
            text_risk_raw = 1.0

        # 2. Get Prosody Risk (0-1)
        prosody_risk_raw = prosody_metrics.get("prosody_risk_score", 0.0)

        # 3. Weighted Combination
        final_risk_score = (text_risk_raw * settings.TEXT_RISK_WEIGHT) + \
                           (prosody_risk_raw * settings.PROSODY_RISK_WEIGHT)

        # 4. Categorize
        if final_risk_score < 0.3:
            category = "Low"
        elif final_risk_score < 0.7:
            category = "Medium"
        else:
            category = "High"

        return {
            "final_score": round(final_risk_score * 10, 1), # 0-10 scale
            "risk_category": category,
            "components": {
                "text_risk": round(text_risk_raw, 2),
                "prosody_risk": round(prosody_risk_raw, 2)
            }
        }
