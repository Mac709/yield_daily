def plot_yield_history():
    df = pd.read_csv("yield_history.csv")
    df['date'] = pd.to_datetime(df['date'])
    
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 5))
    plt.plot(df['date'], df['10y_yield'], marker='o')
    plt.title("10-Year US Treasury Yield History")
    plt.xlabel("Date")
    plt.ylabel("Yield (%)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("yield_plot.png")
    plt.show()
