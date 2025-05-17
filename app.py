from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_cors import CORS
from src.routes.default import default_bp
from src.routes.get_stock_ticker.get_stock_ticker import get_stock_ticker_bp

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins
    
    # Register blueprints
    app.register_blueprint(default_bp)
    app.register_blueprint(get_stock_ticker_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)