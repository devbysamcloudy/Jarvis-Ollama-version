import system_info, weather, memory, voice, security, logger
import dashboard, file_organizer, ai
import os, getpass, json
from datetime import datetime

jarvis_logger = logger.Logger()

current_user = None
current_user_data = None

def load_json(filename, default):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except:
        return default

def save_json(filename, data):
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving {filename}: {e}")

def load_users():
    return load_json("users.json", [])

def save_users(users):
    save_json("users.json", users)

def load_user_data(username):
    return load_json(f"{username}_data.json", {
        "username": username,
        "login_history": [],
        "commands": [],
        "file_actions": [],
        "preferences": {}
    })

def save_user_data(username, data):
    save_json(f"{username}_data.json", data)

def register():
    users = load_users()
    print("\n--- REGISTER ---")
    username = input("Choose username: ").strip()
    for user in users:
        if user["username"] == username:
            print("Username already exists.")
            return

    password = input("Choose password: ").strip()
    confirm_password = input("Confirm password: ").strip()
    if password != confirm_password:
        print("Passwords do not match.")
        return

    full_name = input("Enter full name: ").strip()
    new_user = {
        "user_id": len(users) + 1,
        "username": username,
        "password": password,
        "full_name": full_name,
        "created_at": datetime.now().isoformat()
    }

    users.append(new_user)
    save_users(users)

    user_data = {
        "username": username,
        "full_name": full_name,
        "login_history": [],
        "commands": [],
        "file_actions": [],
        "preferences": {}
    }
    save_user_data(username, user_data)
    print("Registration successful.")

def login():
    global current_user, current_user_data
    users = load_users()
    print("\n--- LOGIN ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    for user in users:
        if user["username"] == username and user["password"] == password:
            current_user = username
            current_user_data = load_user_data(username)
            current_user_data["login_history"].append(datetime.now().isoformat())
            save_user_data(username, current_user_data)
            print(f"Welcome {user.get('full_name', username)}")
            return True

    print("Invalid credentials")
    return False

def logout():
    global current_user, current_user_data
    current_user = None
    current_user_data = None

def require_login():
    if not current_user:
        print("Login first")
        return False
    return True

def save_action(kind, details, status="success"):
    if not current_user:
        return
    entry = {"timestamp": datetime.now().isoformat(), "status": status}
    if kind == "command":
        entry["command"] = details
        current_user_data["commands"].append(entry)
    else:
        entry["action"] = details
        current_user_data["file_actions"].append(entry)
    save_user_data(current_user, current_user_data)

dashboard.show_dashboard()

while True:
    command = input("> ").lower()

    if command == "register":
        register()
    elif command == "login":
        if login():
            dashboard.show_dashboard(current_user)
    elif command == "logout":
        if require_login():
            logout()
            dashboard.show_dashboard()
    elif command == "exit":
        break

    elif command.startswith("open") and require_login():
        target = command[5:].strip()
        if not target:
            print("Specify what to open (e.g., 'open chrome')")
            continue
        safe, msg = security.validate_command(command)
        if not safe:
            jarvis_logger.log_action(current_user, "open", command, f"BLOCKED: {msg}")
            print(f"Security block: {msg}")
            save_action("command", f"open {target}", "blocked")
        else:
            if not security.confirm_dangerous_action("open", target):
                jarvis_logger.log_action(current_user, "open", target, "CANCELLED")
                print("Open cancelled")
                save_action("command", f"open {target}", "cancelled")
            else:
                result = system_info.open_program(target)
                jarvis_logger.log_action(current_user, "open", target, result)
                print(result)
                save_action("command", f"open {target}", "success")


    elif command.startswith("kill") and require_login():
        target = command[5:].strip()
        if not target:
            print("Specify what to kill (e.g., 'kill notepad')")
            continue
        safe, msg = security.validate_command(command)
        if not safe:
            jarvis_logger.log_action(current_user, "kill", command, f"BLOCKED: {msg}")
            print(f"Security block: {msg}")
            save_action("command", f"kill {target}", "blocked")
        else:
            safe, msg = security.validate_kill_target(target)
            if not safe:
                jarvis_logger.log_action(current_user, "kill", target, f"BLOCKED: {msg}")
                print(f"Security block: {msg}")
                save_action("command", f"kill {target}", "blocked")
            else:
                confirmed = security.confirm_dangerous_action("kill", target)
                if not confirmed:
                    jarvis_logger.log_action(current_user, "kill", target, "CANCELLED")
                    print("Kill cancelled")
                    save_action("command", f"kill {target}", "cancelled")
                else:
                    result = system_info.kill_process(target)
                    jarvis_logger.log_action(current_user, "kill", target, "SUCCESS")
                    for item in result:
                        print(f"Terminated: {item}")
                    save_action("command", f"kill {target}", "success")

    elif command == "cpu" and require_login():
        print(f"CPU: {system_info.get_cpu()}%")
        save_action("command", "cpu")

    elif command == "battery" and require_login():
        print(f"Battery: {system_info.get_battery()}")
        save_action("command", "battery")

    elif command == "disk" and require_login():
        print(f"Disk: {system_info.get_disk()}")
        save_action("command", "disk")

    elif command == "processes" and require_login():
        for p in system_info.get_top_processes():
            if p["name"]:
                print(f"{p['name']}: {p['cpu_percent']}%")
        save_action("command", "processes")

    elif command.startswith("organize") and require_login():
        parts = command.split()
        folder = parts[1] if len(parts) > 1 else "."
        if os.path.exists(folder):
            original = os.getcwd()
            os.chdir(folder)
            file_organizer.organize_by_type()
            os.chdir(original)
            save_action("file", f"organized {folder}")
        else:
            print("Folder not found")

    elif command == "undo" and require_login():
        file_organizer.undo_organize()
        save_action("file", "undo")

    elif command.startswith("weather") and require_login():
        city = command[8:]
        print(weather.get_weather(city))
        save_action("command", f"weather {city}")

    elif command == "voice" and require_login():
        voice.speak("Voice mode")
        while True:
            cmd = voice.listen()
            if not cmd:
                continue
            if "exit" in cmd or "stop" in cmd:
                break
            voice.process_with_ai(cmd)
        save_action("command", "voice")

    elif command == "logs" and require_login():
        try:
            lines = input("Lines (default 10): ").strip()
            lines = int(lines) if lines else 10
            jarvis_logger.view_logs(lines)
        except:
            jarvis_logger.view_logs()
        save_action("command", "logs")

    else:
        if require_login():
            response = ai.ask_ai(command)
            print("Jarvis:", response)
            save_action("command", command, "ai_response")