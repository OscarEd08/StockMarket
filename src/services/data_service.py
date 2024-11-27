import json

import pandas as pd
import yfinance as yf
from fastapi import HTTPException


class DataService:
    def get_market_data(self, symbols: list, period: str):
        """Obtiene datos de mercado en tiempo real desde Yahoo Finance usando yfinance y los guarda en un archivo JSON."""
        data = {}
        try:
            for symbol in symbols:
                print(f"Obteniendo datos para: {symbol}")
                ticker = yf.Ticker(symbol)
                print("Obteniendo datos de mercado...")
                history = ticker.history(period=period)
                print("History: ", history)
                if history.empty:
                    raise ValueError(f"No data found for symbol: {symbol}")

                # Convert Timestamp objects to strings
                history.index = history.index.map(lambda x: x.isoformat() if isinstance(x, pd.Timestamp) else x)
                data[symbol] = history.to_dict()

            # Guardar los datos en un archivo JSON
            with open('market_data.json', 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, indent=4, default=str)

            return data

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener datos de Yahoo Finance: {str(e)}")
