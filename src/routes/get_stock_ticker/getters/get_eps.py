from flask import make_response, jsonify
import yfinance as yf

def get_eps(stock_ticker):
    try:
        ticker = yf.Ticker(stock_ticker)
        eps = ticker.eps_trend
        eps = eps.to_dict()
        return eps
    except Exception:
        msg = "Error fetching EPS data"
        return make_response(jsonify({"error": msg}), 500)