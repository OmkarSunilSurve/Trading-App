import pandas as pd
import pandas_datareader.data as pdr
import yfinance as yf
from datetime import date
yf.pdr_override()
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
from pypfopt import HRPOpt


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

