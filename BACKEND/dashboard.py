import os
import threading
import time
from datetime import datetime
import system_info

def clear_screen():
    """Clears the entire screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_current_time():
    """Returns formatted time and date"""
    now = datetime.now()
    current_time = now.strftime("%I:%M %p")
    current_date = now.strftime("%B %d, %Y")
    return current_time, current_date

def show_header(username=None):
    """Title of AI with current time and welcome message"""
    time_str, date_str = get_current_time()
    print("=" * 60)
    print(f"JARVIS COMMAND DASHBOARD - {time_str}")
    print(f"                      {date_str}")
    print("=" * 60)
    if username:
        print(f"Welcome back, {username}!")
        print("-" * 60)

def show_status():
    """Indicates CPU status, Battery, and RAM"""
    cpu = system_info.get_cpu()
    ram = system_info.get_ram()
    battery = system_info.get_battery()

    print("\n SYSTEM STATUS:")
    print(f"   CPU: {cpu}%  |  RAM: {ram}%  |  BATTERY: {battery}")
    print("-" * 60)

def show_commands():
    """Indicates commands one can type"""
    print("\n COMMANDS:")
    print("   system:  cpu | ram | battery | disk | processes")
    print("   actions: kill [name] | open [name]")
    print("   other:   weather [city] | logs | hello | voice")
    print("   tools:   menu | clear | exit | login | logout")
    print("-" * 60)

def show_dashboard(username=None):
    """Shows the complete dashboard with optional username"""
    clear_screen()
    show_header(username)
    show_status()
    show_commands()
    print("\n ENTER COMMAND:")