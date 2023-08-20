import pandas_datareader.data as pdr
import yfinance as yf
from datetime import date
yf.pdr_override()

def MACD(text):
    
    end=date.today()
    #start = end - timedelta(1)
    
    df = pdr.get_data_yahoo(text , start='2023-01-01' , end = end)
    
    df['EMA_short'] = df['Close'].ewm(span=12, min_periods=1, adjust=False).mean()
    
    df['EMA_long'] = df['Close'].ewm(span=26, min_periods=1, adjust=False).mean()
    
    df['MACD'] = df['EMA_short'] - df['EMA_long']
    
    df['Signal_line'] = df['MACD'].ewm(span=9, min_periods=1, adjust=False).mean()
    
    
    
    return df.index , df['MACD'] , df['Signal_line']
    


