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

def binomialTreeOptionValue(S, K, sigma, r, days, n):
    # Convert days to annualized fraction of a year
    t = days / 365.0
    
    if t <= 0:
        return max(0.0, S - K)
        
    h = t / n
    u = np.exp(sigma * np.sqrt(h))
    d = 1 / u
    
    # Avoid zero division or out-of-bounds probability if u == d
    denom = u - d
    if denom == 0:
        return max(0.0, S - K)
        
    p_rn = (np.exp(r * h) - d) / denom
    discountFactor = np.exp(-r * h)
    
    # Initialize terminal payoff array
    V = np.zeros((n + 1, n + 1))
    for i in range(n + 1):
        V[i, n] = max(S * (u**i) * (d**(n - i)) - K, 0.0)
        
    # Backward induction (American Option early exercise allowed)
    for j in range(n - 1, -1, -1):
        for i in range(j + 1):
            continuationValue = discountFactor * (p_rn * V[i + 1, j + 1] + (1 - p_rn) * V[i, j + 1])
            eev = max(S * (u**i) * (d**(j - i)) - K, 0.0)
            V[i, j] = max(eev, continuationValue)
            
    return V[0, 0]