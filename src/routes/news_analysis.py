from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.gpt_service import GPTService
from src.services.news_analysis_service import CompanyNewsSentimentalAnalysis

router = APIRouter()

class AnalysisRequest(BaseModel):
    country: str

@router.post("/analyze")
def analyze_text(request: AnalysisRequest):
    try:
        analysis = CompanyNewsSentimentalAnalysis(request.country)
        result = analysis.run()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
