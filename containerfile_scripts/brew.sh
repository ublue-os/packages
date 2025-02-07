#!/usr/bin/bash

#region Setup

set -euxo pipefail

#endregion Setup

#region Functions

die() {
    echo >&2 "ERROR: $*"
    exit 1
}

writefile() {
    local dest="$1"
    mkdir -p "$(dirname "$dest")"
    cat >"$dest"
}

appendfile() {
    local dest="$1"
    mkdir -p "$(dirname "$dest")"
    cat >>"$dest"
}

#endregion Functions

#region Body

# Files to be copied to /usr/share/factory
FILES_TO_FACTORY=()

# Check /home is a symlink to /var/home
if [[ "$(realpath /home)" != "/var/home" ]]; then
    die "/home is not a symlink to /var/home."
fi

# Ensure the home symlink target exists.
mkdir -p "$(realpath /home)"

# Ensure root symlink target exists
mkdir -p "$(realpath /root)"

# Ensure git is installed, otherwise install it
if ! hash git; then
    dnf5 install -yq --setopt=install_weak_deps=0 git
fi

# Run Homebrew install script
export CI=${CI:-1}
export NONINTERACTIVE=1
/bin/bash <(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh) ||
    die "Something went wrong running Homebrew install.sh"
FILES_TO_FACTORY+=(/var/home/linuxbrew)

# Write /etc/profile.d/brew.sh
writefile /etc/profile.d/brew.sh <<'EOF'
[[ -d /home/linuxbrew/.linuxbrew && $- == *i* ]] && eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
EOF
FILES_TO_FACTORY+=(/etc/profile.d/brew.sh)

# Write brew bash completions
writefile /etc/profile.d/brew-bash-completion.sh <<'EMBEDEOF'
#!/bin/sh
# shellcheck shell=sh disable=SC1091,SC2039,SC2166
# Check for interactive bash and that we haven't already been sourced.
if [ "x${BASH_VERSION-}" != x -a "x${PS1-}" != x -a "x${BREW_BASH_COMPLETION-}" = x ]; then

    # Check for recent enough version of bash.
    if [ "${BASH_VERSINFO[0]}" -gt 4 ] ||
        [ "${BASH_VERSINFO[0]}" -eq 4 -a "${BASH_VERSINFO[1]}" -ge 2 ]; then
        if [ -w /home/linuxbrew/.linuxbrew ]; then
            if ! test -L /home/linuxbrew/.linuxbrew/etc/bash_completion.d/brew; then
                /home/linuxbrew/.linuxbrew/bin/brew completions link > /dev/null
            fi
        fi
        if test -d /home/linuxbrew/.linuxbrew/etc/bash_completion.d; then
            for rc in /home/linuxbrew/.linuxbrew/etc/bash_completion.d/*; do
                if test -r "$rc"; then
                . "$rc"
                fi
            done
            unset rc
        fi
    fi
    BREW_BASH_COMPLETION=1
    export BREW_BASH_COMPLETION
fi
EMBEDEOF
FILES_TO_FACTORY+=(/etc/profile.d/brew-bash-completion.sh)

# Write brew fish completions
writefile /usr/share/fish/vendor_conf.d/brew.fish <<'EMBEDEOF'
#!/usr/bin/fish
#shellcheck disable=all
if status --is-interactive
    if [ -d /home/linuxbrew/.linuxbrew ]
        eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
        if test -d (brew --prefix)/share/fish/completions
            set -p fish_complete_path (brew --prefix)/share/fish/completions
        end
        if test -d (brew --prefix)/share/fish/vendor_completions.d
            set -p fish_complete_path (brew --prefix)/share/fish/vendor_completions.d
        end
    end
end
EMBEDEOF

# Write brew resource limits
writefile "/etc/security/limits.d/30-brew-limits.conf" <<'EMBEDEOF'
#This file sets the resource limits for the users logged in via PAM,
#more specifically, users logged in on via SSH or tty (console).
#Limits related to terminals in Wayland/Xorg sessions depend on a
#change to /etc/systemd/user.conf.
#This does not affect resource limits of the system services.
#This file overrides defaults set in /etc/security/limits.conf

* soft nofile 4096
root soft nofile 4096
EMBEDEOF
FILES_TO_FACTORY+=("/etc/security/limits.d/30-brew-limits.conf")

# Write tmpfile to restore runtime state
writefile /usr/lib/tmpfiles.d/homebrew.conf <<EOF
C /var/home/linuxbrew 0755 1000 1000 -
$(
    for file in "${FILES_TO_FACTORY[@]}"; do
        [[ $file =~ ^/var/home ]] && continue
        printf -- 'C %s - - - -\n' "$file"
    done
)
EOF

# Copy files to /usr/share/factory
mkdir -p /usr/share/factory
cp --parents -ar -- "${FILES_TO_FACTORY[@]}" /usr/share/factory

#endregion Body
