import subprocess
import platform
import re

OS = platform.system()


def set_volume(level):
    """Set system volume (0-100)."""
    try:
        level = max(0, min(100, int(level)))

        if OS == "Windows":
            # Use PowerShell to set volume
            script = f"""
$wshShell = New-Object -ComObject WScript.Shell
$volume = {level}
$wshShell = New-Object -comObject WScript.Shell

Add-Type -TypeDefinition @'
using System.Runtime.InteropServices;
[Guid("5CDF2C82-841E-4546-9722-0CF74078229A"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IAudioEndpointVolume {{
    int f(); int g(); int h(); int i();
    int SetMasterVolumeLevelScalar(float fLevel, System.Guid pguidEventContext);
    int j();
    int GetMasterVolumeLevelScalar(out float pfLevel);
    int k(); int l(); int m(); int n();
    int SetMute([MarshalAs(UnmanagedType.Bool)] bool bMute, System.Guid pguidEventContext);
    int GetMute(out bool pbMute);
}}
[Guid("D666063F-1587-4E43-81F1-B948E807363F"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IMMDevice {{
    int Activate(ref System.Guid id, int clsCtx, int activationParams, out IAudioEndpointVolume aev);
}}
[Guid("A95664D2-9614-4F35-A746-DE8DB63617E6"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IMMDeviceEnumerator {{
    int f();
    int GetDefaultAudioEndpoint(int dataFlow, int role, out IMMDevice endpoint);
}}
[ComImport, Guid("BCDE0395-E52F-467C-8E3D-C4579291692E")]
class MMDeviceEnumeratorComObject {{ }}
public class Audio {{
    static IAudioEndpointVolume Vol() {{
        var enumerator = new MMDeviceEnumeratorComObject() as IMMDeviceEnumerator;
        IMMDevice dev = null;
        Marshal.ThrowExceptionForHR(enumerator.GetDefaultAudioEndpoint(0, 1, out dev));
        IAudioEndpointVolume epv = null;
        var epvid = typeof(IAudioEndpointVolume).GUID;
        Marshal.ThrowExceptionForHR(dev.Activate(ref epvid, 23, 0, out epv));
        return epv;
    }}
    public static float Volume {{
        get {{ float v = -1; Marshal.ThrowExceptionForHR(Vol().GetMasterVolumeLevelScalar(out v)); return v; }}
        set {{ Marshal.ThrowExceptionForHR(Vol().SetMasterVolumeLevelScalar(value, System.Guid.Empty)); }}
    }}
    public static bool Mute {{
        get {{ bool mute; Marshal.ThrowExceptionForHR(Vol().GetMute(out mute)); return mute; }}
        set {{ Marshal.ThrowExceptionForHR(Vol().SetMute(value, System.Guid.Empty)); }}
    }}
}}
'@
[Audio]::Volume = {level / 100}
"""
            result = subprocess.run(
                ["powershell", "-Command", script],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                return f"🔊 Volume set to {level}%"
            else:
                # Simpler fallback using nircmd if available
                result2 = subprocess.run(
                    ["nircmd", "setsysvolume", str(int(level * 655.35))],
                    capture_output=True, timeout=5
                )
                if result2.returncode == 0:
                    return f"🔊 Volume set to {level}%"
                return f"Volume set attempted to {level}% (may need nircmd installed)"

        elif OS == "Darwin":  # macOS
            subprocess.run(["osascript", "-e", f"set volume output volume {level}"], timeout=5)
            return f"🔊 Volume set to {level}%"

        elif OS == "Linux":
            subprocess.run(["amixer", "-q", "sset", "Master", f"{level}%"], timeout=5)
            return f"🔊 Volume set to {level}%"

        return "Volume control not supported on this OS."

    except Exception as e:
        return f"Volume error: {str(e)}"


def mute_volume():
    """Mute system audio."""
    try:
        if OS == "Windows":
            script = "(New-Object -comObject Shell.Application).Windows() | ForEach-Object { }; $wsh = New-Object -ComObject WScript.Shell; $wsh.SendKeys([char]173)"
            subprocess.run(["powershell", "-Command", script], capture_output=True, timeout=5)
            return "🔇 Audio muted"
        elif OS == "Darwin":
            subprocess.run(["osascript", "-e", "set volume with output muted"], timeout=5)
            return "🔇 Audio muted"
        elif OS == "Linux":
            subprocess.run(["amixer", "-q", "sset", "Master", "mute"], timeout=5)
            return "🔇 Audio muted"
    except Exception as e:
        return f"Mute error: {str(e)}"


def unmute_volume():
    """Unmute system audio."""
    try:
        if OS == "Windows":
            script = "$wsh = New-Object -ComObject WScript.Shell; $wsh.SendKeys([char]173)"
            subprocess.run(["powershell", "-Command", script], capture_output=True, timeout=5)
            return "🔊 Audio unmuted"
        elif OS == "Darwin":
            subprocess.run(["osascript", "-e", "set volume without output muted"], timeout=5)
            return "🔊 Audio unmuted"
        elif OS == "Linux":
            subprocess.run(["amixer", "-q", "sset", "Master", "unmute"], timeout=5)
            return "🔊 Audio unmuted"
    except Exception as e:
        return f"Unmute error: {str(e)}"


def get_volume():
    """Get current volume level."""
    try:
        if OS == "Windows":
            script = """
Add-Type -TypeDefinition @'
using System.Runtime.InteropServices;
[Guid("5CDF2C82-841E-4546-9722-0CF74078229A"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IAudioEndpointVolume {
    int f(); int g(); int h(); int i();
    int SetMasterVolumeLevelScalar(float fLevel, System.Guid pguidEventContext);
    int j();
    int GetMasterVolumeLevelScalar(out float pfLevel);
    int k(); int l(); int m(); int n();
    int SetMute([MarshalAs(UnmanagedType.Bool)] bool bMute, System.Guid pguidEventContext);
    int GetMute(out bool pbMute);
}
[Guid("D666063F-1587-4E43-81F1-B948E807363F"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IMMDevice {
    int Activate(ref System.Guid id, int clsCtx, int activationParams, out IAudioEndpointVolume aev);
}
[Guid("A95664D2-9614-4F35-A746-DE8DB63617E6"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
interface IMMDeviceEnumerator {
    int f();
    int GetDefaultAudioEndpoint(int dataFlow, int role, out IMMDevice endpoint);
}
[ComImport, Guid("BCDE0395-E52F-467C-8E3D-C4579291692E")]
class MMDeviceEnumeratorComObject { }
public class Audio {
    static IAudioEndpointVolume Vol() {
        var enumerator = new MMDeviceEnumeratorComObject() as IMMDeviceEnumerator;
        IMMDevice dev = null;
        Marshal.ThrowExceptionForHR(enumerator.GetDefaultAudioEndpoint(0, 1, out dev));
        IAudioEndpointVolume epv = null;
        var epvid = typeof(IAudioEndpointVolume).GUID;
        Marshal.ThrowExceptionForHR(dev.Activate(ref epvid, 23, 0, out epv));
        return epv;
    }
    public static float Volume {
        get { float v = -1; Marshal.ThrowExceptionForHR(Vol().GetMasterVolumeLevelScalar(out v)); return v; }
    }
}
'@
[Math]::Round([Audio]::Volume * 100)
"""
            result = subprocess.run(["powershell", "-Command", script], capture_output=True, text=True, timeout=10)
            level = result.stdout.strip()
            return f"🔊 Current volume: {level}%"
        return "Volume check not supported on this OS."
    except Exception as e:
        return f"Volume error: {str(e)}"