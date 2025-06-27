from flask import make_response, jsonify
from src.util.api_urls import POLYGON_BASE_API_URL, POLYGON_ENDPOINTS, FINNHUB_BASE_API_URL, FINNHUB_ENDPOINTS
import os, requests

def get_rsi(stock_ticker):

    # Polygon API setup
    polygon_api_key = os.getenv("POLYGON_API_KEY")
    headers = {"Authorization": f"Bearer {polygon_api_key}"}
    rsi_url  = f"{POLYGON_BASE_API_URL}{POLYGON_ENDPOINTS['RSI']}/{stock_ticker}"

    # Fetch MACD data from Polygon API
    try:
        rsi_resp = requests.get(rsi_url, headers=headers, timeout=5)
        rsi_resp.raise_for_status()
        rsi_data = rsi_resp.json()
    except Exception:
        msg = "Error fetching RSI data"
        return make_response(jsonify({"error": msg}), 500)

    # extract just the `values` lists
    rsi_values  = rsi_data.get("results", {}).get("values", [])

    return rsi_values