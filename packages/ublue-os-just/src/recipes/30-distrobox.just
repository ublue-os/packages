# vim: set ft=make :

alias assemble := distrobox-assemble

# Create distroboxes from a defined manifest
distrobox-assemble CONTAINER="prompt" ACTION="create" FILE="/etc/distrobox/distrobox.ini":
    #!/usr/bin/bash
    # Distroboxes are gathered from distrobox.ini, please add them there
    source /usr/lib/ujust/ujust.sh
    AssembleList {{ FILE }} {{ ACTION }} {{ CONTAINER }}

alias distrobox := distrobox-new

# Create a new custom distrobox
distrobox-new IMAGE="prompt" NAME="prompt" HOMEDIR="":
    #!/usr/bin/bash
    # Please only add distroboxes here if you need special checks and logins!
    source /usr/lib/ujust/ujust.sh
    # Supported images
    IMAGES='
      New
      Steambox
    '
    IMAGE={{ IMAGE }}
    NAME={{ NAME }}
    HOMEDIR={{ HOMEDIR }}
    ARGS=""
    # Ask user to select an image if we need to prompt
    if [ "$IMAGE" == "prompt" ]; then
      echo "Select what container you want to make"
      IMAGE=$(Choose $IMAGES)
    fi
    # If image is "new"
    if [ "${IMAGE,,}" == "new" ]; then
      echo -en "Please enter an image: "
      read IMAGE
      if [ "$NAME" == "prompt" ]; then
        echo -en "Please enter a name for the container: "
        read NAME
      fi
    elif [ -z "${IMAGE,,}" ]; then
      exit 1
    fi
    # Tailored image selection logic
    # Logic for Steambox
    if [ ${IMAGE,,} == "steambox" ]; then
      echo "${b}Creating Steambox distrobox ...${n}"
      if command -v /usr/bin/mutter > /dev/null; then
        IMAGE="ghcr.io/ublue-os/steambox-gnome"
        NAME="steambox"
        ARGS="--unshare-netns"
      else
        IMAGE="ghcr.io/ublue-os/steambox"
        NAME="steambox"
        ARGS="--unshare-netns"
      fi
    # Anything else
    else
      if [ "$NAME" == "prompt" ]; then
        echo -en "Please enter a name for the container: "
        read NAME
      fi
    fi
    # Create the distrobox
    Distrobox "$IMAGE" "$NAME" "$HOMEDIR" $ARGS
    # If IMAGE is steambox, link to documentation
    if [ "${IMAGE,,}" == "steambox" ]; then
      echo $(Urllink "https://github.com/ublue-os/toolboxes#steambox-usage" "Check out the docs for exportable apps and instructions")
    fi

# Install specialized application containers (like brew)
setup-distrobox-app CONTAINER="prompt":
    #!/usr/bin/bash
    source /usr/lib/ujust/ujust.sh
    AssembleList "/etc/distrobox/apps.ini" create {{ CONTAINER }}

