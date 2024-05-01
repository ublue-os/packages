# shellcheck shell=sh disable=SC1091
if test "$(id -u)" -gt "0"; then
  blue=$(printf '\033[38;5;32m')
  bold=$(printf '\033[1m')
  normal=$(printf '\033[0m')
  if test ! -f /etc/linuxbrew.firstrun; then
    printf "\nBluefin-CLI First Run Setup\n\n"
    printf "Setting up sudo for %s%s%s%s...\t\t\t " "$bold" "$blue" "$USER" "$normal"
    echo "#$(id -u) ALL = (root) NOPASSWD:ALL" | sudo tee -a /etc/sudoers > /dev/null
    printf "%s[ OK ]%s\n" "${blue}" "${normal}"
  fi

  if test ! -d /home/linuxbrew/.linuxbrew; then
    name="$(hostname -s)"
    linuxbrew_home="${XDG_DATA_HOME:-$HOME/.local/share}"/bluefin-cli/"${name}"
    printf "Setting up Linuxbrew...\t\t\t\t "
    if test ! -d "${linuxbrew_home}"; then
      mkdir -p "${linuxbrew_home}"
      if test -d "${XDG_DATA_HOME:-$HOME/.local/share}"/bluefin-cli/.linuxbrew; then
        mv "${XDG_DATA_HOME:-$HOME/.local/share}"/bluefin-cli/.linuxbrew "${linuxbrew_home}"/.linuxbrew
      fi
    fi
    if test ! -d /home/linuxbrew; then
      sudo mkdir -p /home/linuxbrew
    fi
    sudo mount --bind "${linuxbrew_home}" /home/linuxbrew
    sudo cp -R /home/homebrew/.linuxbrew /home/linuxbrew/
    sudo chown -R "$(id -u)" /home/linuxbrew
    unset linuxbrew_home
    printf "%s[ OK ]%s\n" "${blue}" "${normal}"
  fi

  if test ! -d /usr/local/share/bash-completion/completions; then
    printf "Setting up Tab-Completions...\t\t\t "
    sudo mkdir -p /usr/local/share/bash-completion
    sudo mount --bind /run/host/usr/share/bash-completion /usr/local/share/bash-completion
    if test -x /run/host/usr/bin/ujust; then
      sudo ln -fs /usr/bin/distrobox-host-exec /usr/local/bin/ujust
    fi
    printf "%s[ OK ]%s\n" "${blue}" "${normal}"
  fi

  if test ! -f /etc/linuxbrew.firstrun; then
    # Remove local repository added at buildtime
    sudo sed -zi "s|\./packages\n||" /etc/apk/repositories
    sudo touch /etc/linuxbrew.firstrun
    printf "\nBluefin-CLI first run complete!\n\n"
  fi
fi
