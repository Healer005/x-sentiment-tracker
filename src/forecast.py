from prophet import Prophet
import pandas as pd
from datetime import datetime

def forecast_sentiment(df, sentiment_column='sentiment_score', date_column='created_at', periods=24):
    """
    Forecast future sentiment scores using Prophet.
    :param df: pd.DataFrame with sentiment and date columns
    :param sentiment_column: str, name of the sentiment score column
    :param date_column: str, name of the date column
    :param periods: int, number of future periods to forecast (e.g., hours)
    :return: pd.DataFrame with historical and forecasted data
    """
    df = df.copy()
    df[date_column] = pd.to_datetime(df[date_column])
    df[date_column] = df[date_column].dt.tz_localize(None)  # Remove timezone
    df = df.sort_values(date_column)
    
    # Prepare data for Prophet (y = sentiment score, ds = date)
    prophet_df = df[[date_column, sentiment_column]].rename(columns={date_column: 'ds', sentiment_column: 'y'})
    
    # Fit model
    model = Prophet(daily_seasonality=True)
    model.fit(prophet_df)
    
    # Make future dataframe
    future = model.make_future_dataframe(periods=periods, freq='h')  # Hourly forecasts
    forecast = model.predict(future)
    
    # Combine historical and forecast
    result = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    result.loc[:, 'type'] = ['Historical' if i < len(prophet_df) else 'Forecast' for i in range(len(result))]
    return result

# # Test (remove after testing)
# if __name__ == "__main__":
#     # Sample DataFrame (replace with actual sentiment data later)
#     sample_df = pd.DataFrame({
#         'created_at': ['2025-09-20 09:00', '2025-09-20 10:00', '2025-09-20 11:00'],
#         'sentiment_score': [0.8, 0.6, 0.9]
#     })
#     forecast_df = forecast_sentiment(sample_df, periods=6)
#     print(forecast_df)