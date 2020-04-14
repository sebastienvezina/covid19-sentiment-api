from joblib import load
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import os
import csv
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))

def predict(strings):
    m = load(dir_path+'/../model/model.joblib')

    predictions = m.predict(strings)
    return predictions

import csv


tweets = []
with open(dir_path + '/../data/sample.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

for d in data:
    tweets.append(d[0])

#print(data)
predictions = predict(tweets)

mean = np.mean(predictions)
print("mean sentiment: " + str(mean))