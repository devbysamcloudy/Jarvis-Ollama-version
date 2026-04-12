import requests

WIKI_URL = "https://en.wikipedia.org/api/rest_v1/page/summary"
WIKI_SEARCH_URL = "https://en.wikipedia.org/w/api.php"


def search_wikipedia(query):
    """Search Wikipedia and return a summary."""
    try:
        # First try direct page summary
        res = requests.get(
            f"{WIKI_URL}/{query.replace(' ', '_')}",
            headers={"User-Agent": "JARVIS/1.0"},
            timeout=10,
        )

        if res.status_code == 200:
            data = res.json()
            title = data.get("title", query)
            extract = data.get("extract", "No summary available.")
            # Trim to reasonable length
            if len(extract) > 500:
                extract = extract[:500] + "..."
            return f"📖 {title}:\n{extract}"

        # Fallback: search for the term
        search_res = requests.get(
            WIKI_SEARCH_URL,
            params={
                "action": "query",
                "list": "search",
                "srsearch": query,
                "format": "json",
                "srlimit": 3,
            },
            headers={"User-Agent": "JARVIS/1.0"},
            timeout=10,
        )
        results = search_res.json().get("query", {}).get("search", [])
        if not results:
            return f"No Wikipedia results found for '{query}'."

        # Get summary of top result
        top_title = results[0]["title"]
        res2 = requests.get(
            f"{WIKI_URL}/{top_title.replace(' ', '_')}",
            headers={"User-Agent": "JARVIS/1.0"},
            timeout=10,
        )
        if res2.status_code == 200:
            data = res2.json()
            extract = data.get("extract", "No summary available.")
            if len(extract) > 500:
                extract = extract[:500] + "..."
            return f"📖 {top_title}:\n{extract}"

        return f"Could not retrieve Wikipedia article for '{query}'."

    except Exception as e:
        return f"Wikipedia error: {str(e)}"