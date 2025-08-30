#!/usr/bin/env python3

import fnmatch
import functools
import json
import os
import subprocess
from typing import Any

FS_MAPPINGS = {
    "ext4": "defaults,noatime,errors=remount-ro,nofail,rw,users,exec,x-gvfs-show",
    "btrfs": "defaults,noatime,lazytime,commit=120,discard=async,compress-force=zstd:1,space_cache=v2,nofail,rw,users,exec,x-gvfs-show",
}
""" Key: FSTYPE; Value: FSOPTIONS """


@functools.cache
def partuuids_in_fstab() -> set[str]:
    partuuids: set[str] = set()

    cmd_out = subprocess.check_output(
        ["findmnt", "-s", "--json", "--output=FSTYPE,OPTIONS,PARTUUID"], text=True
    ).strip()
    filesystems: list[Any] = json.loads(cmd_out)["filesystems"]
    for filesystem in filesystems:
        partuuids.add(filesystem["partuuid"])

    return partuuids


def main() -> None:
    # Check we are running as root
    if os.getuid() != 0:
        raise RuntimeError("This script must run as root")

    # Get all the available partition devices
    cmd_out = subprocess.check_output(
        [
            "lsblk",
            "--noheadings",
            "--paths",
            "--list",
            "--output=NAME,FSTYPE,TYPE,HOTPLUG,MOUNTPOINTS,LABEL,PARTLABEL,PARTUUID",
            "--json",
        ],
        text=True,
    ).strip()

    # Read the json output
    blockdevices: list[Any] = json.loads(cmd_out)["blockdevices"]

    # Filter out anything that isnt a partition
    blockdevices = [x for x in blockdevices if x["type"] == "part"]

    def filter_dev(block_dev: dict) -> bool:
        if block_dev["type"] != "part":
            print(f"Skipping {block_dev['name']}: not a partition")
            return False

        if not any(
            [
                fnmatch.fnmatch(block_dev["name"].split("/")[-1], pat)
                for pat in ["sd[a-z][0-9]", "nvme[0-9]n[0-9]p[0-9]"]
            ]
        ):
            print(f"Skipping {block_dev['name']}: not an SSD or NVME device")
            return False

        if block_dev["fstype"] not in FS_MAPPINGS.keys():
            print(
                f"Skipping {block_dev['name']}: unsupported filesystem type '{block_dev['fstype']}'"
            )
            return False

        if block_dev["partuuid"] in partuuids_in_fstab():
            print(f"Skipping {block_dev['name']}: already in fstab")
            return False

        if any(block_dev["mountpoints"]):
            print(
                f"Skipping {block_dev['name']}: already mounted at {block_dev['mountpoints']}"
            )
            return False

        if block_dev["hotplug"]:
            print(f"Skipping {block_dev['name']}: removable device")
            return False

        if not any([block_dev["label"], block_dev["partlabel"]]):
            print(f"Skipping {block_dev['name']}: no label or partlabel")
            return False

        return True

    blockdevices = [x for x in blockdevices if filter_dev(x)]

    # For each blockdevice, mount it
    for dev in blockdevices:
        _cmd = [
            "systemd-mount",
            "--collect",
            "--no-block",
            f"--options={FS_MAPPINGS.get(dev['fstype']) or 'ro,nofail,noauto'}",
            dev["name"],
        ]
        subprocess.check_call(_cmd) if os.getenv("DRY_RUN") != "1" else print(
            "DRY_RUN", _cmd
        )


if __name__ == "__main__":
    main()
