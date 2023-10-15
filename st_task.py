import numpy as np
import pandas as pd
import yfinance as yf
import plotly.express as px
import streamlit as st
from datetime import datetime

# Set the page title and sidebar options
st.set_page_config(
    page_title="Stock Screener App",
    layout="wide",
)

# Title and header
st.title("Stock Screener App 📈")
st.header("Filter stocks based on specific conditions")

# Get user input for the stock ticker
ticker_val = st.text_input("Enter the stock ticker (e.g., AAPL for Apple):")

# Load stock information and display basic details
if ticker_val:
    ticker = yf.Ticker(ticker_val)
    st.subheader(f"Information about {ticker_val}")
    st.dataframe(pd.DataFrame(ticker.info))
    # st.DataFrame(ticker.info).iloc[0, 0:8]

    # Load stock splits, dividends, major holders, institutional holders, and cashflow data
    st.subheader("Additional Information")
    # st.dataframe(ticker.splits)
    # st.dataframe(ticker.dividends)
    # st.dataframe(ticker.major_holders)
    # st.dataframe(ticker.institutional_holders)
    # st.dataframe(ticker.cashflow)

    # Get today's date
    today = datetime.now().date().strftime("%Y-%m-%d")

    # Plot the historical closing price of the stock
    st.subheader("Historical Closing Price")
    fig = px.line(ticker.history(start="2002-10-01", end=today)["Close"])
    fig.update_xaxes(range=["2019-03-01", None])
    st.plotly_chart(fig)

    # Get user input for the date range
    start_date = st.text_input("Enter the start date (YYYY-MM-DD):")
    end_date = st.text_input("Enter the end date (YYYY-MM-DD):")

    # Download stock data based on the date range
    if start_date and end_date:
        stock_df = yf.download(ticker_val, start=start_date, end=end_date)
        stock_df = stock_df[['Open', 'High', 'Low', 'Close']]

        # Get user input for filtering conditions
        st.subheader("Filter Stock Data")
        choice = st.radio(
            "Select a filter condition:",
            ("Open=Low and Close=High", "Open=Low or Close=High", "Open=High and Close=Low", "Open=High or Close=Low")
        )

        # Apply the selected filter condition
        if choice == "Open=Low and Close=High":
            st.write("Open=Low and Close=High")
            results_df = stock_df[(stock_df['Open'] == stock_df['Low']) & (stock_df['Close'] == stock_df['High'])]
        elif choice == "Open=Low or Close=High":
            st.write("Open=Low or Close=High")
            results_df = stock_df[(stock_df['Open'] == stock_df['Low']) | (stock_df['Close'] == stock_df['High'])]
        elif choice == "Open=High and Close=Low":
            st.write("Open=High and Close=Low")
            results_df = stock_df[(stock_df['Open'] == stock_df['High']) & (stock_df['Close'] == stock_df['Low'])]
        elif choice == "Open=High or Close=Low":
            st.write("Open=High or Close=Low")
            results_df = stock_df[(stock_df['Open'] == stock_df['High']) | (stock_df['Close'] == stock_df['Low'])]

        # Display filtered data
        st.dataframe(results_df)

        # Plot the results using Plotly Express
        st.subheader("Filtered Data - Price Chart")
        # fig_filtered = px.line(results_df, x=results_df.index, y='Close')
        fig_filtered = px.line(results_df)
        st.plotly_chart(fig_filtered)

# Add a reset button to clear inputs
if st.button("Reset"):
    st.experimental_rerun()

#Author details
st.write("🐱‍💻 Made by Kirtan Tank")
st.write("📧 > cosmickirtan@gmail.com")
