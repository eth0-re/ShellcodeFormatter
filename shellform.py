#!/usr/bin/env python

import argparse
import sys
from io import BytesIO

import transforms.transformer as transformer
import transforms.definitions as definitions



def main(args):
    
    raw_shellcode:BytesIO = args.infile.read()
    definition = definitions.definitions[args.format]
    output = transformer.transform_shellcode(raw_shellcode, definition)

    print(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?', type=argparse.FileType('rb'), default=sys.stdin.buffer)
    
    parser.add_argument('-f', help='Output format', choices=definitions.definitions.keys(), required=True, dest='format')
    parser.add_argument('-o', '--outfile', help='Output file')

    args = parser.parse_args()
    main(args)