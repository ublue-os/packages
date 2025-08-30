# ublue-os-update-reminder

This package provides a reboot reminder system for Universal Blue systems that have been running for an extended period without a reboot.

## How it works

1. The `ublue-uptime-checker.timer` runs daily and executes `ublue-uptime-checker.service`
2. If system uptime is 28+ days, it creates a trigger file in `/run/user/$UID/`
3. The `ublue-reboot-notifier.service` is enabled by default but only starts when the trigger file exists
4. When active, it monitors D-Bus for screen unlock events and shows notifications if uptime ≥ 30 days
5. After a reboot, the trigger file automatically disappears (tmpfs cleanup) and notifications stop

## Components

### Systemd Services

- `ublue-uptime-checker.timer` - Runs daily to check system uptime
- `ublue-uptime-checker.service` - Checks uptime and manages trigger file in `/run/user/`
- `ublue-reboot-notifier.service` - Watches for screen unlock events via D-Bus (only active when needed)

### Scripts

- `ublue-uptime-checker.sh` - Checks system uptime and manages trigger file
- `ublue-reboot-notifier-watcher.py` - D-Bus monitor for screen unlock events + notifier
