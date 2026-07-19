import yfinance as yf
import pandas as pd

def download_stock_data(tickers, start_date, end_date):
    
    data = yf.download(
        tickers=tickers,
        start=start_date,
        end=end_date
    )

    data.to_csv("../data/stock_prices.csv")
    
    return data