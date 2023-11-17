#!/bin/python3
import argparse
import io
import sys


# Arguments parsing
parser = argparse.ArgumentParser(
    description="A simple python script that transforms a png into a thumbnail for Prusa GCode"
)
parser.add_argument('-m', '--merge', action='store_true',
                    help="If this flag is set, the generated thumbnail will be inserted into existing gcode" +\
                        "file passed as output, replacing existing thumbnail data if present.")
parser.add_argument('-s', '--size', nargs='?', default='220*124',
                    help="SIZE: '<int>*<int>' - Specifies the size of the generated thumbnail, 220*124 by default")
parser.add_argument('input', type=argparse.FileType('rb'),
                    help="Input .png file")
parser.add_argument('output', nargs='?', type=argparse.FileType('w'), default=sys.stdout,
                    help="Destination of generated thumnail, stdout by default.")

args = parser.parse_args()
input_file: io.BufferedReader = args.input
output_file: io.TextIOWrapper = args.output
merge: bool = args.merge
if merge:
    if output_file.name == '<stdout>':
        raise SyntaxError("Output must be specified to use --merge")
    output_file = open(output_file.name, '+w')
    if not output_file.readable():
        raise IOError("Output should be readable to use --merge")
try:
    size: tuple = tuple(int(dim) for dim in args.size.strip().split('*'))
    if len(size) != 2:
        raise SyntaxError
except:
    raise SyntaxError(f"SIZE should be of format '<int>*<int>', found '{args.size}'")
