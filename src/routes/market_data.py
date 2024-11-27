from fastapi import APIRouter, HTTPException, Query
from src.services.data_service import DataService
from src.services.prediction_service import PredictionService
from src.services.trading_decision_service import TradingDecisionService
from typing import Literal

router = APIRouter()
data_service = DataService()
prediction_service = PredictionService()
trading_decision_service = TradingDecisionService(prediction_service)

@router.get("/realtime")
def get_realtime_data(symbols: list = Query(...), period: Literal['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'] = Query(...)):
    try:
        data = data_service.get_market_data(symbols, period)
        prediction_service.load_data()
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

@router.get("/decision")
def make_decision(symbol: str, days: int, threshold: float = 5.0):
    try:
        # Delegate the logic to the service
        decision = trading_decision_service.make_decision(symbol, days, threshold)
        return decision
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))