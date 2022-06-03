#!/usr/bin/env python

import sys
import argparse
import fortiparser
import pprint

parser = argparse.ArgumentParser(description='Fortinet Configuration Parser.')
parser.add_argument('file', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
parser.add_argument('--format', dest='format', choices=['dict', 'json', 'text'],
                    default='json',
                    help='output format (default is JSON)')

args = parser.parse_args()

try:
    fortilex = fortiparser.FortinetLexicon()

    for line in args.file.readlines():
        fortilex.scan(line)

    if args.format == 'dict':
        print(fortilex.get_dict())
    elif args.format == 'json':
        print(fortilex.get_json())
    else:
        print(pprint.pprint(fortilex.get_dict()))

except ValueError as e:
    print(e)
