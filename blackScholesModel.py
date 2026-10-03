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

def blackScholesModel(currentPrice, strikePrice, volatility, annual_rate, days):
    # 1. Convert days to years (annualized time term)
    t = days / 365.0
    
    if t <= 0:
        return max(0.0, currentPrice - strikePrice)
    
    denom = volatility * math.sqrt(t)
    if denom == 0:
        return max(0.0, currentPrice - strikePrice)
        
    # 2. Use the raw annualized rate
    d1 = (math.log(currentPrice / strikePrice) + (annual_rate + (volatility ** 2) / 2.0) * t) / denom
    d2 = d1 - denom
    
    price = currentPrice * norm.cdf(d1) - strikePrice * math.exp(-annual_rate * t) * norm.cdf(d2)
    return price
