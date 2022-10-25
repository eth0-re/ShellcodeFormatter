import argparse
from io import BufferedReader, TextIOWrapper, BytesIO
import sys
import binascii
import os.path

class ShellcodeDefinition:
    def __init__(self, name, overall_format, byte_format, line_format):
        self.name = name
        self.overall_format = overall_format
        self.byte_format = byte_format
        self.line_format = line_format



def main(args):
    
    raw_shellcode:BytesIO = args.infile.read()

    hex = binascii.hexlify(raw_shellcode)


    # Different formats
    # csharp:               byte[] buf = new byte[460] { 0x01, 0xab, 0x34, 0xcd }
    #
    #   - overall format:   byte[] buf = new byte[ ^^BYTE_COUNT^^ ] { ^^LINES^^ }
    #   - byte format:      0x01, 0x02
    #   - line format:      ^^BYTEx16^^



def read_binary_file(path) -> BufferedReader:
    with open(path, 'rb') as f:
        return f.read()

def csharp_definition():
    return ShellcodeDefinition(
        name="csharp", 
        overall_format="byte[] buf = new byte[^^BYTE_COUNT^^] { ^^LINES^^ }", 
        byte_format="0x01, 0x02", 
        line_format="^^BYTEx16^^")

def transform_shellcode(shellcode:BytesIO, definition:ShellcodeDefinition):
    output_text = "";

    # Transform byte format
    



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?', type=argparse.FileType('rb'), default=sys.stdin.buffer)
    parser.add_argument('-f', help='Output format', choices=['hex', 'csharp', 'python', 'c'], required=True)
    parser.add_argument('-o', '--outfile', help='Output file')

    args = parser.parse_args()
    main(args)