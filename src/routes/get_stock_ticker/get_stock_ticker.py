from flask import Blueprint, make_response, jsonify
from src.util.polygon import (
    BASE_API_URL,
    ENDPOINTS,
)
import os
import requests

get_stock_ticker_bp = Blueprint("get_stock_ticker", __name__)

@get_stock_ticker_bp.route('/get-stock-ticker/<string:stock_ticker>', methods=['GET'])
def get_stock_ticker(stock_ticker):
    stock_ticker = stock_ticker.upper()
    url = BASE_API_URL + ENDPOINTS["GET_TICKER"]
    API_KEY = os.getenv("POLYGON_API_KEY")
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    params = {
        "ticker": stock_ticker
    }
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=5)
        resp.raise_for_status()  # HTTPError on bad status
        data = resp.json()
    except requests.exceptions.HTTPError as http_err:
        msg = f"Polygon API returned {resp.status_code}: {http_err}"
        print(msg)
        return make_response(jsonify({"error": msg}), resp.status_code)
    except requests.exceptions.RequestException as req_err:
        msg = f"Error fetching data from Polygon API: {req_err}"
        print(msg)
        return make_response(jsonify({"error": msg}), 502)
    except ValueError as json_err:
        msg = f"Invalid JSON response: {json_err}"
        print(msg)
        return make_response(jsonify({"error": msg}), 502)

    return jsonify(data)
