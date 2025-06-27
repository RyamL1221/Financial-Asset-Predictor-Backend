from flask import make_response, jsonify
from src.util.api_urls import TWELVE_DATA_BASE_API_URL, TWELVE_DATA_ENDPOINTS
import os, requests

def get_beta(stock_ticker):

    # Twelve Data API setup
    twelve_data_api_key = os.getenv("TWELVE_DATA_API_KEY")
    interval = "1month"
    api_url = TWELVE_DATA_BASE_API_URL + TWELVE_DATA_ENDPOINTS["BETA"] + "?" + "symbol=" + stock_ticker + "&interval=" + interval
    headers = {"Authorization": f"apikey {twelve_data_api_key}"}

    # Fetch Beta data from Twelve Data API
    try:
        resp = requests.get(api_url, headers=headers, timeout=5)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        msg = "Error fetching Beta data"
        return make_response(jsonify({"error": msg}), 500)

    # extract just the `values` lists
    beta = data.get("values", [])   

    return beta