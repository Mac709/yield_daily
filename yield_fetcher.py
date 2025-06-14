import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta
import matplotlib.dates as mdates

# Yahoo Financeの10年国債利回りのティッカー
TICKER = "^TNX"

# 出力ファイル名
CSV_FILE = "yield_history.csv"
PLOT_FILE = "yield_plot.png"

# データ取得（当日分）
today = datetime.today()
today_str = today.strftime('%Y-%m-%d')
data = yf.download(TICKER, start=today_str, end=today_str, auto_adjust=False)

if data.empty:
    print("No data available for today.")
    exit()

# 利回りの終値を取得（%表記に変換、^TNXは0.1%単位なので10で割る）
yield_today = data['Close'].iloc[-1] / 10

# データをDataFrameに整形
new_entry = pd.DataFrame({
    "Date": [today],
    "Yield": [yield_today]
})

# 既存の履歴を読み込む（あれば）
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
    df['Date'] = pd.to_datetime(df['Date'])
    df = pd.concat([df, new_entry], ignore_index=True)
    df = df.drop_duplicates(subset="Date", keep="last")
else:
    df = new_entry

# 日付でソート
df = df.sort_values("Date")

# 保存
df.to_csv(CSV_FILE, index=False)

# 直近1ヶ月のデータ抽出
one_month_ago = today - timedelta(days=30)
df_recent = df[df['Date'] >= one_month_ago]

# 日付列を明示的にdatetime型に変換
df_recent['Date'] = pd.to_datetime(df_recent['Date'])

# プロット
plt.figure(figsize=(10, 5))
plt.plot(df_recent['Date'], df_recent['Yield'], label='10Y US Treasury Yield (Last 1 Month)', color='blue')

# 横軸の範囲を直近1ヶ月に限定
plt.xlim(one_month_ago, today)

# 日付表示の調整
plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=3))  # 3日おきに目盛り
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))

plt.xlabel('Date')
plt.ylabel('Yield (%)')
plt.title('10-Year US Treasury Yield - Last 1 Month')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(PLOT_FILE)
plt.close()

print(f"Saved plot to {PLOT_FILE}")
