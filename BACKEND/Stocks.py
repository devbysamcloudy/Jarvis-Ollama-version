import requests
import os
from dotenv import load_dotenv

load_dotenv()

ALPHA_KEY = os.getenv("ALPHA_VANTAGE_KEY")
BASE_URL = "https://www.alphavantage.co/query"

STOCK_ALIASES = {
    "apple": "AAPL", "google": "GOOGL", "alphabet": "GOOGL",
    "microsoft": "MSFT", "tesla": "TSLA", "amazon": "AMZN",
    "meta": "META", "facebook": "META", "netflix": "NFLX",
    "nvidia": "NVDA", "amd": "AMD", "intel": "INTC",
    "twitter": "X", "x": "X", "spotify": "SPOT",
    "uber": "UBER", "airbnb": "ABNB", "paypal": "PYPL",
}


def get_stock_price(symbol):
    """Get current stock price for a symbol or company name."""
    try:
        ticker = STOCK_ALIASES.get(symbol.lower(), symbol.upper())

        res = requests.get(
            BASE_URL,
            params={
                "function": "GLOBAL_QUOTE",
                "symbol": ticker,
                "apikey": ALPHA_KEY,
            },
            timeout=10,
        )
        data = res.json()
        quote = data.get("Global Quote", {})

        if not quote or not quote.get("05. price"):
            return f"Stock '{symbol.upper()}' not found or API limit reached. Try again in a minute."

        price = float(quote["05. price"])
        change = float(quote["09. change"])
        change_pct = float(quote["10. change percent"].replace("%", ""))
        prev_close = float(quote["08. previous close"])
        arrow = "📈" if change >= 0 else "📉"

        return (
            f"{arrow} {ticker}: ${price:.2f}\n"
            f"   Change: {change:+.2f} ({change_pct:+.2f}%)\n"
            f"   Prev Close: ${prev_close:.2f}"
        )

    except Exception as e:
        return f"Stock error: {str(e)}"


def get_multiple_stocks(symbols):
    """Get prices for multiple stocks."""
    results = []
    for s in symbols:
        results.append(get_stock_price(s.strip()))
    return "\n".join(results)