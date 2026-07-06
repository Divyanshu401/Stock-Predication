# import yfinance as yf
# import pandas as pd
# import numpy as np

# from sklearn.metrics import mean_squared_error
# from sklearn.preprocessing import StandardScaler

# from statsmodels.tsa.stattools import adfuller
# from statsmodels.tsa.arima.model import ARIMA  

# def get_data(ticker):

#     """
#     Download historical stock prices.
#     Returns only the Close price.
#     """

#     stock_data = yf.download(
#         ticker,
#         start="2024-01-01",
#         progress=False
#     )

#     # Remove MultiIndex if Yahoo returns one
#     if isinstance(stock_data.columns, pd.MultiIndex):
#         stock_data.columns = stock_data.columns.get_level_values(0)

#     return stock_data["Close"]



# def stationary_check(close_price):
#     """
#     Check whether the time series is stationary.
#     Returns the p-value from the ADF test.
#     """

#     result = adfuller(close_price.dropna())

#     p_value = result[1]

#     return p_value

# def get_differencing_order(close_price):

#     d = 0

#     temp = close_price.copy()

#     while stationary_check(temp) > 0.05:

#         temp = temp.diff().dropna()

#         d += 1

#     return d

# def fit_model(data, d):

#     model = ARIMA(
#         data,
#         order=(5, d, 1)
#     )

#     model_fit = model.fit()

#     return model_fit

# def get_rolling_mean(close_price, window=30):

#     rolling_price = (
#         close_price
#         .rolling(window=window)
#         .mean()
#         .dropna()
#     )

#     return rolling_price


# def evaluate_model(data, d):

#     train_data = data[:-30]

#     test_data = data[-30:]

#     model_fit = fit_model(train_data, d)

#     predictions = model_fit.forecast(steps=30)

#     rmse = np.sqrt(
#         mean_squared_error(
#             test_data,
#             predictions
#         )
#     )

#     return rmse

# def get_forecast(data, d):

#     model = fit_model(data, d)

#     forecast = model.forecast(
#         steps=30
#     )

#     return forecast

# # Scale Data
# def scaling(close_price):

#     scaler = StandardScaler()

#     scaled_data = scaler.fit_transform(
#         np.array(close_price).reshape(-1, 1)
#     )

#     return scaled_data, scaler

# # forecast    
# def get_forecast(data, d):

#     model = fit_model(data, d)

#     forecast = model.forecast(steps=30)

#     last_date = data.index[-1]

#     future_dates = pd.date_range(
#         start=last_date + pd.Timedelta(days=1),
#         periods=30,
#         freq="D"
#     )

#     forecast = pd.Series(
#         forecast.values,
#         index=future_dates
#     )

#     return forecast 

# # Convert Scaled Data Back to Original Values
# def inverse_scaling(scaler, scaled_data):

#     original_price = scaler.inverse_transform(
#         np.array(scaled_data).reshape(-1, 1)
#     )

#     return original_price

# def get_forecast(data, d):

#     model = fit_model(data, d)

#     forecast = model.forecast(
#         steps=30
#     )

#     return forecast
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
