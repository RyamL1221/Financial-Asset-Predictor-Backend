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

    # Fetch profile data from Finnhub API
    try:
        profile_resp = requests.get(
            finnhub_url,
            headers=finnhub_headers
        )
        profile_resp.raise_for_status()
        profile = profile_resp.json()
    except Exception:
        msg = f"Error fetching profile data"
        return make_response(jsonify({"error": msg}), 500)

    return profile