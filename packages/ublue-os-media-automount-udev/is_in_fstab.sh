#!/bin/bash

PATH="/usr/bin:/sbin:$PATH"

_respond() {
    local -i v=${1:?}
    echo "UBLUEOS_PART_IS_IN_FSTAB=$v"
    exit 0
}

dev="$(findfs "${1:?}")"
while read -r _what _; do
    [[ $_what =~ ^#.* ]] && continue
    [[ $(findfs $"$_what") == "$dev" ]] && _respond 1
done </etc/fstab
_respond 0
