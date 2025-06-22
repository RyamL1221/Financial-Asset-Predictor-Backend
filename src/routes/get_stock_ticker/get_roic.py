import yfinance as yf
import pandas as pd

# ROIC = (net income – dividends) / (debt + equity)
def get_roic(stock_ticker):
    ticker = yf.Ticker(stock_ticker)
    income_statement = ticker.income_stmt
    balance_sheet = ticker.balance_sheet
    dividends = ticker.dividends

    # Fetch dividends for current year
    current_year = pd.Timestamp.now().year
    total_dividends_this_year = dividends[dividends.index.year == current_year].sum()

    # grab the name of the most-recent year (fiscal year)
    latest_net_income_date = income_statement.columns[0]

    # fetch net income for latest year
    net_income = income_statement.loc['Net Income', latest_net_income_date]


    latest_balance_sheet_date = balance_sheet.columns[0]
    liabilities = balance_sheet.loc['Total Liabilities Net Minority Interest', latest_balance_sheet_date]
    equity = balance_sheet.loc['Total Equity Gross Minority Interest', latest_balance_sheet_date]

    # Calculate ROIC
    roic = (net_income - total_dividends_this_year) / (liabilities + equity)
    return roic

if __name__ == "__main__":
    stock_ticker = "AAPL"
    get_roic(stock_ticker)