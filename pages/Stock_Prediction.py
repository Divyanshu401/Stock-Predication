import streamlit as streamlit
import pandas as pd

from pages.utils.model_train import (
    get_data,
    stationary_check,
    get_differencing_order,
    evaluate_model,
    get_forecast
)

from pages.utils.plotly_figure import (
    plotly_table,
    moving_average_forecast
)


streamlit.set_page_config(
    page_title="Stock Prediction",
    page_icon="📈",
    layout="wide"
)

streamlit.title("Stock Prediction")


ticker = streamlit.text_input(
    "Stock Ticker",
    "AAPL"
).upper()


if ticker:

    close_price = get_data(ticker)

    if close_price.empty:

        streamlit.error("No data found.")

        streamlit.stop()

    streamlit.subheader(f"{ticker} Closing Price")

    streamlit.line_chart(close_price)

    p_value = stationary_check(close_price)

    streamlit.write("ADF Test p-value :", round(p_value, 5))

    d = get_differencing_order(close_price)

    streamlit.write("Differencing Order :", d)

    rmse = evaluate_model(
        close_price,
        d
    )

    streamlit.metric(
        "RMSE",
        rmse
    )

    forecast = get_forecast(
        close_price,
        d
    )

    streamlit.subheader("Forecast (Next 30 Days)")

    streamlit.write(forecast)

    history_df = close_price.to_frame(name="Close")

    forecast_df = forecast.to_frame(name="Close")

    forecast_data = pd.concat(
        [
            history_df,
            forecast_df
        ]
    )

    streamlit.plotly_chart(
        moving_average_forecast(
            forecast_data
        ),
        use_container_width=True
    )

    streamlit.subheader("Forecast Table")

    fig = plotly_table(
        forecast_df.round(2)
    )

    streamlit.plotly_chart(
        fig,
        use_container_width=True
    )

