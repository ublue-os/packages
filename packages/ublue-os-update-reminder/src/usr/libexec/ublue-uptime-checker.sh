#!/bin/bash
uptime_days=$(awk '{print int($1/86400)}' /proc/uptime)
trigger_file="/run/user/$UID/ublue-reboot-notifier-enabled"

if [ "$uptime_days" -ge 28 ]; then
    # Creating trigger file enables notifications in the service
    touch "$trigger_file"
    systemctl --user try-restart ublue-reboot-notifier.service || true
else
    # The trigger file should not exist, but if it does, remove it
    rm -f "$trigger_file"
    systemctl --user stop ublue-reboot-notifier.service 2>/dev/null || true
fi
