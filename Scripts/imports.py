import pandas_datareader.data as pdr
import yfinance as yf
import pandas as pd
from datetime import date
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
from pypfopt import HRPOpt
yf.pdr_override()


def EMA(text):
    
    df = pdr.get_data_yahoo(text,start='2023-01-01',end=date.today())
    
    df['EMA_12'] = df['Close'].ewm(span=12,adjust=False).mean()
    
    df['EMA_24'] = df['Close'].ewm(span=24,adjust=False).mean()
    
    df['EMA_55'] = df['Close'].ewm(span=55,adjust=False).mean()
    
    return df.index,df['EMA_12'],df['EMA_24'],df['EMA_55']


def MACD(text):
    
    end=date.today()
    
    df = pdr.get_data_yahoo(text , start='2023-01-01' , end = end)
    
    df['EMA_short'] = df['Close'].ewm(span=12, min_periods=1, adjust=False).mean()
    
    df['EMA_long'] = df['Close'].ewm(span=26, min_periods=1, adjust=False).mean()
    
    df['MACD'] = df['EMA_short'] - df['EMA_long']
    
    df['Signal_line'] = df['MACD'].ewm(span=9, min_periods=1, adjust=False).mean()
    
    
    
    return df.index , df['MACD'] , df['Signal_line']
    



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



def Optimize(Stocks : list , Amount):
    df = pd.DataFrame()
    for stock in Stocks:
        data = pdr.get_data_yahoo(stock,start='2023-01-01',end=date.today())
        df[stock] = data['Close']
    latest_prices = get_latest_prices(df)


    returns = df.pct_change().dropna()
    hrp = HRPOpt(returns)
    hrp_weights = hrp.optimize()

    da_hrp = DiscreteAllocation(hrp_weights, latest_prices, total_portfolio_value=Amount)
    
    return da_hrp.greedy_portfolio(),latest_prices































































































































