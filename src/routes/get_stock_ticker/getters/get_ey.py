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

    except requests.exceptions.HTTPError as http_err:
        msg = f"Twelve Data API returned {http_err.response.status_code}: {http_err}"
        return make_response(jsonify({"error": msg}), http_err.response.status_code)
    except requests.exceptions.RequestException as req_err:
        msg = f"Error fetching data from Twelve Data API: {req_err}"
        return make_response(jsonify({"error": msg}), 502)
    except ValueError as json_err:
        msg = f"Invalid JSON response: {json_err}"
        return make_response(jsonify({"error": msg}), 502)

    price = data.get('price', 0)
    price = float(price)
    current_eps = eps.get('current', None).get('0y', 0)
    if price == 0 or current_eps == 0:
        return make_response(jsonify({"error": "Price or EPS data is not available"}), 502)
    ey = current_eps / price
    return ey