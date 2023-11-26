import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf
st.title('Finacial Dashboard')

tickers = ('TSLA', 'AAPL', 'MSFT', 'BTS-USD', 'ETH-USD')
dropdown = st.multiselect('Pick your asset',
                         tickers)
start = st.date_input('Start', value = pd.to_datetime('2021-01-01'))
end = st.date_input('End', value =pd.to_datetime('today'))
df = yf.download(tickers,start, end)
def relative_return(df):
    relative = df.pct_change()
    cumulative_return =(1+relative).cumprod() -1
    cumulative_return = cumulative_return.fillna(0)
    return cumulative_return

if len(dropdown) >0:
    df = relative_return(yf.download(dropdown, start, end)['Adj Close'])
    st.line_chart(df)

price_data,news =st.tabs(['Pricing Data', "News"])


with price_data:
    st.header('Price Movements')
    st.write(df)


from stocknews import StockNews
with news:
    st.header(f'News of {tickers}')
    stock_news = StockNews(tickers, save_news= False)
    data_news = stock_news.read_rss()
    for i in range(10):
        st.subheader(f"News {i+1}")
        st.write(data_news['published'][i])
        st.write(data_news['title'][i])
        st.write(data_news['summary'][i])
        title_sentiment = data_news['sentiment_title'][i]
        st.write(f'Title Sentiment {title_sentiment}')
