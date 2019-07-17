#!/usr/bin/env python
import argparse
import json
from os import path

parser = argparse.ArgumentParser(description='Setup')
parser.set_defaults(which='all')

subparsers = parser.add_subparsers(help='commands')

install = subparsers.add_parser('install', help='install help')
install.set_defaults(which='install')

args = parser.parse_args()

print(args)