import tweepy
from dotenv import load_dotenv
import os
import pandas as pd
from preprocess import clean_text
from sentiment import analyze_sentiment

load_dotenv()

def fetch_tweets(query, max_results=10):
    client = tweepy.Client(bearer_token=os.getenv('X_BEARER_TOKEN'))
    try:
        tweets = client.search_recent_tweets(
            query=query,
            tweet_fields=['text', 'created_at'],
            max_results=max_results
        )
    except tweepy.TooManyRequests as e:
        print(f"Rate limit hit: {e}")
        return pd.DataFrame()
    if not tweets.data:
        print("No tweets found for the query.")
        return pd.DataFrame()
    data = [{'text': tweet.text, 'created_at': tweet.created_at} for tweet in tweets.data]
    df = pd.DataFrame(data)
    cleaned_df = clean_text(df)
    sentiment_df = analyze_sentiment(cleaned_df)
    sentiment_df.to_csv('data/sentiment_tweets.csv', index=False)
    return sentiment_df