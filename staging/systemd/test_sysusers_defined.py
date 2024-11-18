#!/usr/bin/python

import sys

def parse_sysusers_file(filename):
    users, groups = set(), set()

    for line in open(filename):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        words = line.split()
        match words[0]:
            case 'u'|'u!':
                users.add(words[1])
            case 'g':
                groups.add(words[1])
            case 'm'|'r':
                continue
            case _:
                assert False
    return users, groups

setup_users, setup_groups = parse_sysusers_file(sys.argv[1])
setup_users2, setup_groups2 = parse_sysusers_file(sys.argv[2])
setup_users |= setup_users2
setup_groups |= setup_groups2

basic_users, basic_groups = parse_sysusers_file(sys.argv[3])

if d := basic_users - setup_users:
    exit(f'We have new users: {d}')
if d := basic_groups - setup_groups:
    exit(f'We have new groups: {d}')
