#importing libraries 
import streamlit as streamlit
import pandas as pd 
import numpy as np
import yfinance as yf  
import pandas_datareader.data as web    
from datetime import datetime   
import capm_function


streamlit.set_page_config(page_title="CAPM",
        page_icon="chart_with_upwards_trend",
        layout="wide")

streamlit.title("Capital Asset Pricing Model")  
#getting input from user
col1, col2 =   streamlit.columns([1,1])  
with col1:     
    stocks_list=streamlit.multiselect("Choose 4 stocks",('TSLA','AAPL','NFLX','MGM','AMZN','NVDA','GOOGL'),['TSLA','AAPL','AMZN','GOOGL'])
with col2:
     year= streamlit.number_input("Number of years",1,10)

# downloading data for SP500



try:
    end = datetime.today()
    start = datetime(
        end.year - year,
        end.month,
        end.day
    )

    SP500 = web.DataReader(['sp500'], 'fred', start, end)

    stocks_df = pd.DataFrame()

    for stock in stocks_list:
        data = yf.download(stock, period=f'{year}y')
        stocks_df[f'{stock}'] = data['Close']


    stocks_df.reset_index(inplace=True)
    SP500.reset_index(inplace=True)


    SP500.columns = ['Date','sp500']

    stocks_df['Date'] = stocks_df["Date"].astype('datetime64[ns]')
    stocks_df['Date'] = stocks_df["Date"].apply(lambda x: str(x)[:10])
    stocks_df['Date'] = pd.to_datetime(stocks_df["Date"])


    stocks_df = pd.merge(
        stocks_df,
        SP500,
        on='Date',
        how='inner'
    )


    # Display data

    col1, col2 = streamlit.columns([1,1])

    with col1:
        streamlit.markdown('## DataFrame head')
        streamlit.dataframe(
            stocks_df.head(),
            use_container_width=True
        )


    with col2:
        streamlit.markdown('## DataFrame tails')
        streamlit.dataframe(
            stocks_df.tail(),
            use_container_width=True
        )


    col1, col2 = streamlit.columns([1,1])


    with col1:
        streamlit.markdown('## Price of all the Stocks')
        streamlit.plotly_chart(
            capm_function.interactive_plot(stocks_df)
        )


    with col2:
        streamlit.markdown(
            '## Price of all the Stocks After Normalizing'
        )

        normalized = capm_function.normalize(stocks_df)

        streamlit.plotly_chart(
            capm_function.interactive_plot(normalized)
        )


    # Daily return

    stocks_daily_return = capm_function.daily_return(stocks_df)


    beta = {}
    alpha = {}


    for i in stocks_daily_return.columns:

        if i != "Date" and i != "sp500":

            b,a = capm_function.calculate_beta(
                stocks_daily_return,
                i
            )

            beta[i] = b
            alpha[i] = a



    beta_df = pd.DataFrame()

    beta_df['Stock'] = list(beta.keys())

    beta_df['Beta Value'] = [
        str(round(i,2))
        for i in beta.values()
    ]


    with col1:

        streamlit.markdown(
            "### Calculated Beta Value"
        )

        streamlit.dataframe(
            beta_df,
            use_container_width=True
        )


    # CAPM Return

    rf = 0

    rm = stocks_daily_return['sp500'].mean()*252


    return_df = pd.DataFrame()

    return_df['Stock'] = list(beta.keys())

    return_df['Return_Value'] = [
        str(round(rf + value*(rm-rf),2))
        for value in beta.values()
    ]


    with col2:

        streamlit.markdown(
            '### Calculated Return using CAPM'
        )

        streamlit.dataframe(
            return_df,
            use_container_width=True
        )


except:

    streamlit.write(
        "please add valid inputs"
    )   