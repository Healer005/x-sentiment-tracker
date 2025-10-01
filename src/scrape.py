import tweepy
from dotenv import load_dotenv
import os
import pandas as pd
from preprocess import clean_text
from sentiment import analyze_sentiment
from forecast import forecast_sentiment

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
    forecast_df = forecast_sentiment(sentiment_df, periods=24)  # Forecast 24 hours
    forecast_df.to_csv('data/forecasted_sentiment.csv', index=False)
    return forecast_df

# Dynamic input for testing (remove after)
if __name__ == "__main__":
    keyword = input("Enter a keyword (e.g., 'Bitcoin'): ").strip()
    if not keyword:
        keyword = "Bitcoin"
    query = f"{keyword} lang:en"
    df = fetch_tweets(query, max_results=10)
    print(f"Analyzed and forecasted {len(df)} entries for '{keyword}':")
    print(df)