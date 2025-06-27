from flask import make_response, jsonify
from src.util.api_urls import TWELVE_DATA_BASE_API_URL, TWELVE_DATA_ENDPOINTS
import os, requests

def get_ey(stock_ticker, eps):

    # Twelve Data API setup
    twelve_data_api_key = os.getenv("TWELVE_DATA_API_KEY")
    api_url = TWELVE_DATA_BASE_API_URL + TWELVE_DATA_ENDPOINTS["PRICE"] + "?" + "symbol=" + stock_ticker 
    headers = {"Authorization": f"apikey {twelve_data_api_key}"}

    # Fetch Price data from Twelve Data API
    try:
        resp = requests.get(api_url, headers=headers, timeout=5)
        resp.raise_for_status()
        data = resp.json()

    except Exception:
        msg = "Error fetching Earnings Yield data"
        return make_response(jsonify({"error": msg}), 500)

    price = data.get('price', 0)
    price = float(price)
    current_eps = eps.get('current', None).get('0y', 0)
    if price == 0 or current_eps == 0:
        return make_response(jsonify({"error": "Price or EPS data is not available"}), 502)
    ey = current_eps / price
    return ey