#!/usr/bin/python3

import os
import re
import sys
import subprocess
from pathlib import Path
import json

TEST_CASES = {
    "loft-sh/devpod": {
       "path": "staging/devpod/devpod.spec",
       "match": r"Version:        v0.\d+\.\d+",
       "replace": r"Version:        v0.6.0",
    },
    "topgrade-rs/topgrade": {
       "path": "staging/topgrade/topgrade.spec",
       "match": r"Version:        \d+\.\d+\.\d+",
       "replace": "Version:        14.0.0",
    },
    "kf6-kio": {
       "path": "staging/kf6-kio/kf6-kio.spec",
       "match": r"%global majmin_ver_kf6 6\.\d+",
       "replace": "%global majmin_ver_kf6 6.7"
    },
    "fwupd": {
       "path": "staging/fwupd/fwupd.spec",
       "match": r"Version:   1.\d+\.\d+",
       "replace": r"Version:   1.8.0",
    },
    "sched-ext/scx": {
       "path": "staging/scx-scheds/scx-scheds.spec",
       "match": r"Version:        1\.\d+\.\d+",
       "replace": r"Version:   1.0.4",
    },
    "rpm-ostree": {
       "path": "staging/rpm-ostree/rpm-ostree.spec",
       "match": r"Version: 202\d.\d",
       "replace": r"Version:   2024.6",
    },
    "GSConnect/gnome-shell-extension-gsconnect": {
       "path": "staging/gnome-shell-extension-gsconnect/gnome-shell-extension-gsconnect.spec",
       "match": r"Version:\s+\d+",
       "replace": r"Version: 57",
    },
    "ublue-os/uupd": {
       "path": "staging/uupd/uupd.spec",
       "match": r"Version:\s+\d+",
       "replace": r"Version: 0.4",
    }
}


def validate_output(payload):
    packages_with_updates = set()
    for deps in payload:
        for dep in deps["deps"]:
            dep_name = dep["depName"]
            if len(dep["updates"]) > 0:
                packages_with_updates.add(dep_name)

    print("Packages with updates:")
    print(packages_with_updates)

    all_packages_found = True
    for package in TEST_CASES.keys():
        if not package in packages_with_updates:
            print(f"ERROR: did not find update for package {package}")
            all_packages_found = False

    return all_packages_found


def main():
    log_filename = "renovate-log.ndjson"

    os.environ["LOG_LEVEL"] = "debug"
    os.environ["RENOVATE_PLATFORM"] = "local"
    os.environ["RENOVATE_CONFIG_FILE"] = str(Path(".github/renovate.json5").resolve())
    os.environ["RENOVATE_LOG_FILE"] = log_filename

    for test_name, test_case in TEST_CASES.items():
        with open(test_case["path"], 'r+') as file:
            content = file.read()
            new_content = re.sub(test_case["match"], test_case["replace"], content)

            if content == new_content:
                print(f"WARNING: did not replace version in {test_name}")
            file.seek(0)
            file.write(new_content)
            file.truncate()

    subprocess.check_call(["/usr/local/sbin/renovate"], shell=False)

    found_payload = False
    validated = False
    with open(log_filename, 'r') as file:
        for line in file.readlines():
            parsed_line = json.loads(line)
            if "config" in parsed_line and "regex" in parsed_line["config"]:
                found_payload = True
                validated = validate_output(parsed_line["config"]["regex"])

    if not found_payload:
        print(f"WARNING: did not find output from renovate")

    if validated:
        print("passed")
        sys.exit(0)
    else:
        print("failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
