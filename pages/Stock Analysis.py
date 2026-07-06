#importing libraries 
import streamlit as streamlit
import pandas as pd 
import numpy as np
import plotly.graph_objects as go
import yfinance as yf     
import datetime   
import ta 
# from pages.Utils.plotly_figure import plotly_table
# from pages.utils.plotly_figure import plotly_table
from pages.utils.plotly_figure import (
    plotly_table,
    candlestick,
    close_chart,
    RSI,
    MACD,
    Moving_average
)
streamlit.set_page_config(
    page_title="Stock Analysis",
    page_icon="page_with_curl",
    layout="wide"
)
streamlit.title("Stock Anaysis")
col1, col2, col3 = streamlit.columns(3)
today= datetime.date.today()
with col1:
    ticker=streamlit.text_input("Enter Ticket","TSLA")
with col2:
    start_date=streamlit.date_input("choose Start Date",datetime.date(today.year-1,today.month,today.day)) 
with col3:
    end_date=streamlit.date_input("choose End Date",datetime.date(today.year,today.month,today.day))     
streamlit.subheader(ticker)
stock = yf.Ticker(ticker)
streamlit.write(stock.info["longBusinessSummary"])
streamlit.write("**Sector**",stock.info['sector'])
streamlit.write("**full Time Employees:**",stock.info['fullTimeEmployees'])
streamlit.write("**Website**",stock.info['website'])   

col1, col2 = streamlit.columns(2)
with col1:
    df=pd.DataFrame(index=['market cap','Beta','EPS','PE Ratio'])
    df['']=[stock.info["marketCap"],stock.info["beta"],stock.info["trailingEps"],stock.info["trailingPE"]]
    fig_df = plotly_table(df)
    streamlit.plotly_chart(fig_df,use_container_width=True) 
with col2:
    df=pd.DataFrame(index=['Quick Ratio','Revenue per share','Profit Margins','Debt to Equity','Return on Equity'])    
    df['']=[stock.info["quickRatio"],stock.info["revenuePerShare"],stock.info["profitMargins"],stock.info["debtToEquity"],stock.info["returnOnEquity"]]
    fig_df = plotly_table(df)
    streamlit.plotly_chart(fig_df,use_container_width=True) 

import pandas as pd


data = yf.download(
    ticker,
    start=start_date,
    end=end_date
)


# Remove MultiIndex from yfinance
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)



col1, col2, col3 = streamlit.columns(3)



# Convert Close value to float
current_price = float(
    data["Close"].iloc[-1]
)


previous_price = float(
    data["Close"].iloc[-2]
)


daily_change = current_price - previous_price



col1.metric(
    label=f"{ticker} Price",
    value=f"{current_price:.2f}",
    delta=f"{daily_change:.2f}"
)



last_10_df = (
    data
    .tail(10)
    .sort_index(ascending=False)
    .round(3)
)



fig = plotly_table(
    last_10_df
)



streamlit.write(
    "Historical Data (Last 10 Days)"
)



streamlit.plotly_chart(
    fig,
    use_container_width=True
)
import streamlit


col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = streamlit.columns(10)

num_period = ''
with col1:
    if streamlit.button("5D"):
        num_period="5d"


with col2:
    if streamlit.button("1M"):
        num_period="1m"


with col3:
    if streamlit.button("6M"):
        num_period="6m"


with col4:
    if streamlit.button("YTD"):
        num_period="ytd"


with col5:
    if streamlit.button("1Y"):
        num_period="1y"


with col6:
    if streamlit.button("5Y"):
        num_period="5y"


with col7:
    if streamlit.button("MAX"):
        num_period="max"

col1 ,col2 ,col3 = streamlit.columns([1,1,4])
with col1:
    chart_type=streamlit.selectbox("",["Candle","Line"]) 
with col2:
    if chart_type=="Candle":
        indicators=streamlit.selectbox('',("RSI","MACD"))
    else:
        indicators=streamlit.selectbox('',("RSI","Moving Average","MACD"))
ticker_ = yf.Ticker(ticker)
# Get maximum historical data
new_df1 = ticker_.history(period="max")


# Get selected period data
data1 = ticker_.history(period="max")

if num_period == "":

    if chart_type == "Candle" and indicators == "RSI":

        streamlit.plotly_chart(
            candlestick(data1, "1y"),
            use_container_width=True
        )

        streamlit.plotly_chart(
            RSI(data1, "1y"),
            use_container_width=True
        )


    elif chart_type == "Candle" and indicators == "MACD":

        streamlit.plotly_chart(
            candlestick(data1, "1y"),
            use_container_width=True
        )

        streamlit.plotly_chart(
            MACD(data1, "1y"),
            use_container_width=True
        )


    elif chart_type == "Line" and indicators == "RSI":

        streamlit.plotly_chart(
            close_chart(data1, "1y"),
            use_container_width=True
        )

        streamlit.plotly_chart(
            RSI(data1, "1y"),
            use_container_width=True
        )


    elif chart_type == "Line" and indicators == "Moving Average":

        streamlit.plotly_chart(
            Moving_average(data1, "1y"),
            use_container_width=True
        )


    elif chart_type == "Line" and indicators == "MACD":

        streamlit.plotly_chart(
            close_chart(data1, "1y"),
            use_container_width=True
        )

        streamlit.plotly_chart(
            MACD(data1, "1y"),
            use_container_width=True
        )


else:

    if chart_type == "Candle" and indicators == "RSI":

        streamlit.plotly_chart(
            candlestick(new_df1, num_period),
            use_container_width=True
        )

        streamlit.plotly_chart(
            RSI(new_df1, num_period),
            use_container_width=True
        )


    elif chart_type == "Candle" and indicators == "MACD":

        streamlit.plotly_chart(
            candlestick(new_df1, num_period),
            use_container_width=True
        )

        streamlit.plotly_chart(
            MACD(new_df1, num_period),
            use_container_width=True
        )


    elif chart_type == "Line" and indicators == "RSI":

        streamlit.plotly_chart(
            close_chart(new_df1, num_period),
            use_container_width=True
        )

        streamlit.plotly_chart(
            RSI(new_df1, num_period),
            use_container_width=True
        )


    elif chart_type == "Line" and indicators == "Moving Average":

        streamlit.plotly_chart(
            Moving_average(new_df1, num_period),
            use_container_width=True
        )


    elif chart_type == "Line" and indicators == "MACD":

        streamlit.plotly_chart(
            close_chart(new_df1, num_period),
            use_container_width=True
        )

        streamlit.plotly_chart(
            MACD(new_df1, num_period),
            use_container_width=True
        )
