"""
Data Loader - Fetch and prepare stock market data
"""

import pandas as pd
import sqlite3
import yfinance as yf


def fetch_stock_data(tickers: list, period: str = "1y") -> pd.DataFrame:
    """
    Fetch historical stock data from Yahoo Finance.
    """
    all_data = []
    
    for ticker in tickers:
        print(f"Fetching data for {ticker}...")
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        hist['ticker'] = ticker
        hist.reset_index(inplace=True)
        all_data.append(hist)
    
    combined = pd.concat(all_data, ignore_index=True)
    combined.columns = [col.lower().replace(' ', '_') for col in combined.columns]
    
    return combined


def create_database(df: pd.DataFrame, db_path: str = "data/stock_database.db"):
    """
    Create SQLite database from DataFrame.
    """
    import os
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    df.to_sql('stock_prices', conn, index=False, if_exists='replace')
    
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ticker ON stock_prices(ticker)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_date ON stock_prices(date)")
    conn.commit()
    conn.close()
    
    print(f"✅ Database created at {db_path}")
    print(f"📊 Total records: {len(df)}")


if __name__ == "__main__":
    tickers = ['AAPL', 'MSFT', 'NVDA']
    data = fetch_stock_data(tickers, period="1y")
    create_database(data)
    data.to_csv('data/stock_data.csv', index=False)
    print("✅ CSV backup saved to data/stock_data.csv")