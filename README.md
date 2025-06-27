# Financial Asset Predictor Backend

## Make sure to have Python and Git Installed

## Cloning the Repository:

`git clone https://github.com/RyamL1221/The-Game-Counter-Backend`

## Setting up Virtual Environment

1. Go to your project's root directory, then: `python -m venv venv` 
2. Prepare the virtual environment: `venv\Scripts\activate.bat`
3. Activate the virtual environment: `venv\Scripts\Activate.ps1`
4. Use pip like usual: `pip install -r requirements.txt`

## Running the App

### Before you run the app, make sure to set up your .env file.

1. Run the app `python -m flask run`
2. Run all unit tests: `pytest`
3. Run a specific unit test: `pytest tests/[file name (including .py)]`

## Running Database Scripts

1. Run this command ONE TIME only: `$env:PYTHONPATH = "."`
2. To run scripts:`python -m src.scripts.[filename minus .py]`

## API Endpoints

### Stock Ticker Endpoint (Enhanced with Analysis)

**GET** `/get-stock-ticker/<stock_ticker>`

Returns comprehensive stock data including technical indicators, company profile, and advanced analysis.

**Parameters:**
- `stock_ticker` (string): The stock ticker symbol (e.g., AAPL, MSFT, GOOGL)

**Response:**
```json
{
  "ticker": "AAPL",
  "name": "Apple Inc.",
  "company_name": "Apple Inc.",
  "country": "US",
  "shareOutstanding": 1000000000,
  "share_outstanding": 1000000000,
  "weburl": "https://www.apple.com",
  "roic": 0.15,
  "ey": 0.04,
  "eps": {
    "current": {
      "0y": 5.0,
      "+1y": 5.5
    }
  },
  "eps_analysis": {
    "current": 5.0,
    "growth_percentage": 10.0
  },
  "macd": [...],
  "rsi": [...],
  "bollinger_bands": [...],
  "beta": [...],
  "macd_signals": [
    {
      "date": "2024-01-15",
      "type": "BUY",
      "description": "A recommendation to purchase a specific security...",
      "confidence": 85,
      "reasoning": ["MACD line crossed above signal line", "Strong positive histogram momentum"],
      "technical_factors": ["Strong MACD momentum", "Bullish histogram pattern"]
    }
  ],
  "current_recommendation": {
    "date": "2024-01-15",
    "type": "BUY",
    "description": "A recommendation to purchase a specific security...",
    "confidence": 85,
    "reasoning": ["MACD line significantly above signal line", "Strong positive histogram momentum"],
    "technical_factors": ["Strong MACD bullish crossover"]
  },
  "technical_analysis": {
    "macd_recommendation": "BUY",
    "macd_analysis": "MACD line at 0.5000 is significantly above signal line...",
    "rsi_recommendation": "HOLD",
    "rsi_analysis": "RSI at 45.00 is in neutral territory (40-60)...",
    "bollinger_recommendation": "HOLD",
    "bollinger_analysis": "Bollinger Bands show normal volatility..."
  },
  "recommendation_scale": [
    {
      "type": "BUY",
      "name": "Buy",
      "alias": "Strong Buy / On the Recommended List",
      "description": "A recommendation to purchase a specific security...",
      "expected_return": "15%+ above market",
      "risk_level": "Low to Medium",
      "time_horizon": "3-12 months",
      "color": "#22543d",
      "background_color": "#c6f6d5"
    }
  ]
}
```

**Error Responses:**
- `400 Bad Request`: Insufficient data for analysis
- `500 Internal Server Error`: Server error during analysis

## Adding new feature

1. Create a new branch and switch to it `git checkout -b feature/{new_feature_name}
2. Develop the feature, and add it to codebase with `git add *`, `git commit -m "{message}"`, and `git push`
3. After finishing the feature, create a pull request to merge with the **dev** branch
