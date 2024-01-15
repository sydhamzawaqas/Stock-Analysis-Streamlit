import streamlit as st, pandas as pd, numpy as np, yfinance as yf
import plotly.express as px
from alpha_vantage.fundamentaldata import FundamentalData
from stocknews import StockNews
import plotly.graph_objects as go

st.title("Stock Analysis Dashboard")
ticker = st.sidebar.text_input("Ticker")
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")

data = yf.download(ticker,start=start_date,end=end_date)
data
fig = px.line(data,x = data.index, y = data['Adj Close'],title=ticker)

st.plotly_chart(fig)
fig_candle = go.Figure(data=[go.Candlestick(x=data.index,
                                             open=data['Open'],
                                             high=data['High'],
                                             low=data['Low'],
                                             close=data['Close'])])
fig_candle.update_layout(title=f"{ticker} - Candlestick Chart")
st.subheader("Candlestick Chart")
st.plotly_chart(fig_candle)

st.subheader("Bar Chart")
fig_bar = px.bar(data, x=data.index, y=data['Volume'], title=f"{ticker} - Volume")
st.plotly_chart(fig_bar)

st.subheader("Scatter Chart")
fig_scatter = px.scatter(data, x=data.index, y=data['Close'], title=f"{ticker} - Scatter Plot")
st.plotly_chart(fig_scatter)



pricing_data, news = st.tabs(["Pricing Data","Top 10 News"])

with pricing_data:
    st.header("Price Movements")
    data2 = data
    data2["% Change"]= data['Adj Close'] / data['Adj Close'].shift(1) -1
    data2.dropna(inplace = True)

    st.write(data2)
    annual_return = data2["% Change"].mean()*252*100 
    st.write("Annual Return is ",annual_return,"%")
    
    stdev = np.std(data2["% Change"])*np.sqrt(252)
    st.write("Standard Deviation is ",stdev*100,"%")
    st.write("Risk ADJ Return is ",annual_return/(stdev*100))
    
    
with news:
    st.write("News")
    st.header(f"News Of {ticker}")
    sn = StockNews(ticker,save_news=False)
    df_news = sn.read_rss()
    for i in range(10):
        st.subheader(f"News {i+1}")
        st.write(df_news['published'][i])
        st.write(df_news['title'][i])
        st.write(df_news['summary'][i]) 
        ts = df_news['sentiment_title'][i]
        st.write(f"Title Sentiment {ts} ")
        ns = df_news['sentiment_summary'][i]
        st.write(f"News Sentiment {ns} ")          

