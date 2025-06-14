import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Yahoo Financeの10年国債利回りのティッカー
TICKER = "^TNX"

# 出力ファイル名
CSV_FILE = "yield_history.csv"
PLOT_FILE = "yield_plot.png"

# データ取得（当日分）
today = datetime.today().strftime('%Y-%m-%d')
data = yf.download(TICKER, start=today, end=today)

if data.empty:
    print("No data available for today.")
    exit()

# 利回りの終値を取得
yield_today = data['Close'].iloc[-1]

# データをDataFrameに整形
new_entry = pd.DataFrame({
    "Date": [today],
    "Yield": [yield_today]
})

# 既存の履歴を読み込む（あれば）
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
    df = pd.concat([df, new_entry], ignore_index=True)
    df = df.drop_duplicates(subset="Date", keep="last")
else:
    df = new_entry

# 日付でソート
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values("Date")

# 保存
df.to_csv(CSV_FILE, index=False)

# プロット
plt.figure(figsize=(10, 5))
plt.plot(df['Date'], df['Yield'], label='10Y US Treasury Yield', color='blue')
plt.xlabel('Date')
plt.ylabel('Yield (%)')
plt.title('10-Year US Treasury Yield Over Time')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(PLOT_FILE)
print(f"Saved plot to {PLOT_FILE}")
