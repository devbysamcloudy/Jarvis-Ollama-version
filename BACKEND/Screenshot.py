import subprocess
import os
import platform
from datetime import datetime

OS = platform.system()
SCREENSHOT_DIR = os.path.join(os.path.expanduser("~"), "Pictures", "JARVIS_Screenshots")


def ensure_dir():
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def take_screenshot(filename=None):
    """Take a screenshot and save it."""
    try:
        ensure_dir()
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        filepath = os.path.join(SCREENSHOT_DIR, filename)

        if OS == "Windows":
            script = f"""
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)
$bitmap.Save('{filepath}')
$graphics.Dispose()
$bitmap.Dispose()
"""
            result = subprocess.run(
                ["powershell", "-Command", script],
                capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0 and os.path.exists(filepath):
                size_kb = os.path.getsize(filepath) // 1024
                return f"📸 Screenshot saved: {filepath} ({size_kb} KB)"
            return f"Screenshot failed: {result.stderr}"

        elif OS == "Darwin":
            result = subprocess.run(["screencapture", filepath], capture_output=True, timeout=10)
            if result.returncode == 0:
                return f"📸 Screenshot saved: {filepath}"
            return "Screenshot failed on macOS."

        elif OS == "Linux":
            result = subprocess.run(["scrot", filepath], capture_output=True, timeout=10)
            if result.returncode == 0:
                return f"📸 Screenshot saved: {filepath}"
            # Try gnome-screenshot
            result2 = subprocess.run(["gnome-screenshot", "-f", filepath], capture_output=True, timeout=10)
            if result2.returncode == 0:
                return f"📸 Screenshot saved: {filepath}"
            return "Screenshot failed. Install scrot: sudo apt install scrot"

        return "Screenshot not supported on this OS."

    except Exception as e:
        return f"Screenshot error: {str(e)}"


def open_screenshots_folder():
    """Open the screenshots folder."""
    try:
        ensure_dir()
        if OS == "Windows":
            subprocess.Popen(["explorer", SCREENSHOT_DIR])
        elif OS == "Darwin":
            subprocess.Popen(["open", SCREENSHOT_DIR])
        elif OS == "Linux":
            subprocess.Popen(["xdg-open", SCREENSHOT_DIR])
        return f"📂 Opened screenshots folder: {SCREENSHOT_DIR}"
    except Exception as e:
        return f"Error opening folder: {str(e)}"