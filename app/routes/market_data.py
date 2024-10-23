from fastapi import APIRouter, HTTPException
from app.services.data_service import DataService

router = APIRouter()
data_service = DataService()

@router.get("/realtime")
def get_realtime_data(symbols: list):
    try:
        data = data_service.get_market_data(symbols)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
