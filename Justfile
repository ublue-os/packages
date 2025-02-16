export mock_image := env("MOCK_IMAGE", "ghcr.io/ublue-os/ublue-builder:latest")

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
    LOG_LEVEL=${LOG_LEVEL:-debug} renovate --platform=local --dry-run={{dry-run}}
    echo "Updates can be found in a section of the logs called \"packageFiles with updates\""

build $spec *MOCK_ARGS:
    #!/usr/bin/env bash
    set -x
    mkdir -p mock
    # Passes your user to the container and adds it to the mock group else rpkg will not be able to recognize local changes
    # Mock also needs to be called unprivileged apparently
    CONTAINERS_DIR="${CONTAINERS_DIR:-/var/lib/containers}"
    MOCK_DIR="${MOCK_DIRECTORY:-./mock}"
    sudo podman run --privileged --rm -it \
        -v "$CONTAINERS_DIR:/var/lib/containers:z" \
        -v "$MOCK_DIR:/var/lib/mock:Z" \
        -v .:/tmp/sources:Z \
        -w /tmp/sources \
        --user "$(id -u):$(id -g)" \
        -e PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin,HOME=/tmp \
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
        apk add curl git zstd posix-libc-utils uutils
        curl --retry 3 -Lo /tmp/brew-install https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh
        chmod +x /tmp/brew-install
        touch /.dockerenv
        ln -s /bin/bash /usr/bin/bash
        env --ignore-environment PATH=/usr/bin:/bin:/usr/sbin:/sbin HOME=/home/linuxbrew NONINTERACTIVE=1 /usr/bin/bash /tmp/brew-install
        tar -cvf /dev/stdout /home/linuxbrew | zstd -v -T0 -10 -f -o /outdir/{{ TARBALL_FILENAME }}"
