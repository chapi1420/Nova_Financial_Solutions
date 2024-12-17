import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Task 1: Minimum Essential To Do
# 1. Setting up a folder structure
os.makedirs("notebooks", exist_ok=True)
os.makedirs("tests", exist_ok=True)
os.makedirs("scripts", exist_ok=True)

# 2. EDA: Load the news data and perform basic descriptive statistics
# Replace 'news_data.csv' with the actual file path
news_df = pd.read_csv('C:\\Users\\nadew\\10x\\week1\\Nova_Financial_Solutions\\data_file\\raw_analyst_ratings.csv\\raw_analyst_ratings.csv')  # Columns: ['headline', 'date', 'stock', 'publisher']

# Summary statistics for headline lengths
news_df['headline_length'] = news_df['headline'].apply(len)
print("Basic Descriptive Statistics for Headline Lengths:")
print(news_df['headline_length'].describe())

# Count number of articles per publisher
publisher_counts = news_df['publisher'].value_counts()
print("Top 5 Publishers by Number of Articles:")
print(publisher_counts.head())

# Analyze publication dates
news_df['date'] = pd.to_datetime(news_df['date'], format="%Y-%m-%d %H:%M:%S", errors='coerce')
daily_articles = news_df['date'].dt.date.value_counts().sort_index()

# Plot: Articles over time
plt.figure(figsize=(10, 6))
plt.plot(daily_articles.index, daily_articles.values, color='blue')
plt.title('Number of Articles Published Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Articles')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 3. Save results to outputs
publisher_counts.to_csv('notebooks/publisher_counts.csv', index=True)
news_df['headline_length'].describe().to_csv('notebooks/headline_length_stats.csv')

print("Task 1 EDA Complete. Results saved.")
