from datetime import datetime, timedelta
import yfinance as yf
import math
import pandas as pd
import numpy as np
from scipy.stats import norm
import requests
import io
import time
import openpyxl
from tqdm import tqdm
from binomialTreePricing import binomialTreeOptionValue
from blackScholesModel import blackScholesModel
from monteCarloPricing import monteCarloPricing

def findClosestDate(tickerDates, time):
    if tickerDates:
        today = datetime.now()
        target_date = today + timedelta(days=time)

        closest_date = min(
            tickerDates, 
            key=lambda d: abs(datetime.strptime(d, "%Y-%m-%d") - target_date)
        )
        date1 = datetime.strptime(closest_date, "%Y-%m-%d")
        date=datetime.now().date()
        days=(date1.date()-date).days
        # 5. Fetch the option chain for that closest date
        opt_chain = ticker.option_chain(closest_date)
        
        calls = opt_chain.calls
        puts = opt_chain.puts
        return calls, days, date1.date()
    else:
        return pd.DataFrame(), None, None

def getVolatility(hist):
    closing_prices = hist['Close']
    returns_abc = closing_prices.pct_change().dropna()
    daily_volatility = returns_abc.std()
    annualized_volatility = daily_volatility * np.sqrt(252)
    return annualized_volatility


def getRiskFreeIntrestRate():
    irx = yf.Ticker("^IRX")
    hist = irx.history(period="5d")
    latest_yield_pct = hist['Close'].iloc[-1]
    return latest_yield_pct / 100.0

#Start 
start_time = time.perf_counter()
print(r"""
    $$$$$$$\  $$\                           
    $$  __$$\ $$ |                          
    $$ |  $$ |$$$$$$$\  $$\   $$\  $$$$$$$\ 
    $$$$$$$  |$$  __$$\ $$ |  $$ |$$  _____|
    $$  __$$< $$ |  $$ |$$ |  $$ |\$$$$$$\  
    $$ |  $$ |$$ |  $$ |$$ |  $$ | \____$$\ 
    $$ |  $$ |$$ |  $$ |\$$$$$$$ |$$$$$$$  |
    \__|  \__|\__|  \__| \____$$ |\_______/ 
                        $$\   $$ |          
                        \$$$$$$  |          
                        \______/           
      """)

dateList=input("What days to expiration do you want:")
print("Starting Pricing Algorithm...")
annual_rate = getRiskFreeIntrestRate()
dates=dateList.split()
dates1=[int(x) for x in dates]
url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)
tickers = pd.read_html(io.StringIO(response.text))[0]
tickers=tickers['Symbol'].tolist()
# Clean ticker symbols for yfinance (e.g., BRK.B -> BRK-B)
tickers = [t.replace('.', '-') for t in tickers]
tickers1=yf.Tickers(tickers)
list=pd.DataFrame()
i=0
for symbol, ticker in tqdm(tickers1.tickers.items(), desc="Analyzing"):
    #print(f"{round(i/500*100,1)}% Complete")
    i+=1
    #ticker = yf.Ticker(i)
    currentPrice= ticker.fast_info["last_price"]
    # 2. Get all available expiration dates (returned as strings 'YYYY-MM-DD')
    available_dates = ticker.options
    if(available_dates==None):
        continue
    hist = ticker.history(period="1mo") 
    annualized_volatility=getVolatility(hist)
    for date in dates1:
        dayCalls, dayDays, dayExpire=findClosestDate(available_dates,date)
        if (dayCalls.empty==True):
            continue
        for row in dayCalls.itertuples(index=True):
            price=blackScholesModel(currentPrice, row.strike,annualized_volatility, annual_rate, dayDays)
            currentAsk=row.ask
            if (price>currentAsk+.01 and currentAsk>0):
                treePrice=binomialTreeOptionValue(currentPrice, row.strike, annualized_volatility, annual_rate, dayDays, 10)
                if (treePrice>currentAsk+.01):
                    carloPrice=monteCarloPricing(currentPrice, row.strike, annualized_volatility, annual_rate, dayDays)
                    if (carloPrice>currentAsk+.01 and currentAsk>0):
                        treePrice=round(treePrice,2)
                        price=round(price, 2)
                        percentIncrease = round(((treePrice - currentAsk) / currentAsk), 2)
                        newrow=pd.DataFrame({"Ticker": [ticker.ticker], "Expires": [dayExpire], "Current Price": [currentPrice], "Strike Price": [row.strike], "Calculated Option Price": [price], "BinomialTree Price": [treePrice], "Monte Carlo Price":[round(carloPrice,2)],  "Asking Amount": [currentAsk], "Difference": [percentIncrease]})
                        list=pd.concat([list, newrow], ignore_index=True)
list.sort_values(by="Difference", inplace=True, ascending=False)
list.to_excel("UndervaluedOptions.xlsx", index=False)
end_time = time.perf_counter()
print(f"Finished in {round(end_time-start_time,2)} seconds")
print("Remember to set the difference column to percent in excel to see the actual value.")