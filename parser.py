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

    # Case 1: no arguments
    fortilex = fortiparser.FortinetLexicon()
    for line in args.file.readlines():
        fortilex.scan(line)

    # Case 2: argument is configuration only
    # cfg = args.file.read()
    # fortilex = fortiparser.FortinetLexicon(cfg)
    # fortilex.parse_cfg()

    # Case 3: argument is string quote only
    # fortilex = fortiparser.FortinetLexicon('"')
    # for line in args.file.readlines():
    #     fortilex.scan(line)

    # Case 4: arguments are configuration, string quote
    # cfg = args.file.read()
    # fortilex = fortiparser.FortinetLexicon(cfg, '"')
    # fortilex.parse_cfg()

    # Case 5: arguments are string quote, configuration
    # cfg = args.file.read()
    # fortilex = fortiparser.FortinetLexicon('"', cfg)
    # fortilex.parse_cfg()

    # Case 6: no arguments, parse configuration later
    # cfg = args.file.read()
    # fortilex = fortiparser.FortinetLexicon()
    # fortilex.parse_cfg(cfg)

    if args.format == 'dict':
        print(fortilex.get_dict())
    elif args.format == 'json':
        print(fortilex.get_json())
    else:
        print(pprint.pprint(fortilex.get_dict()))

except ValueError as e:
    print(e)
