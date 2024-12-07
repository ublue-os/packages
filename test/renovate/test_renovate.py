#!/usr/bin/python3

import os
import re
import sys
import subprocess
from pathlib import Path
import json

TEST_CASES = {
    "kf6-kio": {
       "path": "staging/kf6-kio/kf6-kio.spec",
       "match": r"%global majmin_ver_kf6 6\.\d+",
       "replace": "%global majmin_ver_kf6 6.7"
    },
    "fwupd": {
       "path": "staging/fwupd/fwupd.spec",
       "match": r"Version:   1.\d+\.\d+",
       "replace": r"Version:   1.8.0",
    }
}

OUTPUT_LOG = "renovate-log.ndjson"

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
    os.environ["LOG_LEVEL"] = "debug"
    os.environ["RENOVATE_PLATFORM"] = "local"
    os.environ["RENOVATE_CONFIG_FILE"] = str(Path(".github/renovate.json5").resolve())
    os.environ["RENOVATE_LOG_FILE"] = OUTPUT_LOG

    for test_name, test_case in TEST_CASES.items():
        with open(test_case["path"], 'r+') as file:
            content = file.read()
            new_content = re.sub(test_case["match"], test_case["replace"], content)

            if content == new_content:
                print(f"WARNING: did not replace version in {test_name}")
            file.seek(0)
            file.write(new_content)
            file.truncate()

    subprocess.run("renovate", shell=True)

    found_payload = False
    validated = False
    with open(OUTPUT_LOG, 'r') as file:
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
