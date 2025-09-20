from transformers import pipeline
import pandas as pd

def analyze_sentiment(df, text_column='text'):
    """
    Analyze sentiment of tweet text using a pre-trained model.
    :param df: pd.DataFrame with a text column
    :param text_column: str, name of the text column
    :return: pd.DataFrame with sentiment label and score
    """
    # Load sentiment analysis pipeline
    sentiment_analyzer = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')
    
    # Analyze each text
    def get_sentiment(text):
        result = sentiment_analyzer(text)[0]
        return {'label': result['label'], 'score': result['score']}

    df = df.copy()
    sentiments = df[text_column].apply(get_sentiment)
    df['sentiment_label'] = [s['label'] for s in sentiments]
    df['sentiment_score'] = [s['score'] for s in sentiments]
    return df
