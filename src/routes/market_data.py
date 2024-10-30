from fastapi import APIRouter, HTTPException, Query
from src.services.data_service import DataService
from src.services.prediction_service import PredictionService

router = APIRouter()
data_service = DataService()
prediction_service = PredictionService()

@router.get("/realtime")
def get_realtime_data(symbols: list = Query(...), days: int = Query(...)):
    try:
        data = data_service.get_market_data(symbols, days)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/predict")
def predict_prices(symbol: str, days: int):
    try:
        predictions = prediction_service.predict_prices(symbol, days)
        return predictions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))