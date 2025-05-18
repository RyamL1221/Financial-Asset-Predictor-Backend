from flask import Blueprint, make_response, jsonify
from src.util.api_urls import POLYGON_BASE_API_URL, POLYGON_ENDPOINTS, FINNHUB_BASE_API_URL, FINNHUB_ENDPOINTS
import os, requests

get_stock_ticker_bp = Blueprint("get_stock_ticker", __name__)

@get_stock_ticker_bp.route('/get-stock-ticker/<string:stock_ticker>', methods=['GET'])
def get_stock_ticker(stock_ticker):
    stock_ticker = stock_ticker.upper()

    # Polygon API setup
    polygon_api_key = os.getenv("POLYGON_API_KEY")
    headers = {"Authorization": f"Bearer {polygon_api_key}"}
    macd_url = f"{POLYGON_BASE_API_URL}{POLYGON_ENDPOINTS['MACD']}/{stock_ticker}"
    rsi_url  = f"{POLYGON_BASE_API_URL}{POLYGON_ENDPOINTS['RSI']}/{stock_ticker}"

    # Finhubb API setup
    finnhub_api_key = os.getenv("FINNHUB_API_KEY")
    finnhub_url = (
        f"{FINNHUB_BASE_API_URL}{FINNHUB_ENDPOINTS['COMPANY_PROFILE2']}"
        f"?symbol={stock_ticker}"
    )
    finnhub_headers = {"X-Finnhub-Token": finnhub_api_key}

    try:
        macd_resp = requests.get(macd_url, headers=headers, timeout=5)
        macd_resp.raise_for_status()
        macd_data = macd_resp.json()

        rsi_resp = requests.get(rsi_url, headers=headers, timeout=5)
        rsi_resp.raise_for_status()
        rsi_data = rsi_resp.json()

        
        profile_resp = requests.get(
            finnhub_url,
            headers=finnhub_headers
        )
        profile_resp.raise_for_status()
        profile = profile_resp.json()

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
    macd_values = macd_data.get("results", {}).get("values", [])
    rsi_values  = rsi_data.get("results", {}).get("values", [])
    
    # Above 80 is overbought, below 30 is oversold for RSI
    # Unix Msec Time for timestamp
    return jsonify({
        "ticker":           stock_ticker,
        "macd":             macd_values,
        "rsi":              rsi_values,
        "country":          profile.get("country"),
        "name":             profile.get("name"),
        "shareOutstanding": profile.get("shareOutstanding"),
        "weburl":           profile.get("weburl"),
    }), 200
