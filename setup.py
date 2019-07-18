#!/usr/bin/env python
import argparse
import json
from os import path, chdir
import unittest

parser = argparse.ArgumentParser(description='Setup')
parser.set_defaults(which='all')

subparsers = parser.add_subparsers(help='commands')

test = subparsers.add_parser('test', help='test help')
test.set_defaults(which='test')

args = parser.parse_args()

if args.which == 'test':
    tests = unittest.TestLoader().discover('.')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        exit(0)
    exit(1)

exit(0)
