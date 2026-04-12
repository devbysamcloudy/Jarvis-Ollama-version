import requests
from datetime import datetime

BASE_URL = "https://www.thesportsdb.com/api/v1/json/3"


def get_team_last_result(team_name):
    """Get last match result for a team."""
    try:
        res = requests.get(
            f"{BASE_URL}/searchteams.php",
            params={"t": team_name},
            timeout=10,
        )
        data = res.json()
        teams = data.get("teams")
        if not teams:
            return f"Team '{team_name}' not found."

        team_id = teams[0]["idTeam"]
        team_full = teams[0]["strTeam"]

        events_res = requests.get(
            f"{BASE_URL}/eventslast.php",
            params={"id": team_id},
            timeout=10,
        )
        events = events_res.json().get("results", [])
        if not events:
            return f"No recent results for {team_full}."

        e = events[0]
        return (
            f"⚽ {team_full} last match:\n"
            f"   {e['strHomeTeam']} {e['intHomeScore']} — {e['intAwayScore']} {e['strAwayTeam']}\n"
            f"   {e['strLeague']} | {e['dateEvent']}"
        )

    except Exception as e:
        return f"Sports error: {str(e)}"


def get_team_next_match(team_name):
    """Get next scheduled match for a team."""
    try:
        res = requests.get(
            f"{BASE_URL}/searchteams.php",
            params={"t": team_name},
            timeout=10,
        )
        data = res.json()
        teams = data.get("teams")
        if not teams:
            return f"Team '{team_name}' not found."

        team_id = teams[0]["idTeam"]
        team_full = teams[0]["strTeam"]

        events_res = requests.get(
            f"{BASE_URL}/eventsnext.php",
            params={"id": team_id},
            timeout=10,
        )
        events = events_res.json().get("events", [])
        if not events:
            return f"No upcoming matches for {team_full}."

        e = events[0]
        return (
            f"📅 {team_full} next match:\n"
            f"   {e['strHomeTeam']} vs {e['strAwayTeam']}\n"
            f"   {e['strLeague']} | {e['dateEvent']} {e.get('strTime', '')}"
        )

    except Exception as e:
        return f"Sports error: {str(e)}"


def search_sports_news(sport="soccer"):
    """Get recent events in a sport."""
    try:
        res = requests.get(
            f"{BASE_URL}/search_all_leagues.php",
            params={"s": sport, "c": ""},
            timeout=10,
        )
        data = res.json()
        leagues = data.get("countrys", [])
        if not leagues:
            return f"No leagues found for {sport}."
        top = leagues[:5]
        lines = [f"{i+1}. {l['strLeague']} ({l.get('strCountry', 'International')})" for i, l in enumerate(top)]
        return f"🏆 Top {sport} leagues:\n" + "\n".join(lines)
    except Exception as e:
        return f"Sports error: {str(e)}"