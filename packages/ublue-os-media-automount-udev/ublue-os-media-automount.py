#!/usr/bin/env python3

import fnmatch
import functools
import json
import os
import subprocess
from typing import Any

FS_MAPPINGS = {
    "ext4": "defaults,noatime,errors=remount-ro,nofail,rw,users,exec",
    "btrfs": "defaults,noatime,lazytime,commit=120,discard=async,compress-force=zstd:1,space_cache=v2,nofail,rw,users,exec",
}
""" Key: FSTYPE; Value: FSOPTIONS """


def findfs(s: str) -> str:
    return subprocess.check_output(["findfs", s], text=True).strip()


@functools.cache
def devices_in_fstab() -> set[str]:
    devs: set[str] = set()
    with open("/etc/fstab") as f:
        for line in f.readlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            devs.add(findfs(line.split()[0]))
    return devs


def main() -> None:
    # Get all the available partition devices
    cmd_out = subprocess.check_output(
        [
            "lsblk",
            "--noheadings",
            "--paths",
            "--list",
            "--output=NAME,FSTYPE,TYPE,HOTPLUG,MOUNTPOINTS,LABEL,PARTLABEL",
            "--json",
        ],
        text=True,
    ).strip()

    # Read the json output
    blockdevices: list[Any] = json.loads(cmd_out)["blockdevices"]

    # Filter out anything that isnt a partition
    blockdevices = [x for x in blockdevices if x["type"] == "part"]

    # Check if we lacked enough permissions to read fstype
    if not blockdevices or not blockdevices[0]["fstype"]:
        raise RuntimeError("we lack root perms to fetch fstype")

    def filter_dev(block_dev: dict) -> bool:
        _udev_path = "/etc/udev/rules.d/99-media-automount.rules"
        _is_disabled_udev_rule = (
            os.path.exists(_udev_path) and os.path.realpath(_udev_path) == "/dev/null"
        )

        if (
            # Filter out if the device isnt a partition...
            block_dev["type"] != "part"
            # ... or is not an SSD or NVME...
            or not any(
                [
                    fnmatch.fnmatch(block_dev["name"].split("/")[-1], pat)
                    for pat in ["sd[a-z][0-9]", "nvme[0-9]n[0-9]p[0-9]"]
                ]
            )
            # ... or if is not a supported type...
            or block_dev["fstype"] not in FS_MAPPINGS.keys()
            # ... or if is in fstab...
            or block_dev["name"] in devices_in_fstab()
            # ... or if is mounted somewhere else...
            or any(block_dev["mountpoints"])
            # ... or if is removable...
            or block_dev["hotplug"]
            # ... or if does not have label/partlabel...
            or not any([block_dev["label"], block_dev["partlabel"]])
            # ... or if the udev rule disabling automounting exists
            or _is_disabled_udev_rule
        ):
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
