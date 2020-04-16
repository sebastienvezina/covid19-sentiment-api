from flask import request, render_template, make_response, jsonify
from datetime import datetime, timedelta
from flask import current_app as app
from .models import db, HourlyMean, HourlyMeanSchema, NewsHeadline, NewsHeadlineSchema
from newsapi import NewsApiClient
from joblib import load
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import os

@app.route("/hourlymeans/<mode>", methods=['GET'])
def get_hourlymeans(mode):
    # define marshmallow schema
    hourlymeans_schema = HourlyMeanSchema(many=True)
        
    if '24' == mode:
        last24 = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:00:00")
        hourly_means_query = HourlyMean.query.filter(HourlyMean.timestamp >= last24)
    elif '48' == mode:
        last48 = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d %H:00:00")
        hourly_means_query = HourlyMean.query.filter(HourlyMean.timestamp >= last48)
    elif '7d' == mode:
        last7d = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:00:00")
        hourly_means_query = HourlyMean.query.filter(HourlyMean.timestamp >= last7d)
    else:
        hourly_means_query = HourlyMean.query.all()
    
    hourly_means = hourlymeans_schema.dump(hourly_means_query)
    return jsonify(hourly_means)

@app.route("/newsheadlines/<mode>", methods=['GET'])
def get_newsheadlines(mode):
    # define marshmallow schema
    newsheadlines_schema = NewsHeadlineSchema(many=True)

    if 'best5' == mode:
        newsheadlines_query = NewsHeadline.query.order_by(NewsHeadline.sentiment.desc()).limit(5).all()
    elif 'worse5' == mode:
        newsheadlines_query = NewsHeadline.query.order_by(NewsHeadline.sentiment.asc()).limit(5).all()    
    else:
        newsheadlines_query = NewsHeadline.query.all()

    newsheadlines = newsheadlines_schema.dump(newsheadlines_query)
    return jsonify(newsheadlines)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

@app.route("/update")
def update():
    ###
    # Uses https://newsapi.org to fetch latest headlines about Covid-19 and store them into a CSV file
    #
    newsapi = NewsApiClient(api_key=app.config["NEWSAPI_KEY"])

    articles = []
    top_headlines = newsapi.get_top_headlines(q='covid-19',
                                              language='en',
                                              page_size=100)
    articles = top_headlines['articles']

    top_headlines = newsapi.get_top_headlines(q='coronavirus',
                                              language='en',
                                              page_size=100)
    articles += top_headlines['articles']
    
    model = load(os.path.join(app.config["APP_BASEDIR"],'model','model_v2.joblib'))
    totalSentiment = 0.0
    for a in articles:
        timestamp_parts = a['publishedAt'].split("T")
        timestamp = timestamp_parts[0] + " " + timestamp_parts[1][:8]
   
        new_newsheadline = NewsHeadline(
                                    source_id=a['source']['id'],
                                    source_name=a['source']['name'],
                                    author=a['author'],
                                    title=a['title'],
                                    url=a['url'],
                                    urlToImage=a['urlToImage'],
                                    publishedAt=datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S'),
                                    sentiment=0
                                    )

        title_iterable = [
            new_newsheadline.title
        ]
        predictions = model.predict_proba(title_iterable)
        prediction_positive = predictions[0][1]
        prediction_score = prediction_positive * 4      
        new_newsheadline.sentiment = prediction_score
        
        # add total
        totalSentiment += prediction_score
        
        db.session.add(new_newsheadline)
        db.session.commit()

    mean = totalSentiment / len(articles)

    new_hourlymean = HourlyMean(timestamp=datetime.now(), mean=mean)

    db.session.add(new_hourlymean)
    db.session.commit()

    return "Done. Thank you!"

@app.route('/sync')
def sync():
    '''
    import csv
    dir_path = os.path.dirname(os.path.realpath(__file__))

    with open(os.path.join(app.config["APP_BASEDIR"], 'data', 'hourly_means.csv'), newline='\n', encoding='utf-8') as f:
        reader = csv.reader(f)
        hourly_means_csv = list(reader)
    
    for h in hourly_means_csv:
        new_hourlymean = HourlyMean(timestamp=datetime.strptime(h[0], '%Y-%m-%d %H:%M:%S'), mean=h[1])
        db.session.add(new_hourlymean)
        db.session.commit()
    '''
    return "Done syncing"

@app.route('/ip')
def ip():
    ip = request.remote_addr
    return "Client IP is: " + str(ip)