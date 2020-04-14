from . import db
from . import ma

class NewsHeadline(db.Model):
    """Data model for news headlines."""
    """
        {
            'source': {
                'id': 'google-news-in', 
                'name': 'Google News (India)'
            }, 
            'author': 'Times Of India', 
            'title': 'At 10am today, PM Modi will give a clearer view of way forward', 
            'description': 'India News: The Prime Minister is expected to spell out details of the next phase of the national lockdown to combat the Covid-19 pandemic where enforcement of so', 
            'url': 'https://timesofindia.indiatimes.com/india/pm-modi-address-to-nation-at-10am-today-pm-modi-will-give-a-clearer-view-of-way-forward/articleshow/75131265.cms', 
            'urlToImage': 'https://static.toiimg.com/thumb/msid-75131667,width-1070,height-580,imgsize-63575,resizemode-75,overlay-toi_sw,pt-32,y_pad-40/photo.jpg', 
            'publishedAt': '2020-04-14T01:03:51+00:00', 
            'content': 'Subscribe\r\nStart Your Daily Mornings with Times of India Newspaper!Order Now'
        }
    """

    __tablename__ = 'newsheadlines'
    id = db.Column(db.Integer,
                        primary_key=True)

    source_id = db.Column(db.String(255),
                        index=False,
                        unique=False,
                        nullable=True)
    
    source_name = db.Column(db.String(255),
                        index=False,
                        unique=False,
                        nullable=True)

    author = db.Column(db.String(255),
                        index=False,
                        unique=False,
                        nullable=True)

    title = db.Column(db.String(255),
                        index=False,
                        unique=False,
                        nullable=True)

    url = db.Column(db.String(1024),
                        index=False,
                        unique=False,
                        nullable=True)

    urlToImage = db.Column(db.String(1024),
                        index=False,
                        unique=False,
                        nullable=True)
   
    publishedAt = db.Column(db.DateTime,
                        index=False,
                        unique=False,
                        nullable=False)

    sentiment = db.Column(db.Float,
                        index=False,
                        unique=False,
                        nullable=False)
    
    def __repr__(self):
        return '<NewsHeadline {}>'.format(self.title)

class NewsHeadlineSchema(ma.Schema):
    class Meta:
        fields = ('id', 'source_id', 'source_name', 'author', 'title', 'url', 'urlToImage', 'publishedAt', 'sentiment')


class HourlyMean(db.Model):
    """Data model for hourly means."""

    __tablename__ = 'hourlymeans'
    id = db.Column(db.Integer,
                        primary_key=True)

    timestamp = db.Column(db.DateTime,
                        index=False,
                        unique=False,
                        nullable=False)

    mean = db.Column(db.Float,
                        index=False,
                        unique=False,
                        nullable=False)

    def __repr__(self):
        return '<HourlyMean {}>'.format(self.timestamp)

class HourlyMeanSchema(ma.Schema):
    class Meta:
        fields = ('id', 'timestamp', 'mean')
