from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models import CommandHistory
import system_info
import weather
import file_organizer
import ai
import security
import logger
import news
import crypto
import stocks
import sports
import reminder
import wikipedia_search
import volume
import screenshot
import subprocess
import webbrowser
import re

commands_bp = Blueprint("commands", __name__)
jarvis_logger = logger.Logger()


def save_command(user_id, command, response, command_type="general", success=True):
    cmd = CommandHistory(
        user_id=user_id,
        command_text=command,
        command_type=command_type,
        response_text=response,
        success=success,
        source="web",
    )
    db.session.add(cmd)
    db.session.commit()


def open_url(url):
    """Open a URL in the default browser."""
    if not url.startswith("http"):
        url = "https://" + url
    subprocess.Popen(["cmd", "/c", "start", url], shell=False)
    return url


@commands_bp.route("/run", methods=["POST"])
@jwt_required()
def run_command():
    user_id = get_jwt_identity()
    data = request.get_json()
    command = data.get("command", "").strip().lower()

    if not command:
        return jsonify({"error": "No command provided"}), 400

    response = ""
    command_type = "general"
    success = True

    try:

        # ── SYSTEM INFO ──────────────────────────────────────
        if command == "cpu":
            command_type = "system"
            response = f"CPU usage: {system_info.get_cpu()}%"

        elif command == "battery":
            command_type = "system"
            response = f"Battery: {system_info.get_battery()}"

        elif command == "disk":
            command_type = "system"
            response = f"Disk: {system_info.get_disk()}"

        elif command == "processes":
            command_type = "system"
            procs = system_info.get_top_processes()
            lines = [f"{p['name']}: {p['cpu_percent']}%" for p in procs if p.get("name")]
            response = "\n".join(lines) if lines else "No processes found"

        # ── VOLUME CONTROL ───────────────────────────────────
        elif command == "volume" or command == "get volume":
            command_type = "system"
            response = volume.get_volume()

        elif command == "mute":
            command_type = "system"
            response = volume.mute_volume()

        elif command == "unmute":
            command_type = "system"
            response = volume.unmute_volume()

        elif command.startswith("volume ") or command.startswith("set volume "):
            command_type = "system"
            parts = command.split()
            level = next((p for p in parts if p.isdigit()), None)
            if level:
                response = volume.set_volume(int(level))
            else:
                response = "Usage: volume 50  (or: set volume 75)"

        # ── SCREENSHOT ───────────────────────────────────────
        elif command in ("screenshot", "take screenshot", "capture screen"):
            command_type = "system"
            response = screenshot.take_screenshot()

        elif command in ("screenshots folder", "open screenshots"):
            command_type = "system"
            response = screenshot.open_screenshots_folder()

        # ── OPEN PROGRAM ─────────────────────────────────────
        elif command.startswith("open "):
            command_type = "system"
            target = command[5:].strip()

            # Check if it's a website
            web_pattern = r'\.(com|org|net|io|co|uk|gov|edu|me|app|dev|ai)'
            known_sites = [
                "youtube", "google", "github", "twitter", "x.com",
                "reddit", "facebook", "instagram", "linkedin", "netflix",
                "spotify", "twitch", "discord", "gmail", "maps"
            ]

            is_web = re.search(web_pattern, target) or target in known_sites or target.startswith("http")

            if is_web:
                site_map = {
                    "youtube": "https://youtube.com",
                    "google": "https://google.com",
                    "github": "https://github.com",
                    "twitter": "https://twitter.com",
                    "x": "https://x.com",
                    "reddit": "https://reddit.com",
                    "facebook": "https://facebook.com",
                    "instagram": "https://instagram.com",
                    "linkedin": "https://linkedin.com",
                    "netflix": "https://netflix.com",
                    "spotify": "https://open.spotify.com",
                    "twitch": "https://twitch.tv",
                    "discord": "https://discord.com/app",
                    "gmail": "https://mail.google.com",
                    "maps": "https://maps.google.com",
                }
                url = site_map.get(target, target)
                opened = open_url(url)
                response = f"🌐 Opened {opened}"
            else:
                safe, msg = security.validate_command(command)
                if not safe:
                    response = f"Security block: {msg}"
                    success = False
                else:
                    result = system_info.open_program(target)
                    response = result or f"Opened {target}"

        # ── OPEN MULTIPLE TABS ───────────────────────────────
        elif command.startswith("open tabs ") or command.startswith("tabs "):
            command_type = "system"
            raw = command.replace("open tabs ", "").replace("tabs ", "")
            sites = [s.strip() for s in re.split(r"[,\s]+and\s+|,\s*", raw) if s.strip()]
            opened = []
            for site in sites:
                url = open_url(site)
                opened.append(url)
            response = f"🌐 Opened {len(opened)} tabs:\n" + "\n".join(opened)

        # ── KILL PROCESS ─────────────────────────────────────
        elif command.startswith("kill "):
            command_type = "system"
            target = command[5:].strip()
            safe, msg = security.validate_command(command)
            if not safe:
                response = f"Security block: {msg}"
                success = False
            else:
                safe2, msg2 = security.validate_kill_target(target)
                if not safe2:
                    response = f"Security block: {msg2}"
                    success = False
                else:
                    result = system_info.kill_process(target)
                    response = "\n".join([f"Terminated: {r}" for r in result]) if result else f"No process named {target} found"

        # ── FILE ORGANIZER ───────────────────────────────────
        elif command.startswith("organize"):
            command_type = "file"
            parts = command.split()
            folder = parts[1] if len(parts) > 1 else "."
            result = file_organizer.organize_by_type(folder)
            response = result.get("error") or result.get("message", "Done")
            success = "error" not in result

        elif command.startswith("undo"):
            command_type = "file"
            parts = command.split()
            folder = parts[1] if len(parts) > 1 else "."
            result = file_organizer.undo_organize(folder)
            response = result.get("error") or result.get("message", "Done")
            success = "error" not in result

        elif command.startswith("list files"):
            command_type = "file"
            parts = command.split()
            folder = parts[2] if len(parts) > 2 else "."
            result = file_organizer.list_files(folder)
            if "error" in result:
                response = result["error"]
                success = False
            else:
                files = result.get("files", [])
                response = f"{result['count']} files in {result['path']}:\n" + "\n".join(files)

        # ── WEATHER ──────────────────────────────────────────
        elif command.startswith("weather"):
            command_type = "general"
            city = command[8:].strip() or "Nairobi"
            response = weather.get_weather(city)

        # ── NEWS ─────────────────────────────────────────────
        elif command in ("news", "headlines", "top news"):
            command_type = "general"
            response = news.get_headlines()

        elif command.startswith("news "):
            command_type = "general"
            topic = command[5:].strip()
            categories = ["business", "technology", "sports", "health", "science", "entertainment"]
            if topic in categories:
                response = news.get_headlines(category=topic)
            else:
                response = news.search_news(topic)

        elif command in ("world news", "international news"):
            command_type = "general"
            response = news.get_world_news()

        elif command in ("space news", "nasa news", "space"):
            command_type = "general"
            response = news.get_space_news()

        # ── CRYPTO ───────────────────────────────────────────
        elif command in ("crypto", "crypto prices", "top crypto", "cryptocurrency"):
            command_type = "general"
            response = crypto.get_top_cryptos()

        elif command.startswith("crypto ") or command.startswith("price "):
            command_type = "general"
            coin = command.replace("crypto ", "").replace("price ", "").strip()
            response = crypto.get_crypto_price(coin)

        # ── STOCKS ───────────────────────────────────────────
        elif command.startswith("stock ") or command.startswith("stocks "):
            command_type = "general"
            raw = command.replace("stock ", "").replace("stocks ", "").strip()
            symbols = [s.strip() for s in raw.split(",")]
            if len(symbols) > 1:
                response = stocks.get_multiple_stocks(symbols)
            else:
                response = stocks.get_stock_price(symbols[0])

        # ── SPORTS ───────────────────────────────────────────
        elif command.startswith("scores ") or command.startswith("last match "):
            command_type = "general"
            team = command.replace("scores ", "").replace("last match ", "").strip()
            response = sports.get_team_last_result(team)

        elif command.startswith("next match ") or command.startswith("fixtures "):
            command_type = "general"
            team = command.replace("next match ", "").replace("fixtures ", "").strip()
            response = sports.get_team_next_match(team)

        # ── WIKIPEDIA ────────────────────────────────────────
        elif command.startswith("wiki ") or command.startswith("wikipedia ") or command.startswith("search wiki "):
            command_type = "general"
            query = re.sub(r"^(wiki|wikipedia|search wiki)\s+", "", command).strip()
            response = wikipedia_search.search_wikipedia(query)

        # ── REMINDERS & TIMERS ───────────────────────────────
        elif command.startswith("remind me ") or command.startswith("reminder "):
            command_type = "general"
            # Parse: "remind me in 5 minutes to call mom" or "remind me 10 minutes meeting"
            raw = command.replace("remind me ", "").replace("reminder ", "").strip()

            # Try to extract "in X time to/about MESSAGE"
            match = re.match(r"(?:in\s+)?(.+?)\s+(?:to|about|that)\s+(.+)", raw)
            if match:
                time_part = match.group(1)
                message = match.group(2)
            else:
                # Just time, generic message
                time_part = raw
                message = "Reminder!"

            response = reminder.set_reminder(time_part, message)

        elif command.startswith("timer ") or command.startswith("set timer "):
            command_type = "general"
            duration = command.replace("timer ", "").replace("set timer ", "").strip()
            response = reminder.set_timer(duration)

        elif command in ("reminders", "list reminders", "my reminders"):
            command_type = "general"
            response = reminder.list_reminders()

        # ── LOGS ─────────────────────────────────────────────
        elif command == "logs":
            command_type = "general"
            try:
                with open("jarvis.log", "r") as f:
                    lines = f.readlines()
                response = "".join(lines[-10:]) if lines else "No logs yet"
            except FileNotFoundError:
                response = "No log file found yet"

        # ── HELP ─────────────────────────────────────────────
        elif command == "help":
            response = """Available commands:

SYSTEM:
  cpu                     — CPU usage
  battery                 — Battery status
  disk                    — Disk usage
  processes               — Top processes
  volume                  — Get volume level
  volume [0-100]          — Set volume (e.g. volume 50)
  mute / unmute           — Mute or unmute audio
  screenshot              — Take a screenshot
  open [app/site]         — Open app or website
  open tabs [a, b, c]     — Open multiple tabs
  kill [app]              — Kill a process
  organize [folder]       — Organize files by type
  undo [folder]           — Undo organization
  list files [folder]     — List files

INFO & DATA:
  news                    — Top headlines
  news [topic/category]   — News by topic (e.g. news technology)
  world news              — International news
  space news              — Space & NASA news
  crypto                  — Top crypto prices
  crypto [coin]           — Single coin price (e.g. crypto bitcoin)
  price [coin]            — Same as above
  stock [symbol]          — Stock price (e.g. stock AAPL or stock tesla)
  stocks [a, b, c]        — Multiple stocks
  weather [city]          — Weather

SPORTS:
  scores [team]           — Last match result
  next match [team]       — Next scheduled match

KNOWLEDGE:
  wiki [topic]            — Wikipedia summary

REMINDERS:
  remind me in [time] to [message]  — Set reminder
  timer [duration]        — Set countdown timer
  reminders               — List all reminders

  Or just chat with JARVIS!"""

        # ── AI FALLBACK ──────────────────────────────────────
        else:
            command_type = "ai"
            response = ai.ask_ai(command)

    except Exception as e:
        response = f"Error: {str(e)}"
        success = False

    save_command(user_id, command, response, command_type, success)
    jarvis_logger.log_action(str(user_id), command_type, command, response[:100])

    return jsonify({
        "command": command,
        "response": response,
        "type": command_type,
        "success": success,
    }), 200