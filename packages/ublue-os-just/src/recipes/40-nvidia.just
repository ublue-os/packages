# vim: set ft=make :

# Switch between Nvidia image and NVK
toggle-nvk:
    #!/usr/bin/bash
    CURRENT_IMAGE=$(rpm-ostree status -b --json | jq -r '.deployments[0]."container-image-reference"' | sed -E 's/^.+\/(.+:.+)$/\1/')
    CURRENT_URI=$(rpm-ostree status -b --json | jq -r '.deployments[0]."container-image-reference"' | sed -E 's/^(.+\/).+:.+$/\1/')
    NEW_IMAGE=$CURRENT_IMAGE
    if [[ "$CURRENT_IMAGE" =~ "nvidia-open" ]]; then
      NEW_IMAGE=${CURRENT_IMAGE/-nvidia-open/}
    elif [[ "$CURRENT_IMAGE" =~ "nvidia" ]]; then
      NEW_IMAGE=${CURRENT_IMAGE/-nvidia/}
    else
      # Returns true for legacy NVIDIA hardware (older than Turing) using die names
      # GK### (Kepler), GM### (Maxwell), GP### (Pascal), GV### (Volta)
      if lspci -nn | grep -P "(VGA compatible|3D) controller .+G(K|M|P|V)\d{3}" > /dev/null; then
        NEW_IMAGE=${CURRENT_IMAGE/:/-nvidia:}
      else
        NEW_IMAGE=${CURRENT_IMAGE/:/-nvidia-open:}
      fi
    fi
    echo "Rebasing to ${NEW_IMAGE}"
    rpm-ostree rebase ${CURRENT_URI}${NEW_IMAGE}
