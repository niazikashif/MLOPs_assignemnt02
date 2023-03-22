import tweepy
import pandas as pd
import re
import string
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Authentication credentials for the Twitter API
consumer_key = '7a4YdE6dR374ZZHqMa4thDCpt'
consumer_secret = '6u3Fnprqx8mdBJLWZpHLZPsr2prLOjAy89EVfBVBqwmFQdR4Tg'
access_token = '1056110951404056577-QVtsdZGx4GYVddu0d63dZR5XbNhFFO'
access_token_secret = 'axsXdscBy8jLJtqcJS8tlpNOwuzyTTuuizy8cw2iAVWb5'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def clean_tweet(tweet):
    """
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    """
    tweet = re.sub(r"http\S+|www\S+|https\S+", '', tweet)
    tweet = re.sub(r'\@\w+|\#', '', tweet)
    tweet = re.sub(r'[' + string.punctuation + ']+', ' ', tweet)
    tweet = re.sub(r'\s+', ' ', tweet)
    tweet = tweet.lower().strip()
    return tweet

def get_tweet_sentiment(tweet):
    """
    Utility function to classify sentiment of passed tweet using textblob's sentiment method
    """
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get query and number of tweets from form data
    query = request.form.get('query')
    no_tweets = int(request.form.get('no_tweets'))

    # Search for tweets based on query and number of tweets
    filtered = query + "-filter:retweets"
    tweets = tweepy.Cursor(api.search_tweets, q=filtered, lang="en").items(no_tweets)

    # Clean and analyze tweets
    cleaned_tweets = [clean_tweet(tweet.text) for tweet in tweets]
    sentiment_scores = [get_tweet_sentiment(tweet) for tweet in cleaned_tweets]

    # Count the number of positive, negative, and neutral tweets
    num_positive = sentiment_scores.count('positive')
    num_negative = sentiment_scores.count('negative')
    num_neutral = sentiment_scores.count('neutral')

    # Create dataframe of tweet text and sentiment scores
    df = pd.DataFrame({'tweet': cleaned_tweets, 'sentiment': sentiment_scores})

    # Get lists of positive, negative, and neutral tweets
    positive_tweets = df[df['sentiment'] == 'positive']['tweet'].tolist()
    negative_tweets = df[df['sentiment'] == 'negative']['tweet'].tolist()
    neutral_tweets = df[df['sentiment'] == 'neutral']['tweet'].tolist()


    # Render results page with dataframe and sentiment counts
    return render_template('results.html', query=query, no_tweets=no_tweets, num_positive=num_positive,
                           num_negative=num_negative, num_neutral=num_neutral,table=df)

if __name__ == '__main__':
    app.run(debug=True)
