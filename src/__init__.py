import pandas as pd
import numpy as np
import matplotlib as plt
#import pynance as py
import seaborn as sns
#rom vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

df = pd.read_csv("C:\\Users\\nadew\\10x\\week1\\Nova_Financial_Solutions\\data_used\\raw\\raw_analyst_ratings.csv")
print(df.head(10))
# ###headline lenght
# df['head_lenght']=df['headline'].apply(len)
# print(df['head_lenght'])
# headline_status=df['head_lenght'].describe()
# print(headline_status)

# ###article_per_publisher
# publisher_counts=df['publisher'].value_counts()
# top_publishers=publisher_counts.head(10)
# print(top_publishers)




############ time analysis#############################################


#df['date']=pd.to_datetime(df['date'],format='mixed', errors='coerce',utc=True)
#print(df['date'])
######EXRACTING COMPONENTS FOR ANALYSIS BY WEAK, MONTH AND YEAR

#df['day_of_weak']=df['date'].dt.day_name()
#df['month']=df['date'].dt.month
#df['year']=df['date'].dt.year

#articles publishe by days of the weak, month,
#day_counts=df['day_of_weak'].value_counts()
#month_counts=df['month'].value_counts()
#year_counts=df['year'].value_counts()

# articles published by days of the weak

# plt.figure(figsize=(10, 6))
# sns.countplot(data=df, x=df['day_of_weak'], order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
# plt.title('Articles Published by Day of the Week')
# plt.xlabel('Day of the Week')
# plt.ylabel('Number of Articles')
# plt.show()
# ##################ARTICLES PUBLISHED BY MONTS OF THE YEAR ###################################
# #plt.figure(figsize=(10, 6))
# #sns.countplot(data=df, x=df['month'])
#plt.title('Number of Articles Published by Month')
#plt.xlabel('Month')
#plt.ylabel('Number of Articles')
#plt.show()
#######################################ARTICLES DISTIRBUTION BY YEAR############################################
#def articles_By_years():
  #plt.figure(figsize=(10, 6))
  #sns.countplot(data=df, x=df['year'])
  #plt.title('Number of Articles Published by year')
  #plt.xlabel('years')
  #plt.ylabel('Number of Articles')
  #plt.show()

#articles_By_years()