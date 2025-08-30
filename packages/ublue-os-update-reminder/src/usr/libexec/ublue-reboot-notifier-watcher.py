#!/usr/bin/env python3
import asyncio
import subprocess
import sys
from dbus_next.aio import MessageBus
from dbus_next import BusType

SCREENSAVER_SERVICE = "org.freedesktop.ScreenSaver"
SCREENSAVER_PATH = "/ScreenSaver"
SCREENSAVER_INTERFACE = "org.freedesktop.ScreenSaver"

def get_uptime_days():
    """Get system uptime in days."""
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.read().split()[0])
            return int(uptime_seconds / 86400)
    except (OSError, ValueError, IndexError):
        print("Warning: Unable to read system uptime from /proc/uptime", file=sys.stderr)
        return 0

def show_notification(uptime_days):
    title = "System Update Available"
    message = f"Your system has been running for {uptime_days} days. Please reboot to apply updates."

    subprocess.run([
        "notify-send",
        "--urgency=normal",
        "--expire-time=10000",
        "--icon=system-reboot",
        title,
        message
    ], check=False)

async def monitor_screensaver():
    """Monitor D-Bus for screensaver unlock events."""
    bus = await MessageBus(bus_type=BusType.SESSION).connect()
    introspection = await bus.introspect(SCREENSAVER_SERVICE, SCREENSAVER_PATH)
    obj = bus.get_proxy_object(SCREENSAVER_SERVICE, SCREENSAVER_PATH, introspection)
    iface = obj.get_interface(SCREENSAVER_INTERFACE)

    def on_active_changed(active: bool):
        if not active:  # Active=false means user unlocked screen
            uptime_days = get_uptime_days()
            if uptime_days >= 30:
                show_notification(uptime_days)

    iface.on_active_changed(on_active_changed)
    await asyncio.get_event_loop().create_future()

if __name__ == "__main__":
    asyncio.run(monitor_screensaver())
