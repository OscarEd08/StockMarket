from fastapi import APIRouter, HTTPException
from src.services.gpt_service import GPTService

router = APIRouter()
gpt_service = GPTService(api_key="tu_api_key_de_openai")

@router.post("/analyze")
def analyze_text(text: str):
    try:
        sentiment = gpt_service.analyze_sentiment(text)
        return {"sentiment": sentiment}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
