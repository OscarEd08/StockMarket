import openai

class GPTService:
    def __init__(self, api_key):
        openai.api_key = api_key

    def analyze_sentiment(self, text):
        """Analiza el sentimiento de un texto financiero con GPT-4."""
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": text}]
        )
        sentiment = response.choices[0].message['content']
        return sentiment
