#!/bin/bash
set -eoux pipefail
ARCH=$(uname -m)
while [[ "${JUST_VERSION:-}" =~ null || -z "${JUST_VERSION:-}" ]]
do
    JUST_VERSION=$(curl -L https://api.github.com/repos/casey/just/releases/latest | jq -r '.tag_name')
done
curl -sSLO https://github.com/casey/just/releases/download/"${JUST_VERSION}"/just-"${JUST_VERSION}"-"${ARCH}"-unknown-linux-musl.tar.gz
tar -zxvf just-"${JUST_VERSION}"-"${ARCH}"-unknown-linux-musl.tar.gz -C /tmp just
sudo mv /tmp/just /usr/local/bin/just
rm -f just-"${JUST_VERSION}"-"${ARCH}"-unknown-linux-musl.tar.gz
