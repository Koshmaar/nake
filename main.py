import os
import subprocess
import sys
import pathlib
from typing import List


def main():
    #print("Running nake ver 0.0.1")
    if len(sys.argv) < 2:
        print("Not enough params")
        sys.exit(1)

    target = sys.argv[1]
    #print(f"Target: {target}")

    nakefile_path = pathlib.Path('./Nakefile')

    if not nakefile_path.exists():
        print("Nakefile does not exists")
        sys.exit(1)

    if not nakefile_path.is_file():
        print("Nakefile is not file")
        sys.exit(1)

    with open(nakefile_path) as f:
        lines = f.readlines()
        rules = parse_nakefile(lines)

        if target in rules:
            rule = rules[target]
            # print(f"To run: found rule with: {rule}")

            commands = ""
            for command in rule:
                commands += command.strip() + "; "

            call_system(commands)
        else:
            print(f"Didn't found '{target}' in Nakefile.")


def call_system(cmd: str) -> int:
    print(f"> {cmd}")
    cmd = f"/bin/bash -c '{cmd}'"

    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        # print(result.stderr)
        return result.returncode
    return 0


def parse_nakefile(lines: List[str]) -> dict:
    rules = {}
    line_nr = 0

    while line_nr < len(lines):
        line = lines[line_nr]
        if not line.endswith(":\n"):
            line_nr += 1
            continue

        rule_name = line.rstrip(": \n")
        # print(f"found rule: {rule_name}")
        rule = []
        line_nr += 1

        while line_nr < len(lines):
            line = lines[line_nr]
            if len(line.strip()) == 0:
                break
            rule.append(line)
            line_nr += 1
        if len(rule) > 0:
            # print(f"adding rule: {rule}")
            rules[rule_name] = rule

    return rules


if __name__ == '__main__':
    main()
