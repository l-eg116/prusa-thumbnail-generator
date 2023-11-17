#!/bin/python3
import argparse
import base64
import io
import os
import sys

from PIL import Image


# Arguments parsing
parser = argparse.ArgumentParser(
    description="A simple python script that transforms a png into a thumbnail for Prusa GCode"
)
parser.add_argument('-m', '--merge', action='store_true',
                    help="If this flag is set, the generated thumbnail will be inserted into existing gcode" +
                    "file passed as output, replacing existing thumbnail data if present.")
parser.add_argument('-s', '--size', nargs='?', default='220x124',
                    help="SIZE: '<int>x<int>' or 'keep' - Specifies the size of the generated thumbnail," +
                    "220x124 by default. Use 'keep' to prevent image resizing.")
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
resize: bool = args.size.lower() != 'keep'
size: tuple = (220, 124)
if resize:
    try:
        size = tuple(int(dim) for dim in args.size.strip().split('x'))
        if len(size) != 2:
            raise SyntaxError
    except:
        raise SyntaxError(
            f"SIZE should be of format '<int>x<int>', found '{args.size}'")


# Constants & global variables
MAX_THUMBNAIL_LINE_LENGTH: int = 78


# Code
# Image resizing
if resize:
    image = Image.open(input_file).resize(size)
    input_file.close()
    input_file = io.BytesIO()  # type: ignore
    image.save(input_file, format='png')
    image.show()

# Thumbnail generator
thumbnail_str = base64.b64encode(input_file.read()).decode('utf-8')
thumbnail_len = len(thumbnail_str)
thumbnail_str = "; " + "\n; ".join(thumbnail_str[i:i + MAX_THUMBNAIL_LINE_LENGTH]
                                   for i in range(0, len(thumbnail_str), MAX_THUMBNAIL_LINE_LENGTH))
thumbnail_header = f"; \n; thumbnail begin {size[0]}x{size[1]} {thumbnail_len}"
thumbnail_footer = f"; \n; thumbnail end"
input_file.close()
