import yfinance as yf
import pandas as pd
import numpy as np

from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA

from sklearn.metrics import mean_squared_error


def get_data(ticker):

    data = yf.download(
        ticker,
        start="2024-01-01",
        progress=False
    )

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    return data["Close"]


def stationary_check(close_price):

    result = adfuller(close_price.dropna())

    return result[1]


def get_differencing_order(close_price):

    temp = close_price.copy()

    d = 0

    while stationary_check(temp) > 0.05:

        temp = temp.diff().dropna()

        d += 1

    return d


def fit_model(close_price, d):

    model = ARIMA(
        close_price,
        order=(5, d, 1)
    )

    model_fit = model.fit()

    return model_fit


def evaluate_model(close_price, d):

    train = close_price[:-30]

    test = close_price[-30:]

    model = fit_model(train, d)

    prediction = model.forecast(steps=30)

    rmse = np.sqrt(
        mean_squared_error(
            test,
            prediction
        )
    )

    return round(rmse, 2)


def get_forecast(close_price, d):

    model = fit_model(close_price, d)

    forecast = model.forecast(steps=30)

    future_dates = pd.date_range(
        start=close_price.index[-1] + pd.Timedelta(days=1),
        periods=30,
        freq="D"
    )

    forecast = pd.Series(
        forecast.values,
        index=future_dates,
        name="Close"
    )

    return forecast
