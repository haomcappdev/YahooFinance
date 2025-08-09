from pathlib import Path
from datetime import datetime

import sys
import math
import yfinance as yf


def populate_stock_info(stock_code):
    stock = get_stock_object(stock_code)
    write_info(stock)


def get_stock_object(stock_code):
    stock = yf.Ticker(stock_code)
    return stock


def write_info(stock):
    print(stock.info.get("longName"))
    print(f"Stock Price: {stock.info.get("currentPrice")}")
    print(f"52 Week High: {stock.info.get("fiftyTwoWeekHigh")}")
    print(f"52 Week Low: {stock.info.get("fiftyTwoWeekLow")}")
    trailing_yield_percent = round(stock.info.get("trailingAnnualDividendYield") * 100, 2)
    print(f"Trailing Annual Dividend Yield: {trailing_yield_percent}%")
    nav = calculate_nav(stock)
    print(f"Net Asset Value: {nav}")
    max_price_by_nav = round(nav * 1.5, 2)
    print(f"Net Asset Value x1.5 (current stock price should not exceed this value): {max_price_by_nav}")
    calculate_average_eps(stock)


def calculate_nav(stock):
    balance_sheet = stock.balance_sheet
    latest_col = balance_sheet.columns[0]
    shares_outstanding = stock.info.get("sharesOutstanding")
    total_assets = balance_sheet.loc["Total Assets", latest_col]
    total_liabilities = balance_sheet.loc["Total Liabilities Net Minority Interest", latest_col]
    nav = round((total_assets - total_liabilities) / shares_outstanding, 2)
    return nav


def calculate_average_eps(stock):
    temp = 0
    eps_available_years = 0
    financials = stock.financials
    eps_data = financials.loc["Basic EPS"]
    for date, eps in eps_data[:3].items():
        if not (math.isnan(eps)):
            eps_available_years += 1
            temp += eps
    average_eps = round(temp / eps_available_years, 2)
    print(f"Average EPS ({eps_available_years} years): {average_eps}")
    max_price_by_eps = round((temp / eps_available_years) * 15, 2)
    print(f"Average EPS ({eps_available_years} years) x15 (current stock price should not exceed this value): {max_price_by_eps}")


stock_codes = []
stockCodesFile = open("stock codes.txt", "r")
for line in stockCodesFile:
    stock_codes.append(line)
stockCodesFile.close()

folder = Path("Output")
folder.mkdir(parents=True, exist_ok=True)

now = datetime.now()
filename = now.strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
file_path = folder / filename

original_stdout = sys.stdout
with file_path.open("w") as f:
    sys.stdout = f
    for code in stock_codes:
        print(code.strip())
        populate_stock_info(code.strip())
        print('\n'.strip())

# Restore original stdout
sys.stdout = original_stdout
print("Completed script.")
