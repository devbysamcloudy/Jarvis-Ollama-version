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

        # ── OPEN PROGRAM ─────────────────────────────────────
        elif command.startswith("open "):
            command_type = "system"
            target = command[5:].strip()
            safe, msg = security.validate_command(command)
            if not safe:
                response = f"Security block: {msg}"
                success = False
            else:
                result = system_info.open_program(target)
                response = result or f"Opened {target}"

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
            if "error" in result:
                response = result["error"]
                success = False
            else:
                response = result["message"]

        elif command.startswith("undo"):
            command_type = "file"
            parts = command.split()
            folder = parts[1] if len(parts) > 1 else "."
            result = file_organizer.undo_organize(folder)
            if "error" in result:
                response = result["error"]
                success = False
            else:
                response = result["message"]

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

        # ── HELP ─────────────────────────────────────────────
        elif command == "help":
            response = (
                "Available commands:\n"
                "  cpu               — CPU usage\n"
                "  battery           — Battery status\n"
                "  disk              — Disk usage\n"
                "  processes         — Top processes\n"
                "  open [app]        — Open a program (e.g. open notepad)\n"
                "  kill [app]        — Kill a process\n"
                "  organize [folder] — Organize folder (e.g. organize desktop)\n"
                "  undo [folder]     — Undo organization\n"
                "  list files [folder] — List files in folder\n"
                "  weather [city]    — Get weather\n"
                "  Or just chat with JARVIS!"
            )
            # ── LOGS ─────────────────────────────────────────────
        elif command == "logs":
            command_type = "general"
            try:
                with open("jarvis.log", "r") as f:
                    lines = f.readlines()
                last_10 = "".join(lines[-10:]) if lines else "No logs yet"
                response = last_10
            except FileNotFoundError:
                response = "No log file found yet"

        # ── AI FALLBACK ──────────────────────────────────────
        else:
            command_type = "ai"
            response = ai.ask_ai(command)

    except Exception as e:
        response = f"Error: {str(e)}"
        success = False

    # Save to DB
    save_command(user_id, command, response, command_type, success)
    jarvis_logger.log_action(str(user_id), command_type, command, response[:100])

    return jsonify({
        "command": command,
        "response": response,
        "type": command_type,
        "success": success,
    }), 200
