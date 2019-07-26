#!/usr/bin/env python
import argparse
import json
import subprocess
from os import path, chdir
import unittest
import json

parser = argparse.ArgumentParser(description='CLI')
parser.set_defaults(which='all')

subparsers = parser.add_subparsers(help='commands')

subcommand = subparsers.add_parser('test', help='test help')
subcommand.set_defaults(which='test')
subcommand = subparsers.add_parser('build', help='build help')
subcommand.set_defaults(which='build')
subcommand = subparsers.add_parser('deploy-test', help='deploy-test help')
subcommand.set_defaults(which='deploy-test')

args = parser.parse_args()

if args.which == 'test':
    tests = unittest.TestLoader().discover('.')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if not result.wasSuccessful():
        exit(1)

if args.which == 'build':
    subprocess.check_call(['rm', '-rf', 'dist'])
    subprocess.check_call(['python', 'setup.py', 'sdist', 'bdist_wheel'])

if args.which == 'deploy-test':
    subprocess.check_call(['python', 'cli.py', 'build'])
    subprocess.check_call(['python', '-m', 'pip', 'install', '--upgrade', 'twine'])
    subprocess.check_call(['python', '-m', 'twine', 'upload', '--repository-url', 'https://test.pypi.org/legacy/', 'dist/*'])

exit(0)
