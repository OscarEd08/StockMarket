from fastapi import APIRouter, HTTPException
from src.services.broker_service import BrokerService

router = APIRouter()
broker_service = BrokerService()

@router.post("/place-order")
def place_order(symbol: str, secType: str, exchange: str, action: str, 
                quantity: int, orderType: str, lmtPrice: float = None):
    """Coloca una orden."""
    try:
        result = broker_service.place_order(symbol, secType, exchange, action, quantity, orderType, lmtPrice)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cancel-order")
def cancel_order(order_id: int):
    """Cancela una orden."""
    try:
        result = broker_service.cancel_order(order_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/order-status/{order_id}")
def get_order_status(order_id: int):
    """Consulta el estado de una orden."""
    try:
        return broker_service.get_order_status(order_id)
    except HTTPException as e:
        raise e

@router.get("/all-orders")
def get_all_orders():
    """Lista todas las órdenes abiertas."""
    return broker_service.get_all_orders()
