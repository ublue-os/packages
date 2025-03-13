#!/bin/bash
set -eo pipefail

dev="$(findfs "$1")"
while read -r _what _; do
    [[ $_what =~ ^#.* ]] && continue
    [[ $(findfs $"$_what") == "$dev" ]] && { echo "yes"; exit 0; }
done </etc/fstab
echo "no" && exit 1
