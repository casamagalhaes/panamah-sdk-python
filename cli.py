#!/usr/bin/env python
import argparse
import json
from os import path, chdir
import unittest
import json

parser = argparse.ArgumentParser(description='Setup')
parser.set_defaults(which='all')

subparsers = parser.add_subparsers(help='commands')

test = subparsers.add_parser('test', help='test help')
test.set_defaults(which='test')

install = subparsers.add_parser('install', help='install help')
install.set_defaults(which='install')

args = parser.parse_args()

if args.which == 'test':
    tests = unittest.TestLoader().discover('.')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if not result.wasSuccessful():
        exit(1)

if args.which == 'install':
    install_requires = []
    tests_require = []

    with open('Pipfile.lock') as fd:
        lock_data = json.load(fd)
        install_requires = [
            package_name + package_data['version']
            for package_name, package_data in lock_data['default'].items()
        ]
        tests_require = [
            package_name + package_data['version']
            for package_name, package_data in lock_data['develop'].items()
        ]

        # print(install_requires)
        # print(tests_require)

exit(0)
