import threading
import time
from datetime import datetime, timedelta
import re

reminders = []
_lock = threading.Lock()


def _reminder_thread(seconds, message, reminder_id):
    """Background thread that fires a reminder after delay."""
    time.sleep(seconds)
    with _lock:
        for r in reminders:
            if r["id"] == reminder_id:
                r["fired"] = True
                r["fired_at"] = datetime.now().strftime("%H:%M:%S")
                break
    print(f"\n⏰ JARVIS REMINDER: {message}\n")


def parse_time(time_str):
    """Parse time strings like '5 minutes', '1 hour', '30 seconds', '2 hours 30 minutes'."""
    time_str = time_str.lower().strip()
    total_seconds = 0

    patterns = [
        (r"(\d+)\s*hour[s]?", 3600),
        (r"(\d+)\s*hr[s]?", 3600),
        (r"(\d+)\s*minute[s]?", 60),
        (r"(\d+)\s*min[s]?", 60),
        (r"(\d+)\s*second[s]?", 1),
        (r"(\d+)\s*sec[s]?", 1),
    ]

    for pattern, multiplier in patterns:
        match = re.search(pattern, time_str)
        if match:
            total_seconds += int(match.group(1)) * multiplier

    return total_seconds if total_seconds > 0 else None


def set_reminder(time_str, message="Reminder!"):
    """Set a reminder after a time duration."""
    try:
        seconds = parse_time(time_str)
        if not seconds:
            return f"Could not understand time '{time_str}'. Try: '5 minutes', '1 hour', '30 seconds'"

        reminder_id = len(reminders) + 1
        fire_at = datetime.now() + timedelta(seconds=seconds)

        reminder = {
            "id": reminder_id,
            "message": message,
            "seconds": seconds,
            "fire_at": fire_at.strftime("%H:%M:%S"),
            "fired": False,
            "fired_at": None,
        }

        with _lock:
            reminders.append(reminder)

        thread = threading.Thread(
            target=_reminder_thread,
            args=(seconds, message, reminder_id),
            daemon=True,
        )
        thread.start()

        # Human-readable duration
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        parts = []
        if h: parts.append(f"{h} hour{'s' if h > 1 else ''}")
        if m: parts.append(f"{m} minute{'s' if m > 1 else ''}")
        if s: parts.append(f"{s} second{'s' if s > 1 else ''}")
        duration = ", ".join(parts)

        return f"⏰ Reminder set! I'll remind you in {duration} at {fire_at.strftime('%H:%M:%S')}.\nMessage: {message}"

    except Exception as e:
        return f"Reminder error: {str(e)}"


def list_reminders():
    """List all active and fired reminders."""
    with _lock:
        if not reminders:
            return "No reminders set."
        lines = []
        for r in reminders:
            status = f"✅ Fired at {r['fired_at']}" if r["fired"] else f"⏳ Due at {r['fire_at']}"
            lines.append(f"{r['id']}. {r['message']} — {status}")
        return "📋 Reminders:\n" + "\n".join(lines)


def set_timer(duration_str):
    """Set a countdown timer (alias for reminder with default message)."""
    return set_reminder(duration_str, "Timer complete!")