import yfinance as yf

# ROIC = (net income – dividends) / (debt + equity)
def get_roic(stock_ticker):
    ticker = yf.Ticker(stock_ticker)
    income_statement = ticker.income_stmt
    balance_sheet = ticker.balance_sheet
    dividends = ticker.dividends
    print(income_statement)
    print(dividends)