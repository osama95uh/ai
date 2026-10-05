from __future__ import annotations
import os
import time
import subprocess
from typing import Any, Dict, List

def collect_snapshot() -> Dict[str, Any]:
    return {
        "timestamp": time.time(),
        "activeWindow": _active_window(),
        "applications": _visible_applications(),
        "userIdleSeconds": _idle_seconds(),
        "disk": _disk_snapshot()
    }

def _active_window() -> Dict[str, Any]:
    try:
        # Get active window title using xdotool
        win_id = subprocess.check_output(["xdotool", "getactivewindow"], text=True).strip()
        win_info = subprocess.check_output(["xdotool", "getwindowname", win_id], text=True).strip()
        return {"title": win_info, "application": "unknown", "pid": None}
    except:
        return {"title": None, "application": None, "pid": None}

def _visible_applications() -> List[str]:
    try:
        # List all windows via wmctrl
        out = subprocess.check_output(["wmctrl", "-l"], text=True)
        return list(set(line.split(None, 3)[3] for line in out.splitlines()))
    except:
        return []

def _idle_seconds() -> float:
    try:
        # xprintidle is the Linux equivalent of GetLastInputInfo
        return float(subprocess.check_output(["xprintidle"], text=True).strip()) / 1000.0
    except:
        return 0.0

def _disk_snapshot() -> Dict[str, Any]:
    st = os.statvfs('/')
    return {
        "path": "/",
        "freeBytes": st.f_bavail * st.f_frsize,
        "totalBytes": st.f_blocks * st.f_frsize,
        "percentUsed": (1 - (st.f_bavail / st.f_blocks)) * 100
    }