from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)