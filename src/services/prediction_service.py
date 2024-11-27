import json
import numpy as np
from sklearn.linear_model import LinearRegression

class PredictionService:
    def __init__(self, json_file='market_data.json'):
        self.data : dict | None = None
        self.load_data(json_file)

    def predict_prices(self, symbol, days):
        if symbol not in self.data:
            raise ValueError(f"No data found for symbol: {symbol}")

        history = self.data[symbol]
        dates = list(history['Close'].keys())
        prices = list(history['Close'].values())

        # Convert dates to ordinal numbers for regression
        X = np.array([np.datetime64(date).astype(int) for date in dates]).reshape(-1, 1)
        y = np.array(prices)

        # Train the model
        model = LinearRegression()
        model.fit(X, y)

        # Predict future prices
        last_date = np.datetime64(dates[-1])
        future_dates = [last_date + np.timedelta64(i, 'D') for i in range(1, days + 1)]
        future_X = np.array([date.astype(int) for date in future_dates]).reshape(-1, 1)
        predictions = model.predict(future_X)

        return {str(date): price for date, price in zip(future_dates, predictions)}

    def load_data(self, json_file='market_data.json'):
        with open(json_file, 'r', encoding='utf-8') as file:
            self.data = json.load(file)