#!/usr/bin/env python

import argparse
import sys
from io import BytesIO
from ShellcodeFormatter.definitions import ShellcodeDefinitions 
from ShellcodeFormatter.transformer import ShellcodeTransformer


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?', type=argparse.FileType('rb'), default=sys.stdin.buffer)
    parser.add_argument('-f', help='Output format', choices=ShellcodeDefinitions.list_definitions(), required=True, dest='format')
    parser.add_argument('-o', '--outfile', help='Output file')
    args = parser.parse_args()

    raw_shellcode:BytesIO = args.infile.read()
    definition = ShellcodeDefinitions.get_definition(args.format)
    output = ShellcodeTransformer(definition).transform_shellcode(raw_shellcode)
    print(output)


if __name__ == '__main__':

    main()