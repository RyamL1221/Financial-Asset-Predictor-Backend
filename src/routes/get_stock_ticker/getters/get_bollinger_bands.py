from flask import make_response, jsonify
from src.util.api_urls import TWELVE_DATA_BASE_API_URL, TWELVE_DATA_ENDPOINTS
import os, requests

def get_bollinger_bands(stock_ticker):

    # Twelve Data API setup
    twelve_data_api_key = os.getenv("TWELVE_DATA_API_KEY")
    interval = "1day"
    adjust = "all"
    api_url = TWELVE_DATA_BASE_API_URL + TWELVE_DATA_ENDPOINTS["BOLLINGER_BANDS"] + "?" + "symbol=" + stock_ticker + "&interval=" + interval + "&adjust=" + adjust
    headers = {"Authorization": f"apikey {twelve_data_api_key}"}

    # Fetch Bollinger Bands data from Twelve Data API
    try:
        resp = requests.get(api_url, headers=headers, timeout=5)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        msg = "Error fetching Bollinger Bands data"
        return make_response(jsonify({"error": msg}), 500)

    # extract just the `values` lists
    bollinger_bands_values = data.get("values", [])   

    return bollinger_bands_values