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

def monteCarloPricing(currentPrice, strikePrice, volatility, annual_rate, days, num_simulations=10000):
    z = np.random.standard_normal(num_simulations)
    T=days/365
    
    # Calculate terminal stock prices using Geometric Brownian Motion
    ST = currentPrice * np.exp((annual_rate - 0.5 * volatility**2) * T + volatility * np.sqrt(T) * z)
    
    # Calculate payoff for a European Call option
    payoffs = np.maximum(ST - strikePrice, 0)
    
    # Discount the average payoff back to present value
    option_price = np.exp(-annual_rate * T) * np.mean(payoffs)
    
    return option_price
    