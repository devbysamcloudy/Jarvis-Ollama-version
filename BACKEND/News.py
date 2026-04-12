import requests
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2"


def get_headlines(category="general", country="us", count=5):
    """Get top headlines by category."""
    try:
        res = requests.get(
            f"{BASE_URL}/top-headlines",
            params={
                "apiKey": NEWS_API_KEY,
                "category": category,
                "country": country,
                "pageSize": count,
            },
            timeout=10,
        )
        data = res.json()
        if data.get("status") != "ok":
            return f"News error: {data.get('message', 'Unknown error')}"

        articles = data.get("articles", [])
        if not articles:
            return "No headlines found."

        lines = [f"{i+1}. {a['title']} — {a['source']['name']}" for i, a in enumerate(articles)]
        return "\n".join(lines)

    except Exception as e:
        return f"News error: {str(e)}"


def get_world_news(count=5):
    """Get international/world news."""
    try:
        res = requests.get(
            f"{BASE_URL}/top-headlines",
            params={
                "apiKey": NEWS_API_KEY,
                "language": "en",
                "pageSize": count,
                "q": "world",
            },
            timeout=10,
        )
        data = res.json()
        articles = data.get("articles", [])
        if not articles:
            return "No world news found."
        lines = [f"{i+1}. {a['title']} — {a['source']['name']}" for i, a in enumerate(articles)]
        return "🌍 World News:\n" + "\n".join(lines)
    except Exception as e:
        return f"World news error: {str(e)}"


def get_space_news(count=5):
    """Get space news from Spaceflight News API (free, no key needed)."""
    try:
        res = requests.get(
            "https://api.spaceflightnewsapi.net/v4/articles/",
            params={"limit": count, "ordering": "-published_at"},
            timeout=10,
        )
        data = res.json()
        articles = data.get("results", [])
        if not articles:
            return "No space news found."
        lines = [f"{i+1}. {a['title']} — {a['news_site']}" for i, a in enumerate(articles)]
        return " Space News:\n" + "\n".join(lines)
    except Exception as e:
        return f"Space news error: {str(e)}"


def search_news(query, count=5):
    """Search news by keyword."""
    try:
        res = requests.get(
            f"{BASE_URL}/everything",
            params={
                "apiKey": NEWS_API_KEY,
                "q": query,
                "pageSize": count,
                "sortBy": "publishedAt",
                "language": "en",
            },
            timeout=10,
        )
        data = res.json()
        articles = data.get("articles", [])
        if not articles:
            return f"No news found for '{query}'."
        lines = [f"{i+1}. {a['title']} — {a['source']['name']}" for i, a in enumerate(articles)]
        return f" News for '{query}':\n" + "\n".join(lines)
    except Exception as e:
        return f"News search error: {str(e)}"