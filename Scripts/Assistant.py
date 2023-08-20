#from neuralintents import GenericAssistant
from Neu import GenericAssistant
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader.data as pdr
import mplfinance as mpf
import yfinance as yf
import pickle
import sys
import datetime as dt
from datetime import date
from datetime import timedelta
import mplfinance as mpf
#import boto3
yf.pdr_override()
#s3_client = boto3.client('s3')

portfolio = {"AXISBANK.NS":10}


with open('portfolio.pkl','rb') as f:
    portfolio = pickle.load(f)
    
def save_portfolio():
    with open('portfolio.pkl','wb') as f:
        pickle.dump(portfolio,f)
        
    
def update_data(ticker,amount,trans_type):
    file_name = ticker+'.csv'
    path = r"C:\Users\Omkar\Desktop\Folder\Finance{}".format('\\' + file_name)
    df = pdr.get_data_yahoo(ticker).iloc[-1]
    df = df.to_frame()
    df = df.T
    df['Name'] = ticker ;
    if trans_type == 'Add' :
        
        df['Quantity'] = amount
        df['Status'] = trans_type
        df['Current_Quantity'] = int(portfolio[ticker])
        
    else:
        
        df['Quantity'] = amount
        df['Status'] = trans_type
        df['Current_Quantity'] = int(portfolio[ticker])
        
    df.to_csv(file_name)    
    #response = s3_client.upload_file(path,"python-omkar",file_name)
    
        
def add_portfolio():
    ticker = input('Which Stock to add : ')
    amount = int(input('How many to add : '))
    
    if ticker in portfolio.keys():
        portfolio[ticker] += int(amount)
    else:
        portfolio[ticker] = int(amount)
        
    save_portfolio()
    update_data(ticker,amount ,'Add')
    
    
def remove_portfolio():
    ticker = input('Which Stock to remove : ')
    amount = int(input('How many to remove : '))
    
    if ticker in portfolio.keys():
        if int(amount) <= portfolio[ticker]:
            portfolio[ticker] -= int(amount)
        else:
            print('Insufficient amount')
    else:
        print('You do not have {} stock'.format(ticker))
        
    update_data(ticker,amount,'Sub')
        

def show_portfolio():
    print('Your portfolio : ')
    for ticker in portfolio.keys():
        print('{} : {}'.format(ticker,portfolio[ticker]))
        

def portfolio_worth():
    sum = 0 
    for ticker in portfolio.keys():
        Data = yf.Ticker(ticker).info
        price = Data['currentPrice']
        sum += float(portfolio[ticker]) * price
        
    print('Total Value of portfolio : {} '.format(sum))
    

def portfolio_gains():
    starting_date = input('Enter date for comparison (YYYY-MM-DD) : ')
    
    sum_now = 0
    sum_then = 0
    
    try:
        for ticker in portfolio.keys():
            d = pdr.get_data_yahoo(ticker)
            price_now = d['Close'].iloc[-1]
            price_then = d.loc[d.index == starting_date]['Close'].values[0]
            sum_now += price_now
            sum_then += price_then
            
        print('Relative Gains : {}%'.format((sum_now-sum_then)/sum_then)*100)
        print('Actual Gains : {}%'.format(sum_now-sum_then))
    except IndexError:
        print('No Trading on this day')
    

def plot_chart():
    ticker = input('Enter ticker : ')
    starting_string = input('Choose starting date (DD-MM-YYYY) : ')
    
    plt.style.use('dark_background')
    
    start = dt.datetime.strptime(starting_string,'%d/%m/%Y')
    end = dt.datetime.now()
    
    Data = pdr.get_data_yahoo(ticker,start,end)
    
    colors = mpf.make_marketcolors(up='#00ff00',down = '#ff0000',wick = 'inherit',edge = 'inherit',volume = 'in')
    
    mpf_style = mpf.make_mpf_style(base_mpf_style = 'nightclouds',marketcolors = colors)
    
    mpf.plot(Data,type = 'candle',style = mpf_style,volume = True)
    
    
def bye():
    print('GoodBye')
    sys.exit(0)
    
    
    
def stock_price():
    ticker = input('Enter stock name : ')
    Data = yf.Ticker(ticker).info
    curr_price = Data['currentPrice']
    
    print('Current Price of {} is {} .'.format(ticker,curr_price))

mappings = { 'plot_chart' : plot_chart, 'add_portfolio' : add_portfolio, 'show_portfolio' : show_portfolio, 'bye' : bye, 'portfolio_gains' : portfolio_gains,
            'portfolio_worth' : portfolio_worth , 'stock_price' : stock_price , 'remove_portfolio' : remove_portfolio}




assistant = GenericAssistant('Intents.json',mappings,'Financial_Assistant_new')

assistant.train_model()

assistant.save_model()

while True:
    inp = input("Hello How may I help you ???")
    
    assistant.request(inp)











































