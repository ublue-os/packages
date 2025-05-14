#!/bin/bash

if [ "$(id -u)" -ne 0 ]; then
  echo "This script must be run as root." >&2
  exit 1
fi

get_config() {
    SETUP_CONFIG_FILE="${SETUP_CONFIG_FILE:-/etc/ublue-os/setup.json}"
    QUERY="$1"
    FALLBACK="$2"
    shift
    shift
    OUTPUT="$(jq -r "$QUERY" "$SETUP_CONFIG_FILE" 2>/dev/null || echo "$FALLBACK")"
    if [ "$OUTPUT" == "null" ] ; then
        echo "$FALLBACK"
        return
    fi
    echo "$OUTPUT"
}

WARNING_MSG="This machine has secure boot turned on, but you haven't enrolled Universal Blue's keys. Failing to enroll these before rebooting **may cause your system to fail to boot**. Follow [the documentation](https://docs.projectbluefin.io/installation#secure-boot) ~for key enrollment information."
KEY_WARN_FILE="/run/user-motd-sbkey-warn.md"
KEY_DER_FILE="$(get_config '."der-path"' "/etc/pki/akmods/certs/akmods-ublue.der")"
IS_THIS_ENABLED="$(get_config '."check-secureboot"' "true")"

mokutil --sb-state | grep -q enabled
SB_ENABLED=$?

if [ $SB_ENABLED -ne 0 ]; then
    echo "Secure Boot disabled. Skipping..."
    exit 0
fi

if [ "$IS_THIS_ENABLED" == "false" ] ; then
    exit 0
fi

if mokutil --test-key "$KEY_DER_FILE"; then 
    echo "$WARNING_MSG" > $KEY_WARN_FILE
else
    [ -e $KEY_WARN_FILE ] && rm $KEY_WARN_FILE
fi
exit 0
