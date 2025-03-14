#!/bin/bash
set -eo pipefail

PATH="/usr/bin:/sbin:$PATH"

dev="$(findfs "$1")"
while read -r _what _; do
    [[ $_what =~ ^#.* ]] && continue
    [[ $(findfs $"$_what") == "$dev" ]] && { echo "yes"; exit 0; }
done </etc/fstab
echo "no" && exit 0
