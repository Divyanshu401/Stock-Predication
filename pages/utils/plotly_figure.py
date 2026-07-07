import plotly.graph_objects as go
import dateutil
#import pandas_ta as pta 
from dateutil.relativedelta import relativedelta
from ta.momentum import RSIIndicator
from ta.trend import MACD as MACDIndicator
import datetime
def plotly_table(dataframe):

    headerColor = "grey"
    rowColor = "lightgrey"
    rowOddColor = "white"

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["<b>" + str(i) + "</b>" for i in dataframe.columns],
            line_color="white",
            fill_color="#203F7F",
            align="center",
            font=dict(color="white", size=15),
            height=35
        ),

        cells=dict(
            values=[
                ["<b>" + str(i) + "</b>" for i in dataframe.index]
            ] + [
                dataframe[i] for i in dataframe.columns
            ],
            fill_color=[rowOddColor, rowColor],
            align="left",
            line_color="white",
            font=dict(color="black", size=15)
        )
    )])

    fig.update_layout(
        height=400,
        margin=dict(l=0, r=0, t=0, b=0)
    )

    return fig

def moving_average_forecast(dataframe):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=dataframe.index,
            y=dataframe["Close"],
            mode="lines",
            name="Forecast"
        )
    )

    fig.update_layout(
        title="Stock Price Forecast",
        xaxis_title="Date",
        yaxis_title="Close Price",
        height=500,
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    return fig

# Filter Data Function
def filter_data(dataframe, num_period):

    if num_period == "1m":
        date = dataframe.index[-1] - relativedelta(months=1)

    elif num_period == "5d":
        date = dataframe.index[-1] - relativedelta(days=5)

    elif num_period == "6m":
        date = dataframe.index[-1] - relativedelta(months=6)

    elif num_period == "1y":
        date = dataframe.index[-1] - relativedelta(years=1)

    elif num_period == "5y":
        date = dataframe.index[-1] - relativedelta(years=5)

    elif num_period == "ytd":
        date = datetime.datetime(
            dataframe.index[-1].year,
            1,
            1
        )

    else:
        return dataframe.reset_index()

    # Reset index only once
    dataframe = dataframe.reset_index()

    # Remove timezone if present
    if dataframe["Date"].dt.tz is not None:
        dataframe["Date"] = dataframe["Date"].dt.tz_localize(None)

    # Remove timezone from comparison date if present
    if hasattr(date, "tzinfo") and date.tzinfo is not None:
        date = date.replace(tzinfo=None)

    return dataframe[
        dataframe["Date"] >= date
    ]
# Close Price Chart
def close_chart(dataframe, num_period):

    dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()


    fig.add_trace(
        go.Scatter(
            x=dataframe["Date"],
            y=dataframe["Open"],
            name="Open",
            line=dict(width=2)
        )
    )


    fig.add_trace(
        go.Scatter(
            x=dataframe["Date"],
            y=dataframe["Close"],
            name="Close",
            line=dict(width=2)
        )
    )


    fig.add_trace(
        go.Scatter(
            x=dataframe["Date"],
            y=dataframe["High"],
            name="High",
            line=dict(width=2)
        )
    )


    fig.add_trace(
        go.Scatter(
            x=dataframe["Date"],
            y=dataframe["Low"],
            name="Low",
            line=dict(width=2)
        )
    )


    fig.update_xaxes(
        rangeslider_visible=True
    )


    fig.update_layout(
        height=500,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white"
    )


    return fig



# Candlestick Chart
def candlestick(dataframe, num_period):

    dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()


    fig.add_trace(
        go.Candlestick(
            x=dataframe["Date"],
            open=dataframe["Open"],
            high=dataframe["High"],
            low=dataframe["Low"],
            close=dataframe["Close"]
        )
    )


    fig.update_layout(
        showlegend=False,
        height=500,
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white"
    )


    return fig



# RSI Indicator
def RSI(dataframe, num_period):

    dataframe["RSI"] = RSIIndicator(
        close=dataframe["Close"],
        window=14
    ).rsi()

    dataframe = filter_data(
        dataframe,
        num_period
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=dataframe["Date"],
            y=dataframe["RSI"],
            name="RSI"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=dataframe["Date"],
            y=[70] * len(dataframe),
            name="Overbought"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=dataframe["Date"],
            y=[30] * len(dataframe),
            name="Oversold"
        )
    )

    fig.update_layout(
        yaxis=dict(range=[0,100]),
        height=300
    )

    return fig
# Moving Average
def Moving_average(dataframe, num_period):

    dataframe["SMA 50"] = (
        dataframe["Close"]
        .rolling(window=50)
        .mean()
    )

    dataframe = filter_data(
        dataframe,
        num_period
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=dataframe["Date"],
            y=dataframe["Close"],
            name="Close"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=dataframe["Date"],
            y=dataframe["SMA 50"],
            name="SMA 50"
        )
    )

    fig.update_layout(
        height=500,
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    return fig
# MACD Indicator
# def MACD(dataframe, num_period):

#     macd = ta.macd(
#         dataframe["Close"]
#     )


#     dataframe["MACD"] = macd["MACD_12_26_9"]
#     dataframe["MACD_signal"] = macd["MACDs_12_26_9"]
#     dataframe["MACD_hist"] = macd["MACDh_12_26_9"]


#     dataframe = filter_data(
#         dataframe,
#         num_period
#     )


#     fig = go.Figure()


#     fig.add_trace(
#         go.Scatter(
#             x=dataframe["Date"],
#             y=dataframe["MACD"],
#             name="MACD"
#         )
#     )


#     fig.add_trace(
#         go.Scatter(
#             x=dataframe["Date"],
#             y=dataframe["MACD_signal"],
#             name="Signal"
#         )
#     )


#     fig.update_layout(
#         height=300,
#         plot_bgcolor="white",
#         paper_bgcolor="white"
#     )


#     return fig
def MACD(dataframe, num_period):

    indicator = MACDIndicator(close=dataframe["Close"])

    dataframe["MACD"] = indicator.macd()
    dataframe["MACD_signal"] = indicator.macd_signal()

    dataframe = filter_data(dataframe, num_period)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=dataframe["Date"],
            y=dataframe["MACD"],
            name="MACD"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=dataframe["Date"],
            y=dataframe["MACD_signal"],
            name="Signal"
        )
    )

    fig.update_layout(
        height=300,
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    return fig














