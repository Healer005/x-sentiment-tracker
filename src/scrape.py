import tweepy
from dotenv import load_dotenv
import os
import pandas as pd
from preprocess import clean_text  # Import the cleaning function

load_dotenv()  # Load .env variables

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
    cleaned_df = clean_text(df)  # Clean the fetched tweets
    cleaned_df.to_csv('data/raw_tweets.csv', index=False)  # Save to CSV
    return cleaned_df

# # Main block for dynamic input testing
# if __name__ == "__main__":
#     keyword = input("Enter a keyword for tweets (e.g., 'Bitcoin'): ").strip()
#     if not keyword:
#         keyword = "Bitcoin"  # Default fallback
#     query = f"{keyword} lang:en"
#     df = fetch_tweets(query, max_results=10)
#     print(f"Fetched and cleaned {len(df)} tweets for '{keyword}':")
#     print(df)