import re
import pandas as pd

def clean_text(df, text_column='text'):
    """
    Clean tweet text by removing RT, URLs, mentions, and special characters.
    :param df: pd.DataFrame with a text column
    :param text_column: str, name of the text column
    :return: pd.DataFrame with cleaned text
    """
    df = df.copy()
    df[text_column] = df[text_column].str.replace(r'^RT @\w+: ', '', regex=True)  # Remove RT
    df[text_column] = df[text_column].str.replace(r'http\S+|www\S+|https\S+', '', regex=True)  # Remove URLs
    df[text_column] = df[text_column].str.replace(r'@\w+', '', regex=True)  # Remove mentions
    df[text_column] = df[text_column].str.replace(r'[^\w\s]', '', regex=True)  # Remove special chars
    df[text_column] = df[text_column].str.lower()  # Convert to lowercase
    return df
