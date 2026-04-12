import requests

COINGECKO_URL = "https://api.coingecko.com/api/v3"

COIN_ALIASES = {
    "bitcoin": "bitcoin", "btc": "bitcoin",
    "ethereum": "ethereum", "eth": "ethereum",
    "solana": "solana", "sol": "solana",
    "dogecoin": "dogecoin", "doge": "dogecoin",
    "cardano": "cardano", "ada": "cardano",
    "xrp": "ripple", "ripple": "ripple",
    "bnb": "binancecoin", "binance": "binancecoin",
    "usdt": "tether", "tether": "tether",
    "usdc": "usd-coin",
    "polygon": "matic-network", "matic": "matic-network",
    "litecoin": "litecoin", "ltc": "litecoin",
}


def get_crypto_price(coin="bitcoin"):
    """Get price of a single coin."""
    try:
        coin_id = COIN_ALIASES.get(coin.lower(), coin.lower())
        res = requests.get(
            f"{COINGECKO_URL}/simple/price",
            params={"ids": coin_id, "vs_currencies": "usd", "include_24hr_change": "true"},
            timeout=10,
        )
        data = res.json()
        if coin_id not in data:
            return f"Coin '{coin}' not found. Try: bitcoin, ethereum, solana, dogecoin..."

        price = data[coin_id]["usd"]
        change = data[coin_id].get("usd_24h_change", 0)
        arrow = "📈" if change >= 0 else "📉"
        return f"{arrow} {coin.upper()}: ${price:,.4f} ({change:+.2f}% 24h)"

    except Exception as e:
        return f"Crypto error: {str(e)}"


def get_top_cryptos(count=5):
    """Get top cryptocurrencies by market cap."""
    try:
        res = requests.get(
            f"{COINGECKO_URL}/coins/markets",
            params={
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": count,
                "page": 1,
                "sparkline": False,
            },
            timeout=10,
        )
        coins = res.json()
        if not coins:
            return "No crypto data found."

        lines = []
        for i, c in enumerate(coins):
            change = c.get("price_change_percentage_24h", 0) or 0
            arrow = "📈" if change >= 0 else "📉"
            lines.append(
                f"{i+1}. {arrow} {c['name']} ({c['symbol'].upper()}): "
                f"${c['current_price']:,.4f} ({change:+.2f}%)"
            )
        return " Top Cryptos:\n" + "\n".join(lines)

    except Exception as e:
        return f"Crypto error: {str(e)}"