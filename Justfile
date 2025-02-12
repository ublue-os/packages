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
    mkdir -p mock
    # Passes your user to the container and adds it to the mock group else rpkg will not be able to recognize local changes
    # Mock also needs to be called unprivileged apparently
    sudo podman run --privileged --rm -it \
        -v /var/lib/containers:/var/lib/containers:z \
        -v ./mock:/var/lib/mock:Z \
        -v .:/tmp/sources:Z \
        -w /tmp/sources \
        --user "$(id -u):$(id -g)" \
        -e PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin,HOME=/tmp \
        --group-entry "mock:x:135:$(id -nu)" \
        $mock_image \
        $spec {{ MOCK_ARGS }}
