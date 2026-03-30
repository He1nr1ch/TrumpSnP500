import io
import yfinance as yf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, Response

app = Flask(__name__)

@app.route('/')
def chart():
    ticker = "^GSPC"
    start_date = "2025-01-20"
    interval = "1d"

    data = yf.download(ticker, start=start_date, interval=interval, auto_adjust=True)
    if data.empty:
        return Response("No data fetched. Check ticker or internet connection.", status=503)

    price_column = 'Adj Close' if 'Adj Close' in data.columns else 'Close'
    first_price = data[price_column].iloc[0].item()
    last_price = data[price_column].iloc[-1].item()
    percent_change = ((last_price - first_price) / first_price) * 100
    change_color = 'green' if percent_change >= 0 else 'red'

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(data.index, data[price_column], label=f'S&P 500 {price_column}', color='blue')
    ax.annotate(f'{percent_change:.2f}%',
                xy=(data.index[-1], last_price),
                xytext=(data.index[-1], last_price * 1.05),
                fontsize=24,
                fontweight='bold',
                color=change_color)
    ax.set_title(f'S&P 500 {price_column} - From January 20, 2025 Onwards')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (USD)')
    ax.grid(True)
    ax.legend()
    fig.autofmt_xdate()
    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return Response(buf.getvalue(), mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)