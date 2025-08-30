#!/bin/bash
uptime_days=$(awk '{print int($1/86400)}' /proc/uptime)

if [ "$uptime_days" -ge 28 ]; then
    systemctl --user enable ublue-reboot-notifier.service
else
    systemctl --user disable ublue-reboot-notifier.service
fi
