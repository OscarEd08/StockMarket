import requests

class DataService:
    YAHOO_FINANCE_API_URL = "https://query1.finance.yahoo.com/v7/finance/quote"

    def get_market_data(self, symbols: list):
        """Obtiene datos de mercado en tiempo real desde Yahoo Finance."""
        query = ','.join(symbols)
        url = f"{self.YAHOO_FINANCE_API_URL}?symbols={query}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Error al obtener datos de Yahoo Finance.")
