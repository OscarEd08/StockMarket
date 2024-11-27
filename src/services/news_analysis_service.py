import string
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import requests
from yahoo_fin import news
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
import json

class CompanyNewsSentimentalAnalysis:
    def __init__(self, country):
        self.country = country
        self.company_news_dict = {}
        print('🚀 Process Initiated!')

    def get_companies_data(self):
        print(f'🔍 Fetching {self.country} companies data...')
        headers = {
            'authority': 'api.nasdaq.com',
            'accept': 'application/json, text/plain, */*',
            'user-agent': 'Mozilla/5.0',
            'origin': 'https://www.nasdaq.com',
        }
        params = {
            'tableonly': 'true',
            'limit': '25',
            'offset': '0',
            'download': 'true',
            'country': self.country
        }
        response = requests.get('https://api.nasdaq.com/api/screener/stocks/', headers=headers, params=params)
        json_data = response.json()['data']
        data = pd.DataFrame(json_data['rows'], columns=json_data['headers'])
        print(f'✅ {self.country} companies data downloaded successfully!')
        return data

    def get_company_news(self, company_ticker_symbol):
        print(f'🔍 Fetching news for {company_ticker_symbol}...')
        company_news_list = news.get_yf_rss(company_ticker_symbol)
        print(f'📰 {company_ticker_symbol} news gathered successfully!')
        return pd.DataFrame({
            'titles': [article.get('title') for article in company_news_list],
            'summaries': [article.get('summary') for article in company_news_list]
        })

    def preprocess_setup(self):
        print('🛠 Text Preprocessing Setup initiated...')
        nltk.download('stopwords')
        nltk.download('punkt')
        self.stop_words = set(stopwords.words('english'))
        print('✅ Text Preprocessing Setup completed successfully!')

    def preprocess_text(self, text):
        no_punctuation = text.translate(str.maketrans('', '', string.punctuation))
        tokens = nltk.word_tokenize(no_punctuation)
        return [word for word in tokens if word.lower() not in self.stop_words]

    def analyze_sentiment(self, text):
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        sentiment = 'Positive' if polarity > 0 else 'Negative' if polarity < 0 else 'Neutral'
        return polarity, sentiment

    def gather_companies_info(self):
        print(f'🔎 Gathering {self.country} company information...')
        self.companies_df = self.get_companies_data()
        self.companies_df['title average polarity'] = None
        self.companies_df['summary average polarity'] = None
        self.companies_df['overall average polarity'] = None

    def gather_company_info(self, company_name, company_ticker_symbol):
        print(f'📰 Fetching news for {company_name}...')
        self.company_news_dict[company_name] = self.get_company_news(company_ticker_symbol)
        self.company_news_dict[company_name]['name'] = company_name

    def run_sentimental_analysis(self, company_name):
        self.company_news_dict[company_name]['title polarity'], self.company_news_dict[company_name]['title sentiment'] = \
            zip(*self.company_news_dict[company_name]['titles'].apply(self.analyze_sentiment))
        self.company_news_dict[company_name]['summary polarity'], self.company_news_dict[company_name]['summary sentiment'] = \
            zip(*self.company_news_dict[company_name]['summaries'].apply(self.analyze_sentiment))

    def calculate_average_polarity(self, company_name):
        title_average_polarity = self.company_news_dict[company_name]['title polarity'].mean()
        summary_average_polarity = self.company_news_dict[company_name]['summary polarity'].mean()
        filt = self.companies_df['name'] == company_name
        self.companies_df.loc[filt, 'title average polarity'] = title_average_polarity
        self.companies_df.loc[filt, 'summary average polarity'] = summary_average_polarity
        self.companies_df.loc[filt, 'overall average polarity'] = (title_average_polarity + summary_average_polarity) / 2

    def combine_company_news(self):
        self.company_news_df = pd.concat(list(self.company_news_dict.values()))

    def get_sentiment_analysis_json(self):
        # data_dict = self.company_news_df.to_dict(orient='records')
        # return json.dumps(data_dict, ensure_ascii=False)
        return json.loads(self.company_news_df.to_json(orient='records'))

    def run(self):
        self.gather_companies_info()
        self.company_news_dict = dict()
        self.company_dict = dict(zip(self.companies_df['name'], self.companies_df['symbol']))
        self.preprocess_setup()
        for company_name, company_ticker_symbol in self.company_dict.items():
            self.gather_company_info(company_name, company_ticker_symbol)
            self.run_sentimental_analysis(company_name)
            self.calculate_average_polarity(company_name)
        self.combine_company_news()
        return self.get_sentiment_analysis_json()