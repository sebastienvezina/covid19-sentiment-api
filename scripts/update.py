import os
import csv

dir_path = os.path.dirname(os.path.realpath(__file__))
###
# Uses https://newsapi.org to fetch latest headlines about Covid-19 and store them into a CSV file
#
from newsapi import NewsApiClient

print("Fetching news articles...")
newsapi = NewsApiClient(api_key='e3591106e13347bc92a3d1ab29a5c341')

articles = []
top_headlines = newsapi.get_top_headlines(q='covid-19',
                                          language='en',
                                          page_size=100)
articles = top_headlines['articles']

top_headlines = newsapi.get_top_headlines(q='coronavirus',
                                          language='en',
                                          page_size=100)
articles += top_headlines['articles']

dir_path = os.path.dirname(os.path.realpath(__file__))

with open(dir_path + '/../data/news.csv', 'w', newline='\n', encoding='utf-8') as f:
    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
    for a in articles:
        row = [a['author'], a['title'], a['description'], a['url'], a['urlToImage'], a['publishedAt'], 0]
        wr.writerow(row)

###
# Loads up our Naive Bayes model and computes sentiment on latest headlines 
#
from joblib import load
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np
def predict(strings):
    m = load(dir_path+'/../model/model.joblib')

    predictions = m.predict(strings)
    return predictions

import csv

with open(dir_path + '/../data/news.csv', newline='\n', encoding='utf-8') as f:
    reader = csv.reader(f)
    articles = list(reader)

titles = []
for a in articles:
    titles.append(a[1])

print("Making predictions...")
predictions = predict(titles)

print(predictions)

mean = np.mean(predictions)
print("Mean sentiment: " + str(mean))

#keep the mean with a timestamp
from datetime import datetime
dt = datetime.now()
current_sentiment = [
    str(dt.year) + '-' + str(dt.month) + '-' + str(dt.day) + ' ' + str(dt.hour) + ':00:00',
    mean
]
print("Storing new hourly mean...")
with open(dir_path + '/../data/hourly_means.csv', 'a', newline='\n', encoding='utf-8') as f:
    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
    wr.writerow(current_sentiment)


#update articles with sentiment prediction
print("Updating latest news article sentiment predictions...")
with open(dir_path + '/../data/news.csv', 'w', newline='\n', encoding='utf-8') as f:
    wr = csv.writer(f, quoting=csv.QUOTE_ALL)

    for i in range(0, len(predictions)):
        p = predictions[i]
        articles[i][-1] = p
        wr.writerow(articles[i])

print("Done. Thank you!")