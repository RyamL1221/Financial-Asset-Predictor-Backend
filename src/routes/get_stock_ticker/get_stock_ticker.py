from flask import Blueprint, jsonify, Response
from src.routes.get_stock_ticker.getters import (
    get_macd, get_rsi, get_profile, get_bollinger_bands, 
    get_roic, get_eps, get_beta, get_ey
)
from src.routes.get_stock_ticker.analysis import perform_stock_analysis

get_stock_ticker_bp = Blueprint("get_stock_ticker", __name__)

@get_stock_ticker_bp.route('/get-stock-ticker/<string:stock_ticker>', methods=['GET'])
def get_stock_ticker(stock_ticker):
    """
    Get comprehensive stock data and analysis for a given ticker symbol.
    
    Args:
        stock_ticker (str): The stock ticker symbol (e.g., 'AAPL', 'MSFT')
    
    Returns:
        JSON response containing:
        - profile: Company profile information
        - macd: MACD technical indicator data
        - rsi: RSI technical indicator data
        - bollinger_bands: Bollinger Bands data
        - roic: Return on Invested Capital data
        - eps: Earnings Per Share data
        - beta: Beta coefficient data
        - ey: Earnings Yield data
        - analysis: Technical analysis and recommendations
    """
    try:
        stock_ticker = stock_ticker.upper()
        
        # Get all stock data
        profile = get_profile(stock_ticker)
        macd = get_macd(stock_ticker)
        rsi = get_rsi(stock_ticker)
        bollinger_bands = get_bollinger_bands(stock_ticker)
        roic = get_roic(stock_ticker)
        eps = get_eps(stock_ticker)
        beta = get_beta(stock_ticker)
        
        # Get earnings yield (requires EPS data)
        ey = get_ey(stock_ticker, eps) if eps else None
        if isinstance(ey, Response):
            return ey
        
        # Perform technical analysis
        analysis = perform_stock_analysis(
            macd_values=macd,
            rsi_values=rsi,
            bollinger_band_values=bollinger_bands,
            eps=eps
        )
        
        # Prepare response
        response = {
            "profile": profile,
            "macd": macd,
            "rsi": rsi,
            "bollinger_bands": bollinger_bands,
            "roic": roic,
            "eps": eps,
            "beta": beta,
            "ey": ey,
            "analysis": analysis
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(e)
        msg = "Error fetching stock data"
        return jsonify({"error": msg}), 500
