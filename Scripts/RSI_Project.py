
import pandas as pd
import pandas_datareader.data as pdr
import yfinance as yf
from datetime import date


yf.pdr_override()


def RSI(text):
    End = date.today()
    
    
    df = pdr.get_data_yahoo(text,start = '2023-01-01' , end=End)
    
    delta = df['Adj Close'].diff(1)
    
    delta.dropna(inplace=True)

    positive = delta.copy()
    
    negative = delta.copy()

    positive[positive < 0] = 0
    
    negative[negative > 0] = 0

    days = 14

    avg_gain = positive.rolling(window = days).mean()
    
    avg_loss = abs(negative.rolling(window = days).mean())

    relative_strength = avg_gain / avg_loss

    RSI = 100.0 - (100.0 / (1 + relative_strength))
    
    combined_df = pd.DataFrame()
    
    combined_df['RSI'] = RSI

    return combined_df.index , combined_df['RSI'].values




































































