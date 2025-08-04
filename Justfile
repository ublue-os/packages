export mock_image := env("MOCK_IMAGE", "ghcr.io/ublue-os/ublue-builder:latest")
export extensions_dir := env("SYSTEMD_EXTENSIONS_DIR", "/var/lib/extensions")
export overlay_dir := env("OVERLAY_DIR", "overlays")

# Run renovate locally to test modules
renovate dry-run="lookup" log-level="debug":
    #!/usr/bin/env bash
    if ! command -v "renovate" &> /dev/null ; then
        echo "You need to install renovate first"
        echo "It should be available on brew and on npm."
        exit 1
    fi
    if [ "$GITHUB_COM_TOKEN" == "" ] ; then
        echo "Warning: No Github token found, renovate will nag at you for this."
        echo "Set it with GITHUB_COM_TOKEN=(your token)"
    fi
    LOG_LEVEL=${LOG_LEVEL:-debug} renovate --platform=local --dry-run={{ dry-run }}
    echo "Updates can be found in a section of the logs called \"packageFiles with updates\""

build $spec *MOCK_ARGS:
    #!/usr/bin/env bash
    set -x
    mkdir -p mock
    # Passes your user to the container and adds it to the mock group else rpkg will not be able to recognize local changes
    # Mock also needs to be called unprivileged apparently
    CONTAINERS_DIR="${CONTAINERS_DIR:-/var/lib/containers}"
    MOCK_DIR="${MOCK_DIRECTORY:-./mock}"
    SOURCES_DIR="${SOURCES_DIR:-.}"
    sudo podman run --privileged --rm -i \
        --pull "newer" \
        -v "$CONTAINERS_DIR:/var/lib/containers:z" \
        -v "$MOCK_DIR:/var/lib/mock:Z" \
        -v "$SOURCES_DIR:/tmp/sources:Z" \
        -w /tmp/sources \
        --user "$(id -u):$(id -g)" \
        -e PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin,HOME=/tmp \
        -e MOCK_COPRS=$MOCK_COPRS \
        --group-entry "mock:x:135:$(id -nu)" \
        $mock_image \
        $spec {{ MOCK_ARGS }}

generate-homebrew-tarball $OUTDIR="./brew-out" $TARBALL_FILENAME="homebrew.tar.zst":
    #!/usr/bin/env bash

    set -x

    mkdir -p $OUTDIR

    podman run --rm -it \
        -v "$OUTDIR:/outdir:Z" \
        cgr.dev/chainguard/wolfi-base:latest \
        /bin/sh -c "
        set -o xtrace
        apk add curl git zstd posix-libc-utils uutils gnutar grep
        curl --retry 3 -Lo /tmp/brew-install https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh
        chmod +x /tmp/brew-install
        touch /.dockerenv
        ln -s /bin/bash /usr/bin/bash
        ls -s /usr/bin/grep /bin/grep
        env --ignore-environment PATH=/usr/bin:/bin:/usr/sbin:/sbin HOME=/home/linuxbrew NONINTERACTIVE=1 /usr/bin/bash /tmp/brew-install
        tar --zstd -cvf /outdir/{{ TARBALL_FILENAME }} /home/linuxbrew/.linuxbrew"

alias add-overlay := overlay

overlay $TARGET_RPM $REFRESH="0" $CLEAN_ROOTFS="1":
    #!/usr/bin/env bash
    set -xeuo pipefail

    if [ ! -s "${TARGET_RPM}" ] ; then
        echo "Target RPM is not a valid file"
        exit 1
    fi

    mkdir -p "{{ overlay_dir }}"
    BASENAME_RPM="$(basename "$TARGET_RPM")"
    NAME_TRIMMED="${BASENAME_RPM%.*}"

    if [ -s "{{ overlay_dir }}/${NAME_TRIMMED}.raw" ] && [ "$REFRESH" == "0" ] ; then
        sudo mkdir -p {{ extensions_dir }}
        sudo cp -f "{{ overlay_dir }}/${NAME_TRIMMED}.raw" "{{ extensions_dir }}/${NAME_TRIMMED}.raw"
        sudo systemd-sysext refresh
        exit 0
    fi 

    ROOTFS_DIRECTORY="$(mktemp -d --tmpdir="{{ overlay_dir }}")"
    echo "➡️ Setting up extension config file"
    sudo install -d -m0755 "$ROOTFS_DIRECTORY/usr/lib/extension-release.d"
    {
    echo "ID=\"_any\""
    # Post process architecture to match systemd architecture list
    arch="$(echo $(arch) | sed 's/_/-/g')"
    echo "ARCHITECTURE=\"${arch}\""
    } | sudo tee "${ROOTFS_DIRECTORY}/usr/lib/extension-release.d/extension-release.${NAME_TRIMMED}" > /dev/null

    rpm2cpio "$TARGET_RPM" | sudo cpio -idmv -D "${ROOTFS_DIRECTORY}" &> /dev/null

    if [ -d "${ROOTFS_DIRECTORY}/etc" ] ; then
        echo "➡️ Moving /etc to /usr/etc"
        sudo mv --no-clobber --no-copy "${ROOTFS_DIRECTORY}/etc" "${ROOTFS_DIRECTORY}/usr/etc"
    fi

    for dir in "var" "run"; do
        if [ -d "${ROOTFS_DIRECTORY}"/"${dir}" ] ; then
            echo "➡️ Removing ${dir} from rootfs"
            sudo rm -r "${ROOTFS}/${dir}"
        fi
    done

    filecontexts="/etc/selinux/targeted/contexts/files/file_contexts"
    echo "🏷️ Resetting SELinux labels"
    sudo setfiles -r "${ROOTFS_DIRECTORY}" "${filecontexts}" "${ROOTFS_DIRECTORY}"
    sudo chcon --user=system_u --recursive "${ROOTFS_DIRECTORY}"

    # Then create erofs
    mkfs.erofs "{{ overlay_dir }}/${NAME_TRIMMED}.raw" "${ROOTFS_DIRECTORY}"
    [ "$CLEAN_ROOTFS" == "1" ] && sudo rm -rf "${ROOTFS_DIRECTORY}"
    sudo mkdir -p {{ extensions_dir }}
    sudo cp -f "{{ overlay_dir }}/${NAME_TRIMMED}.raw" "{{ extensions_dir }}/${NAME_TRIMMED}.raw"
    sudo systemd-sysext refresh

remove-overlay $TARGET_RPM:
    #!/usr/bin/env bash

    set -euo pipefail

    BASENAME_RPM="$(basename "$TARGET_RPM")"
    NAME_TRIMMED="${BASENAME_RPM%.*}"
    sudo rm -f "{{ extensions_dir }}/${NAME_TRIMMED}.raw"
    sudo systemd-sysext refresh

clean:
    #!/usr/bin/env bash
    for line in $(cat .gitignore | xargs) ; do
        sudo rm -ri $line
    done
    exit 0

# Check Just Syntax

just := just_executable()

[group('Just')]
check:
    #!/usr/bin/bash
    find . -type f -name "*.just" | while read -r file; do
      echo "Checking syntax: $file"
      {{ just }} --unstable --fmt --check -f $file
    done
    echo "Checking syntax: Justfile"
    {{ just }} --unstable --fmt --check -f Justfile
