# ublue-os-update-reminder

This package provides a reboot reminder system for Universal Blue systems that have been running for an extended period without a reboot.

## How it works

1. The `ublue-uptime-checker.timer` runs daily and executes `ublue-uptime-checker.service`
2. If system uptime is 28+ days, it enables the `ublue-reboot-notifier.service`
3. The reboot notifier watches for screen unlock events via D-Bus
4. When the screen is unlocked and uptime is 30+ days, it directly shows a notification
5. After a reboot, `ublue-uptime-checker-boot.service` automatically disables the notifier

This two-service approach was taken so that the D-Bus watcher is not active/ running until the uptime exceeds 28 days. This could also be implemented perhaps by using systemd's capabilities to subscribe to D-Bus interfaces.

## Components

### Systemd Services

- `ublue-uptime-checker.timer` - Runs daily to check system uptime
- `ublue-uptime-checker.service` - Checks uptime and enables/disables the reboot notifier
- `ublue-uptime-checker-boot.service` - Runs on boot to disable notifications after reboot
- `ublue-reboot-notifier.service` - Watches for screen unlock events and shows notifications directly

### Scripts

- `ublue-uptime-checker.sh` - Checks system uptime and manages notification service
- `ublue-reboot-notifier-watcher.py` - D-Bus monitor for screen unlock events with integrated notification display

## Dependencies

- `python3-dbus-next` - For D-Bus communication in Python
- `libnotify` - For desktop notifications
- `kdialog` (optional) - For KDE notifications

