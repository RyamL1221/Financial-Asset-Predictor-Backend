from flask import make_response, jsonify
from src.util.api_urls import POLYGON_BASE_API_URL, POLYGON_ENDPOINTS, FINNHUB_BASE_API_URL, FINNHUB_ENDPOINTS
import os, requests

def get_macd(stock_ticker):

    # Polygon API setup
    polygon_api_key = os.getenv("POLYGON_API_KEY")
    headers = {"Authorization": f"Bearer {polygon_api_key}"}
    macd_url = f"{POLYGON_BASE_API_URL}{POLYGON_ENDPOINTS['MACD']}/{stock_ticker}"

    # Fetch MACD data from Polygon API
    try:
        macd_resp = requests.get(macd_url, headers=headers, timeout=5)
        macd_resp.raise_for_status()
        macd_data = macd_resp.json()

    except Exception:
        msg = "Error fetching MACD data"
        return make_response(jsonify({"error": msg}), 500)

    # extract just the `values` lists
    macd_values = macd_data.get("results", {}).get("values", [])

    # Above 80 is overbought, below 30 is oversold for RSI
    # Unix Msec Time for timestamp
    return macd_values