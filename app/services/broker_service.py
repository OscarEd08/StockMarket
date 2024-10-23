import threading
import time
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
from fastapi import HTTPException

class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.nextorderId = None
        self.open_orders = {}  # Almacenar información de órdenes abiertas

    def nextValidId(self, orderId: int):
        """Obtiene el próximo ID válido para órdenes."""
        super().nextValidId(orderId)
        self.nextorderId = orderId
        print('The next valid order id is: ', self.nextorderId)

    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, 
                    permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        """Actualiza el estado de una orden."""
        self.open_orders[orderId] = {
            "status": status,
            "filled": filled,
            "remaining": remaining,
            "lastFillPrice": lastFillPrice,
        }
        print(f"OrderStatus - ID: {orderId}, Status: {status}, Filled: {filled}, Remaining: {remaining}")

    def openOrder(self, orderId, contract, order, orderState):
        """Almacena la información de una orden abierta."""
        self.open_orders[orderId] = {
            "symbol": contract.symbol,
            "action": order.action,
            "quantity": order.totalQuantity,
            "status": orderState.status
        }
        print(f"OpenOrder ID: {orderId}, {contract.symbol} @ {contract.exchange}: {order.action} {order.totalQuantity}, {orderState.status}")

    def execDetails(self, reqId, contract, execution):
        """Registra detalles de ejecución de una orden."""
        print(f"Order Executed: {execution.execId}, {contract.symbol}, {execution.shares}")

class BrokerService:
    def __init__(self, host='127.0.0.1', port=4002, client_id=0):
        """Inicializa la conexión con Interactive Brokers."""
        self.app = IBapi()
        self.app.connect(host, port, client_id)
        self.api_thread = threading.Thread(target=self.run_loop, daemon=True)
        self.api_thread.start()

        # Espera a que la conexión esté lista
        while self.app.nextorderId is None:
            print("Waiting for connection...")
            time.sleep(1)
        print("Connected to IB API.")

    def run_loop(self):
        """Ejecuta el bucle de la API."""
        self.app.run()

    def get_order_status(self, order_id: int):
        """Obtiene el estado de una orden específica."""
        if order_id in self.app.open_orders:
            return self.app.open_orders[order_id]
        else:
            raise HTTPException(status_code=404, detail="Orden no encontrada")

    def get_all_orders(self):
        """Obtiene todas las órdenes abiertas."""
        return self.app.open_orders

    def define_contract(self, symbol: str, secType: str, exchange: str, currency: str = 'USD'):
        """Define un contrato financiero."""
        contract = Contract()
        contract.symbol = symbol
        contract.secType = secType
        contract.exchange = exchange
        contract.currency = currency
        return contract

    def create_order(self, action: str, totalQuantity: int, orderType: str, lmtPrice: float = None):
        """Crea una orden."""
        order = Order()
        order.action = action
        order.totalQuantity = totalQuantity
        order.orderType = orderType
        
        if orderType == 'LMT' and lmtPrice is not None:
            order.lmtPrice = lmtPrice
        
        order.eTradeOnly = False  # Evita errores en FOREX
        order.firmQuoteOnly = False

        return order

    def place_order(self, symbol: str, secType: str, exchange: str, action: str, 
                    quantity: int, orderType: str, lmtPrice: float = None):
        """Coloca una orden en Interactive Brokers."""
        try:
            contract = self.define_contract(symbol, secType, exchange)
            order = self.create_order(action, quantity, orderType, lmtPrice)
            self.app.placeOrder(self.app.nextorderId, contract, order)
            time.sleep(2)
            return {"status": "Orden enviada", "orderId": self.app.nextorderId}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error placing order: {str(e)}")

    def cancel_order(self, order_id: int):
        """Cancela una orden."""
        try:
            self.app.cancelOrder(order_id)
            time.sleep(2)
            return {"status": "Orden cancelada", "orderId": order_id}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error canceling order: {str(e)}")

    def disconnect(self):
        """Desconecta del broker."""
        self.app.disconnect()
