from flask import Blueprint, jsonify
from src.routes.get_stock_ticker.get_macd import get_macd
from src.routes.get_stock_ticker.get_rsi import get_rsi
from src.routes.get_stock_ticker.get_profile import get_profile
from src.routes.get_stock_ticker.get_bollinger_bands import get_bollinger_bands
from src.routes.get_stock_ticker.get_roic import get_roic
from src.routes.get_stock_ticker.get_eps import get_eps
from src.routes.get_stock_ticker.get_beta import get_beta
from src.routes.get_stock_ticker.get_ey import get_ey

get_stock_ticker_bp = Blueprint("get_stock_ticker", __name__)

@get_stock_ticker_bp.route('/get-stock-ticker/<string:stock_ticker>', methods=['GET'])
def get_stock_ticker(stock_ticker):
    stock_ticker = stock_ticker.upper()

    macd_values = get_macd(stock_ticker)
    rsi_values = get_rsi(stock_ticker)
    bollinger_band_values = get_bollinger_bands(stock_ticker)
    profile = get_profile(stock_ticker)
    roic = get_roic(stock_ticker)
    eps = get_eps(stock_ticker)
    beta = get_beta(stock_ticker)
    ey = get_ey(stock_ticker, eps)
   
    return jsonify({
        "eps":              eps,
        "ticker":           stock_ticker,
        "macd":             macd_values,
        "rsi":              rsi_values,
        "roic":             roic,
        "bollinger_bands":  bollinger_band_values,
        "beta":             beta,
        "ey":               ey,
        "country":          profile.get("country"),
        "name":             profile.get("name"),
        "shareOutstanding": profile.get("shareOutstanding"),
        "weburl":           profile.get("weburl"),
    }), 200
