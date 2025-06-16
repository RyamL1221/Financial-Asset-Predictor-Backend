from flask import Blueprint, jsonify
from src.routes.get_stock_ticker.get_macd import get_macd
from src.routes.get_stock_ticker.get_rsi import get_rsi
from src.routes.get_stock_ticker.get_profile import get_profile

get_stock_ticker_bp = Blueprint("get_stock_ticker", __name__)

@get_stock_ticker_bp.route('/get-stock-ticker/<string:stock_ticker>', methods=['GET'])
def get_stock_ticker(stock_ticker):
    stock_ticker = stock_ticker.upper()

    macd_values = get_macd(stock_ticker)
    rsi_values = get_rsi(stock_ticker)
    profile = get_profile(stock_ticker)
   
    return jsonify({
        "ticker":           stock_ticker,
        "macd":             macd_values,
        "rsi":              rsi_values,
        "country":          profile.get("country"),
        "name":             profile.get("name"),
        "shareOutstanding": profile.get("shareOutstanding"),
        "weburl":           profile.get("weburl"),
    }), 200
