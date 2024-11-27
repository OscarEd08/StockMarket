class TradingDecisionService:
    def __init__(self, prediction_service):
        self.prediction_service = prediction_service

    def make_decision(self, symbol: str, days: int, threshold: float = 5.0):
        """
        Make a decision based on stock price predictions.

        :param symbol: Stock symbol to predict.
        :param days: Number of days to predict.
        :param threshold: Percentage threshold for decision-making.
        :return: Decision and prediction details.
        """
        # Get predictions from the prediction service
        predictions = self.prediction_service.predict_prices(symbol, days)

        # Convert predictions to a list of prices
        predicted_prices = list(predictions["prediction"].values())
        
        if len(predicted_prices) < 2:
            raise ValueError("Not enough data for decision-making.")

        # Calculate the percentage change between the last predicted price and the first
        initial_price = predicted_prices[0]
        final_price = predicted_prices[-1]
        percentage_change = ((final_price - initial_price) / initial_price) * 100

        # Make a decision
        if percentage_change > threshold:
            decision = "Buy"
        elif percentage_change < -threshold:
            decision = "Sell"
        else:
            decision = "Hold"

        # Return the decision and relevant data
        return {
            "symbol": symbol,
            "days": days,
            "threshold": threshold,
            "decision": decision,
            "percentage_change": percentage_change,
            "predictions": predictions
        }