# Install/update DaVinci Resolve, a closed-source video editing utility. Options: status | install | uninstall
install-resolve ACTION="":
    #!/usr/bin/bash
    source /usr/lib/ujust/ujust.sh
    set -eo pipefail

    get_status_token() {
      if podman container exists davincibox >/dev/null 2>&1; then
        echo "install"
      else
        echo "uninstall"
      fi
    }

    show_help() {
      echo "Usage: ujust install-resolve <option>"
      echo "  <option>: Specify the quick option to skip the prompt"
      echo "  Use 'status' to print the current portal token"
      echo "  Use 'install' to select Install/upgrade davincibox"
      echo "  Use 'uninstall' to select Uninstall davincibox"
    }

    run_resolve_installer() {
      local runfile="$1"
      local RUNFILE
      tmpdir=/var/tmp/bazzite_davincibox_setup.tmp
      mkdir -p $tmpdir
      trap "rm -rf ${tmpdir}" INT EXIT HUP

      # Download davincibox setup script
      SCRIPT_URL="https://raw.githubusercontent.com/zelikos/davincibox/10b4b82f0e7f121596b33595f584bc576c03bb3a/setup.sh"
      SETUPSCRIPT=/tmp/davincibox_setup.sh
      wget -O $SETUPSCRIPT ${SCRIPT_URL}
      chmod +x $SETUPSCRIPT

      if [[ ! -z $runfile && -f $runfile ]]; then
        if [[ $runfile =~ .zip$ ]]; then
          unzip -o -d "$tmpdir" "$runfile"
          RUNFILE=$(find $tmpdir -executable -name "DaVinci_Resolve_*.run")
        else
          RUNFILE="$runfile"
        fi
        echo "Installer found: ${RUNFILE}"
      else
        echo "${red}Installer not found${n}";
        DOWNLOADDIR=$(xdg-user-dir DOWNLOAD || echo ${HOME})
        echo "${red}Please place the file DaVinci_Resolve_*_Linux.run in ${HOME} or ${DOWNLOADDIR}${n}";
        exit 1
      fi
      bash <<< "env -C ${tmpdir} $SETUPSCRIPT $RUNFILE"
      echo "davincibox was successfully installed"
    }

    install_resolve() {
      DOWNLOADDIR=$(xdg-user-dir DOWNLOAD || echo ${HOME})

      echo "This script requires you to download the DaVinci Resolve installer (should be a zip file) manually from their website and place it in ${HOME} or ${DOWNLOADDIR}"
      echo "https://www.blackmagicdesign.com/event/davinciresolvedownload"
      echo ""
      echo -e "${b}\033[3mDo not\033[0m ${b}extract the .zip contents, the script will handle everything${n}"
      echo "${lightgrey}TIP: For manual installation, see https://github.com/zelikos/davincibox${n}"
      # Get sure user reads instructions
      ugum confirm || exit 0
      # Check if the installer is in HOME or DOWNLOAD
      shopt -s nullglob && possible_installers=({$HOME,$DOWNLOADDIR}/DaVinci_Resolve_{,Studio_}*_Linux.{zip,run}) \
          && shopt -u nullglob
      runfile=$(Choose ${possible_installers[@]})
      run_resolve_installer "$runfile"
    }

    install_resolve_gui() {
      DOWNLOADDIR=$(xdg-user-dir DOWNLOAD || echo ${HOME})
      message="Please select the downloaded ZIP file to be installed"
      download_url="https://www.blackmagicdesign.com/event/davinciresolvedownload"

      while true; do
        set +e
        choice=$(zenity --info \
          --title="DaVinci Resolve Installer" \
          --text="Download the DaVinci Resolve Linux ZIP installer from Blackmagic Design, then continue to select it." \
          --ok-label="Next" \
          --extra-button="Download Installer" 2>/dev/null)
        zenity_status=$?
        set -e
        if [[ "$choice" == "Download Installer" ]]; then
          xdg-open "$download_url" >/dev/null 2>&1 &
        elif (( zenity_status == 0 )); then
          break
        else
          exit 0
        fi
      done

      zenity --info --title="DaVinci Resolve Installer" --text="$message" --ok-label="Select" 2>/dev/null || exit 0
      runfile=$(zenity --file-selection \
        --title="Select DaVinci Resolve installer" \
        --filename="${DOWNLOADDIR}/" \
        --file-filter="DaVinci Resolve Linux installer | *.zip *.run" \
        --file-filter="All files | *" 2>/dev/null) || exit 0

      run_resolve_installer "$runfile"
    }

    cleanup_davincibox_desktop_files() {
      local app_dir desktop_file
      local removed=false
      for app_dir in "$HOME/.local/share/applications" "$HOME/Desktop"; do
        [[ -d "$app_dir" ]] || continue
        while IFS= read -r -d '' desktop_file; do
          if grep -qi "davincibox" "$desktop_file"; then
            rm -f "$desktop_file"
            removed=true
          fi
        done < <(find "$app_dir" -maxdepth 1 -type f -name "*.desktop" -print0 2>/dev/null)
      done
      if [[ "$removed" == "true" ]]; then
        echo "Removed davincibox desktop launchers."
      else
        echo "No davincibox desktop launchers found."
      fi
    }

    uninstall_resolve() {
      # Remove the existing container
      if podman container exists davincibox >/dev/null 2>&1; then
        echo "Removing existing davincibox container"
        distrobox enter davincibox -- add-davinci-launcher remove || true
        podman stop davincibox
        podman rm davincibox
        cleanup_davincibox_desktop_files
      else
        echo "davincibox is not installed, checking for stale desktop launchers..."
        cleanup_davincibox_desktop_files
        exit 0
      fi
    }

    OPTION="{{ ACTION }}"
    case "${OPTION,,}" in
      help)
        show_help
        exit 0
        ;;
      status)
        get_status_token
        exit 0
        ;;
      install|install/upgrade*)
        install_resolve_gui
        exit 0
        ;;
      uninstall*)
        uninstall_resolve
        exit 0
        ;;
      "")
        # Display install state and show options
        INSTALL_STATE=0
        INSTALL_STATE=$(podman container exists davincibox; echo $?)
        if (( $INSTALL_STATE == 0 )); then
          echo "Installed?: ${green}yes${n}"
        else
          echo "Installed?: ${red}no${n}"
        fi
        OPTION=$(Choose \
          "Install/upgrade davincibox" \
          "Uninstall davincibox" \
        )
        if [[ "${OPTION,,}" =~ (^install/upgrade[[:space:]]davincibox) ]]; then
            install_resolve
        elif [[ "${OPTION,,}" =~ (^uninstall[[:space:]]davincibox) ]]; then
            ugum confirm "Confirm davincibox uninstall?" || exit 0
            uninstall_resolve
        fi
        ;;
      *)
        echo "Incorrect option"
        exit 1
        ;;
    esac

alias install-resolve-studio := install-resolve
alias install-davinci := install-resolve
alias install-davinci-resolve := install-resolve
