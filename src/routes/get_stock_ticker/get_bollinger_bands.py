from flask import make_response, jsonify
from src.util.api_urls import TWELVE_DATA_BASE_API_URL, TWELVE_DATA_ENDPOINTS
import os, requests

def get_bollinger_bands(stock_ticker):
    stock_ticker = stock_ticker.upper()

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

    except requests.exceptions.HTTPError as http_err:
        msg = f"Twelve Data API returned {http_err.response.status_code}: {http_err}"
        return make_response(jsonify({"error": msg}), http_err.response.status_code)
    except requests.exceptions.RequestException as req_err:
        msg = f"Error fetching data from Twelve Data API: {req_err}"
        return make_response(jsonify({"error": msg}), 502)
    except ValueError as json_err:
        msg = f"Invalid JSON response: {json_err}"
        return make_response(jsonify({"error": msg}), 502)

    # extract just the `values` lists
    bollinger_bands_values = data.get("values", [])   

    # Above 80 is overbought, below 30 is oversold for RSI
    # Unix Msec Time for timestamp
    return bollinger_bands_values