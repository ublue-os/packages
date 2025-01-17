# Install JetBrains Toolbox | https://www.jetbrains.com/toolbox-app/
[group('Apps')]
install-jetbrains-toolbox:
    #!/usr/bin/env bash
    pushd "$(mktemp -d)"
    echo "Get latest JetBrains Toolbox version"
    # Get the json with latest releases
    curl -sSfL -o releases.json "https://data.services.jetbrains.com/products/releases?code=TBA&latest=true&type=release"
    # Extract information
    BUILD_VERSION=$(jq -r '.TBA[0].build' ./releases.json)
    DOWNLOAD_LINK=$(jq -r '.TBA[0].downloads.linux.link' ./releases.json)
    CHECKSUM_LINK=$(jq -r '.TBA[0].downloads.linux.checksumLink' ./releases.json)
    echo "Installing JetBrains Toolbox ${BUILD_VERSION}"
    curl -sSfL -O "${DOWNLOAD_LINK}"
    curl -sSfL "${CHECKSUM_LINK}" | sha256sum -c
    tar zxf jetbrains-toolbox-"${BUILD_VERSION}".tar.gz
    echo "Launching JetBrains Toolbox"
    ./jetbrains-toolbox-"${BUILD_VERSION}"/jetbrains-toolbox

# Set up command-not-found for Homebrew
[group('Apps')]
setup-brew-not-found ACTION="":
    #!/usr/bin/env bash
    source /usr/lib/ujust/ujust.sh

    OPTION={{ ACTION }}
    if [ "$OPTION" == "help" ]; then
        echo "Usage: ujust setup-brew-not-found <option>"
        echo "  <option>: Specify the quick option to skip the prompt"
        echo "  Use 'enable' to select Enable Brew Not Found"
        echo "  Use 'disable' to select Disable Brew Not Found"
        exit 0
    elif [ "$OPTION" == "" ]; then
        echo "${bold}Brew command-not-found Setup${normal}"
        OPTION=$(Choose "Enable Brew command-not-found" "Disable Brew command-not-found")
    fi

    set -euo pipefail

    BREW_BINARY=/home/linuxbrew/.linuxbrew/bin/brew
    HOMEBREW_REPOSITORY=${HOMEBREW_REPOSITORY:-$($BREW_BINARY --repository)}
    if ! $BREW_BINARY -h > /dev/null; then
      echo "Make sure Homebrew is installed first. Check journalctl -e -u brew-setup.service"
      exit
    fi

    if [[ "${OPTION,,}" =~ ^enable ]]; then
        $BREW_BINARY tap homebrew/command-not-found
        pkexec tee /etc/profile.d/brew-command-not-found.sh > /dev/null <<EOF
    # Check for interactive bash or zsh and that we haven't already been sourced
    if [[ -d /home/linuxbrew/.linuxbrew && \$- == *i* && BREW_COMMAND_NOT_FOUND != 1 ]] ; then
      HB_CNF_HANDLER="${HOMEBREW_REPOSITORY}/Library/Taps/homebrew/homebrew-command-not-found/handler.sh"
      [ -f "\$HB_CNF_HANDLER" ] && source "\$HB_CNF_HANDLER"
      export BREW_COMMAND_NOT_FOUND=1
    fi
    EOF
        # Necessary for fish since just having a script sourcing it does not work
        pkexec ln -sf "${HOMEBREW_REPOSITORY}/Library/Taps/homebrew/homebrew-command-not-found/handler.fish" /etc/fish/conf.d/brew-cnf-handler.fish
        echo "Brew command-not-found has been ${b}${green}enabled${n}"
    fi

    if [[ "${OPTION,,}" =~ ^disable ]]; then
        $BREW_BINARY untap homebrew/command-not-found
        FILES_TO_BE_REMOVED=()
        [ -f /etc/profile.d/brew-command-not-found.sh ] && FILES_TO_BE_REMOVED+=("/etc/profile.d/brew-command-not-found.sh")
        [ -f /etc/fish/conf.d/brew-command-not-found.fish ] && FILES_TO_BE_REMOVED+=("/etc/fish/conf.d/brew-command-not-found.fish")
        pkexec rm -f "${FILES_TO_BE_REMOVED[@]}"
      echo "Brew command-not-found has been ${b}${red}disabled${n}"
    fi
