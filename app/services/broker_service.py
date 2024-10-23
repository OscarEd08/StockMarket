import requests

class BrokerService:
    BASE_URL = "https://api.interactivebrokers.com/v1"

    def execute_order(self, symbol, action, quantity):
        """Ejecuta una orden en el broker."""
        order = {
            "symbol": symbol,
            "action": action,  # 'buy' o 'sell'
            "quantity": quantity
        }
        response = requests.post(f"{self.BASE_URL}/orders", json=order)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Error al ejecutar la orden.")
