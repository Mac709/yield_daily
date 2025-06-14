# yield_fetcher.py

import yfinance as yf
import pandas as pd
from datetime import datetime

def fetch_yield():
    ticker = "^TNX"
    data = yf.Ticker(ticker)
    hist = data.history(period="1d")
    
    if hist.empty:
        print("データ取得失敗")
        return
    
    yield_value = hist['Close'].iloc[-1] / 100
    today = datetime.now().strftime("%Y-%m-%d")

    df = pd.DataFrame({
        "date": [today],
        "10y_yield": [yield_value]
    })

    try:
        existing = pd.read_csv("yield_history.csv")
        df = pd.concat([existing, df]).drop_duplicates("date", keep="last")
    except FileNotFoundError:
        pass

    df.to_csv("yield_history.csv", index=False)
    print(f"{today}: {yield_value}% を保存しました。")

if __name__ == "__main__":
    fetch_yield()
