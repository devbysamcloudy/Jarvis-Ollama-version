import psutil
import subprocess
import os


class SystemInfo:

    def get_cpu(self):
        return psutil.cpu_percent(interval=1)

    def get_ram(self):
        memory = psutil.virtual_memory()
        return memory.percent

    def get_battery(self):
        battery = psutil.sensors_battery()
        if battery:
            return f"{battery.percent}% {'Plugged' if battery.power_plugged else 'Not Plugged'}"
        else:
            return "No battery detected"

    def get_disk(self):
        disk = psutil.disk_usage('/')
        return f"{disk.percent}% used"

    def get_top_processes(self):
        processes = []
        for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        top_cpu = sorted(
            processes,
            key=lambda x: x['cpu_percent'] or 0,
            reverse=True
        )[:3]

        return top_cpu

    def kill_process(self, process_name):
        killed = []

        for proc in psutil.process_iter(['name', 'pid']):
            try:
                if not proc.info['name']:
                    continue

                if process_name.lower() in proc.info['name'].lower():
                    proc.terminate()
                    killed.append(f"{proc.info['name']} (PID: {proc.info['pid']})")

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

        return killed if killed else ["No matching processes found"]

    def open_program(self, program_name):

        username = os.getlogin()

        common_programs = {
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'paint': 'mspaint.exe',
            'cmd': 'cmd.exe',
            'powershell': 'powershell.exe',
            'explorer': 'explorer.exe',

            'chrome': 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
            'firefox': 'C:\\Program Files\\Mozilla Firefox\\firefox.exe',
            'edge': 'msedge.exe',

            'word': 'winword.exe',
            'winword': 'winword.exe',
            'excel': 'excel.exe',
            'powerpoint': 'powerpnt.exe',
            'outlook': 'outlook.exe',

            'vs code': f'C:\\Users\\{username}\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe',
            'code': f'C:\\Users\\{username}\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe',
            'vscode': f'C:\\Users\\{username}\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe',

            'task manager': 'taskmgr.exe',
            'control panel': 'control.exe',
            'registry': 'regedit.exe'
        }

        program_key = program_name.lower()

        if program_key in common_programs:
            try:
                program_path = common_programs[program_key]
                subprocess.Popen(program_path)
                return f"Opened {program_name}"
            except FileNotFoundError:
                return f"Program file not found: {common_programs[program_key]}"
            except PermissionError:
                return f"Permission denied to open {program_name}"
            except Exception as e:
                return f"Failed to open {program_name}: {str(e)}"
        else:
            return f"Don't know how to open '{program_name}'"

    def search_and_open(self, program_name):

        search_paths = [
            "C:\\Program Files",
            "C:\\Program Files (x86)",
            f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Programs",
            f"C:\\Users\\{os.getlogin()}\\AppData\\Local",
            f"C:\\Users\\{os.getlogin()}\\AppData\\Roaming",
            "C:\\Windows\\System32"
        ]

        print(f"Searching for '{program_name}'...")
        found = []

        for path in search_paths:
            if not os.path.exists(path):
                continue

            try:
                for root, dirs, files in os.walk(path):

                    if len(found) >= 5:
                        break

                    for file in files:
                        if file.lower().endswith('.exe') and program_name.lower() in file.lower():
                            full_path = os.path.join(root, file)
                            found.append(full_path)
                            print(f"Found: {full_path}")

                            if len(found) >= 5:
                                break

            except (PermissionError, OSError):
                continue

        if found:
            try:
                subprocess.Popen(found[0])
                return f"Opened: {os.path.basename(found[0])}"
            except Exception as e:
                return f"Found but failed to open: {str(e)}"
        else:
            return f"Could not find '{program_name}' on your system"


_system = SystemInfo()

def get_cpu():
    return _system.get_cpu()

def get_ram():
    return _system.get_ram()

def get_battery():
    return _system.get_battery()

def get_disk():
    return _system.get_disk()

def get_top_processes():
    return _system.get_top_processes()

def kill_process(process_name):
    return _system.kill_process(process_name)

def open_program(program_name):
    return _system.open_program(program_name)

def search_and_open(program_name):
    return _system.search_and_open(program_name)