import requests
import pandas as pd

# API Key for financial API
API_KEY = "your_api_key_here"
BASE_URL = "https://www.alphavantage.co/query"

# Portfolio
portfolio = {}

# Function to fetch stock data
def get_stock_data(symbol):
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "5min",
        "apikey": API_KEY,
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        try:
            latest_time = list(data["Time Series (5min)"].keys())[0]
            price = float(data["Time Series (5min)"][latest_time]["1. open"])
            return {"symbol": symbol, "price": price}
        except KeyError:
            print("Error: Invalid symbol or data unavailable.")
    return None

# Add a stock
def add_stock(symbol):
    stock_data = get_stock_data(symbol)
    if stock_data:
        portfolio[symbol] = stock_data["price"]
        print(f"Added {symbol} to portfolio at ${stock_data['price']}.")

# Remove a stock
def remove_stock(symbol):
    if symbol in portfolio:
        del portfolio[symbol]
        print(f"Removed {symbol} from portfolio.")
    else:
        print(f"{symbol} is not in your portfolio.")

# View portfolio
def view_portfolio():
    if portfolio:
        df = pd.DataFrame.from_dict(portfolio, orient="index", columns=["Price"])
        print(df)
    else:
        print("Your portfolio is empty.")

# Main Menu
def main():
    while True:
        print("\n--- Stock Portfolio Tracker ---")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. View Portfolio")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            symbol = input("Enter stock symbol: ").upper()
            add_stock(symbol)
        elif choice == "2":
            symbol = input("Enter stock symbol: ").upper()
            remove_stock(symbol)
        elif choice == "3":
            view_portfolio()
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
