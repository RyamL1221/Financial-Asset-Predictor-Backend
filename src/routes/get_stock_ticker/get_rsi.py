from flask import Blueprint, make_response, jsonify
from src.util.api_urls import POLYGON_BASE_API_URL, POLYGON_ENDPOINTS, FINNHUB_BASE_API_URL, FINNHUB_ENDPOINTS
import os, requests

def get_rsi(stock_ticker):
    stock_ticker = stock_ticker.upper()

    # Polygon API setup
    polygon_api_key = os.getenv("POLYGON_API_KEY")
    headers = {"Authorization": f"Bearer {polygon_api_key}"}
    rsi_url  = f"{POLYGON_BASE_API_URL}{POLYGON_ENDPOINTS['RSI']}/{stock_ticker}"

    # Fetch MACD data from Polygon API
    try:
        rsi_resp = requests.get(rsi_url, headers=headers, timeout=5)
        rsi_resp.raise_for_status()
        rsi_data = rsi_resp.json()

    except requests.exceptions.HTTPError as http_err:
        msg = f"Polygon API returned {http_err.response.status_code}: {http_err}"
        return make_response(jsonify({"error": msg}), http_err.response.status_code)
    except requests.exceptions.RequestException as req_err:
        msg = f"Error fetching data from Polygon API: {req_err}"
        return make_response(jsonify({"error": msg}), 502)
    except ValueError as json_err:
        msg = f"Invalid JSON response: {json_err}"
        return make_response(jsonify({"error": msg}), 502)

    # extract just the `values` lists
    rsi_values  = rsi_data.get("results", {}).get("values", [])

    return rsi_values