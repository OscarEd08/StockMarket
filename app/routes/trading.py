from fastapi import APIRouter, HTTPException
from app.services.broker_service import BrokerService

router = APIRouter()
broker_service = BrokerService()

@router.post("/execute")
def execute_trade(symbol: str, action: str, quantity: int):
    try:
        result = broker_service.execute_order(symbol, action, quantity)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
