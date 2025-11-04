# forecaster.py
from prophet import Prophet
import pandas as pd

def train_prophet(daily_df, weekly=True, monthly=False):
    m = Prophet(daily_seasonality=False, weekly_seasonality=weekly, yearly_seasonality=False)
    if monthly:
        m.add_seasonality(name='monthly', period=30.5, fourier_order=5)
    m.fit(daily_df.rename(columns={"ds":"ds","y":"y"}))
    return m

def predict_prophet(m, periods=30):
    fut = m.make_future_dataframe(periods=periods, freq='D')
    fc = m.predict(fut)
    return fc
