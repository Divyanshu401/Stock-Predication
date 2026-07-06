import streamlit
streamlit.set_page_config(
    page_title="Trading App",
    page_icon="heavy_dollar_sign",
    layout="wide"

)
streamlit.title("Trading Guide App :bar_chart:")
streamlit.header("We provide the Greatest platform for you to collect all information prior to investing in stocks.")
streamlit.image("app.png")
streamlit.markdown("### we provide the following services: ")
streamlit.markdown("#### :one: Stock Information")

streamlit.write(
    "Through this page, you can see all the information about stock."
)


streamlit.markdown("#### :two: Stock Prediction")

streamlit.write(
    "You can explore predicted closing prices for the next 30 days based on historical stock data and advanced forecasting models."
)


streamlit.markdown("#### :three: CAPM Return")

streamlit.write(
    "Discover how the Capital Asset Pricing Model (CAPM) calculates the expected return of different stocks based on its risk and return."
)


streamlit.markdown("#### :four: CAPM Beta")

streamlit.write(
    "Calculates Beta and Expected Return for Individual Stocks."
)
