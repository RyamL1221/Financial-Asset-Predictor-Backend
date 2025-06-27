from flask import make_response, jsonify
from src.util.api_urls import POLYGON_BASE_API_URL, POLYGON_ENDPOINTS, FINNHUB_BASE_API_URL, FINNHUB_ENDPOINTS
import os, requests

def get_profile(stock_ticker):

     # Finhubb API setup
    finnhub_api_key = os.getenv("FINNHUB_API_KEY")
    finnhub_url = (
        f"{FINNHUB_BASE_API_URL}{FINNHUB_ENDPOINTS['COMPANY_PROFILE2']}"
        f"?symbol={stock_ticker}"
    )
    finnhub_headers = {"X-Finnhub-Token": finnhub_api_key}

    # Fetch MACD data from Polygon API
    try:
        profile_resp = requests.get(
            finnhub_url,
            headers=finnhub_headers
        )
        profile_resp.raise_for_status()
        profile = profile_resp.json()
    except requests.exceptions.HTTPError as http_err:
        msg = f"Finnhub API returned {http_err.response.status_code}: {http_err}"
        return make_response(jsonify({"error": msg}), http_err.response.status_code)
    except requests.exceptions.RequestException as req_err:
        msg = f"Error fetching data from Finnhub API: {req_err}"
        return make_response(jsonify({"error": msg}), 502)
    except ValueError as json_err:
        msg = f"Invalid JSON response: {json_err}"
        return make_response(jsonify({"error": msg}), 502)

    return profile