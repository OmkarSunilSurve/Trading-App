import pandas_datareader.data as pdr
import yfinance as yf
from datetime import date
yf.pdr_override()


def EMA(text):
    
    df = pdr.get_data_yahoo(text,start='2023-01-01',end=date.today())
    
    df['EMA_12'] = df['Close'].ewm(span=12,adjust=False).mean()
    
    df['EMA_24'] = df['Close'].ewm(span=24,adjust=False).mean()
    
    df['EMA_55'] = df['Close'].ewm(span=55,adjust=False).mean()
    
    return df.index,df['EMA_12'],df['EMA_24'],df['EMA_55']










