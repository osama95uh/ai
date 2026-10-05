from __future__ import annotations
import subprocess
from typing import Any, Dict
from .registry import ToolError, register

def _get_active_id() -> str:
    return subprocess.check_output(["xdotool", "getactivewindow"], text=True).strip()

@register("minimizeWindow")
def minimize_window(args: Dict[str, Any]) -> Dict[str, Any]:
    subprocess.run(["xdotool", "windowminimize", _get_active_id()])
    return {"result": "Window minimized."}

@register("maximizeWindow")
def maximize_window(args: Dict[str, Any]) -> Dict[str, Any]:
    subprocess.run(["wmctrl", "-r", ":ACTIVE:", "-b", "add,maximized_vert,maximized_horz"])
    return {"result": "Window maximized."}

@register("closeWindow")
def close_window(args: Dict[str, Any]) -> Dict[str, Any]:
    subprocess.run(["wmctrl", "-c", ":ACTIVE:"])
    return {"result": "Window closed."}

@register("switchApplication")
def switch_application(args: Dict[str, Any]) -> Dict[str, Any]:
    title = args.get("title")
    if title:
        subprocess.run(["wmctrl", "-a", str(title)])
        return {"result": f"Switched to: {title}"}
    subprocess.run(["xdotool", "key", "alt+Tab"])
    return {"result": "Cycled windows."}

@register("volumeUp")
def volume_up(args: Dict[str, Any]) -> Dict[str, Any]:
    step = int(args.get("amount", 5))
    subprocess.run(["amixer", "sset", "Master", f"{step}%+"], capture_output=True)
    return {"result": f"Volume increased by {step}%."}

@register("volumeDown")
def volume_down(args: Dict[str, Any]) -> Dict[str, Any]:
    step = int(args.get("amount", 5))
    subprocess.run(["amixer", "sset", "Master", f"{step}%-"], capture_output=True)
    return {"result": f"Volume decreased by {step}%."}

@register("setVolume")
def set_volume(args: Dict[str, Any]) -> Dict[str, Any]:
    percent = int(args.get("percent", 50))
    subprocess.run(["amixer", "sset", "Master", f"{percent}%"], capture_output=True)
    return {"result": f"Volume set to {percent}%."}

@register("muteToggle")
def mute_toggle(args: Dict[str, Any]) -> Dict[str, Any]:
    subprocess.run(["amixer", "sset", "Master", "toggle"], capture_output=True)
    return {"result": "Mute toggled."}

@register("brightnessUp")
def brightness_up(args: Dict[str, Any]) -> Dict[str, Any]:
    # লিনাক্সে brightness-এর জন্য 'light' টুলটি ইনস্টল করে রাখতে পারেন (sudo pacman -S light)
    subprocess.run(["light", "-A", "10"])
    return {"result": "Brightness increased."}

@register("brightnessDown")
def brightness_down(args: Dict[str, Any]) -> Dict[str, Any]:
    subprocess.run(["light", "-U", "10"])
    return {"result": "Brightness decreased."}

__all__ = [
    "minimize_window", "maximize_window", "close_window", 
    "switch_application", "volume_up", "volume_down", 
    "set_volume", "mute_toggle", "brightness_up", "brightness_down"
]