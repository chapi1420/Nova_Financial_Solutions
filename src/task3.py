import pandas as pd
import yfinance as yf
import numpy as np
import talib
from textblob import TextBlob
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

class FinancialAnalysis:
    def __init__(self, news_data_path):
        """
        Initialize with news data path
        """
        self.news_df = pd.read_csv(news_data_path)
        self.news_df['date'] = pd.to_datetime(self.news_df['date'], format="%Y-%m-%d %H:%M:%S", errors='coerce')
        self.stocks_data = {}
        self.technical_indicators = {}
        
    def get_sentiment_score(self, text):
        """
        Calculate sentiment score using TextBlob
        """
        return TextBlob(str(text)).sentiment.polarity
    
    def analyze_news_sentiment(self):
        """
        Perform sentiment analysis on news headlines
        """
        self.news_df['sentiment_score'] = self.news_df['headline'].apply(self.get_sentiment_score)
        
        # Aggregate sentiments by date and stock
        self.daily_sentiment = self.news_df.groupby(['date', 'stock'])['sentiment_score'].mean().reset_index()
        return self.daily_sentiment
    
    def get_stock_data(self, symbols):
        """
        Fetch stock data using yfinance
        """
        end_date = datetime.now()
        start_date = self.news_df['date'].min()
        
        for symbol in symbols:
            stock_data = yf.download(symbol, start=start_date, end=end_date)
            self.stocks_data[symbol] = stock_data
            
            # Calculate daily returns
            self.stocks_data[symbol]['returns'] = stock_data['Close'].pct_change()
            
            # Calculate technical indicators
            self.technical_indicators[symbol] = self.calculate_technical_indicators(stock_data)
    
    def calculate_technical_indicators(self, stock_data):
        """
        Calculate technical indicators for a stock
        """
        indicators = pd.DataFrame()
        
        # Moving averages
        indicators['MA20'] = talib.SMA(stock_data['Close'], timeperiod=20)
        indicators['MA50'] = talib.SMA(stock_data['Close'], timeperiod=50)
        
        # RSI
        indicators['RSI'] = talib.RSI(stock_data['Close'], timeperiod=14)
        
        # MACD
        macd, signal, hist = talib.MACD(stock_data['Close'])
        indicators['MACD'] = macd
        indicators['MACD_Signal'] = signal
        
        return indicators
    
    def calculate_correlations(self):
        """
        Calculate correlations between sentiment and stock returns
        """
        correlation_results = {}
        
        for symbol in self.stocks_data.keys():
            # Get stock specific sentiment
            stock_sentiment = self.daily_sentiment[self.daily_sentiment['stock'] == symbol]
            
            # Get stock returns
            stock_returns = self.stocks_data[symbol]['returns']
            
            # Align dates
            merged_data = pd.merge(
                stock_sentiment,
                stock_returns.reset_index(),
                left_on='date',
                right_on='Date',
                how='inner'
            )
            
            # Calculate correlation
            correlation, p_value = stats.pearsonr(
                merged_data['sentiment_score'],
                merged_data['returns'].fillna(0)
            )
            
            correlation_results[symbol] = {
                'correlation': correlation,
                'p_value': p_value
            }
            
        return correlation_results
    
    def calculate_technical_correlations(self):
        """
        Calculate correlations between technical indicators across stocks
        """
        # Prepare DataFrames for each indicator
        ma20_data = pd.DataFrame()
        ma50_data = pd.DataFrame()
        rsi_data = pd.DataFrame()
        
        for symbol in self.technical_indicators.keys():
            ma20_data[symbol] = self.technical_indicators[symbol]['MA20']
            ma50_data[symbol] = self.technical_indicators[symbol]['MA50']
            rsi_data[symbol] = self.technical_indicators[symbol]['RSI']
        
        correlations = {
            'MA20': ma20_data.corr(),
            'MA50': ma50_data.corr(),
            'RSI': rsi_data.corr()
        }
        
        return correlations
    
    def plot_correlations(self, correlations, title):
        """
        Create heatmap of correlations
        """
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlations, annot=True, cmap='coolwarm', center=0)
        plt.title(title)
        plt.tight_layout()
        plt.show()
    
    def generate_report(self):
        """
        Generate analysis report
        """
        report = {
            'sentiment_stats': self.news_df['sentiment_score'].describe(),
            'daily_sentiment_avg': self.daily_sentiment.groupby('stock')['sentiment_score'].mean(),
            'correlations': self.calculate_correlations(),
            'technical_correlations': self.calculate_technical_correlations()
        }
        return report

def main():
    # Initialize analysis
    analysis = FinancialAnalysis('C:\\Users\\nadew\\10x\\week1\\Nova_Financial_Solutions\\data_file\\raw_analyst_ratings.csv\\raw_analyst_ratings.csv')
    
    # Analyze news sentiment
    analysis.analyze_news_sentiment()
    
    # Get stock data
    symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META', 'TSLA', 'NVDA']
    analysis.get_stock_data(symbols)
    
    # Calculate correlations
    sentiment_correlations = analysis.calculate_correlations()
    technical_correlations = analysis.calculate_technical_correlations()
    
    # Generate report
    report = analysis.generate_report()
    
    # Plot correlations
    for indicator, corr_matrix in technical_correlations.items():
        analysis.plot_correlations(corr_matrix, f'{indicator} Correlations Across Stocks')
    
    # Print results
    print("\nSentiment-Returns Correlations:")
    for symbol, results in sentiment_correlations.items():
        print(f"\n{symbol}:")
        print(f"Correlation: {results['correlation']:.4f}")
        print(f"P-value: {results['p_value']:.4f}")
    
    # Save results
    pd.DataFrame(sentiment_correlations).to_csv('sentiment_correlations.csv')
    for indicator, corr_matrix in technical_correlations.items():
        corr_matrix.to_csv(f'{indicator}_correlations.csv')

main()