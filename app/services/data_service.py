import yfinance as yf
from fastapi import HTTPException

class DataService:
    def get_market_data(self, symbols: list):
        """Obtiene datos de mercado en tiempo real desde Yahoo Finance usando yfinance."""
        data = {}
        try:
            for symbol in symbols:
                print(f"Obteniendo datos para: {symbol}")
                ticker = yf.Ticker(symbol)
                print("Obteniendo datos de mercado...")
                history = ticker.history(period="1d", interval="15m")
                print("History: ", history)
                if history.empty:
                    raise ValueError(f"No data found for symbol: {symbol}")
                data[symbol] = history.to_dict()
            return data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener datos de Yahoo Finance: {str(e)}")