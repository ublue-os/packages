if [ "$EUID" -ne 0 ]; then
    bootc() {
        # Check if the command is already running with sudo
        if [ "$EUID" -eq 0 ]; then
            /usr/bin/bootc "$@"
        else
            sudo /usr/bin/bootc "$@"
        fi
    }
fi
