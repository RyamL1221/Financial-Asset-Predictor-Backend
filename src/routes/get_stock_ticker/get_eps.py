import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import yfinance as yf

def get_eps(stock_ticker):
    ticker = yf.Ticker(stock_ticker)
    eps = ticker.eps_trend
    eps = eps.to_dict()
    return eps