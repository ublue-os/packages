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

build package="staging/devpod/devpod.spec":
    #!/usr/bin/env bash
    PKGNAME={{package}}
    PKGNAME="${PKGNAME##*/}"
    PKGNAME="${PKGNAME%.*}"
    buildah bud -f Containerfile -t localhost/${PKGNAME}:latest --build-arg TARGET_SPEC={{package}} .

extract package="staging/devpod/devpod.spec" extract_rpm="0":
    #!/usr/bin/env bash
    PKGNAME={{package}}
    PKGNAME="${PKGNAME##*/}"
    PKGNAME="${PKGNAME%.*}"
    rm -rf output
    mkdir -p output
    podman export $(podman create localhost/${PKGNAME}:latest) | tar xf - -C output
    if [ {{extract_rpm}} -ne 1 ] ; then
        exit 0
    fi
    pushd output
    for rpm_file in $(find . -iname "*.rpm"); do
        rpm2cpio "$rpm_file" | cpio -idmv
    done
    popd
