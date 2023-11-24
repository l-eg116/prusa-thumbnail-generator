#!/bin/python3
import argparse
import base64
import io
import os
import re
import sys

from PIL import Image


# Arguments parsing
parser = argparse.ArgumentParser(
    description="A simple python script that transforms a png into a thumbnail for Prusa GCode"
)
parser.add_argument('-m', '--merge', action='store_true',
                    help="Set this flag to insert the generated thumbnail into existing gcode " +
                    "file passed as output, replacing existing thumbnail data if present.")
parser.add_argument('-s', '--size', nargs='?', default='220x124',
                    help="SIZE: '<width-int>x<height-int>' or 'keep' - Specifies the size of the generated thumbnail," +
                    "220x124 by default. Use 'keep' to prevent image resizing.")
parser.add_argument('--crop', action='store_true',
                    help="Use this flag to crop input to aspect ratio of output before resizing.")
parser.add_argument('input', type=argparse.FileType('rb'),
                    help="Input .png file")
parser.add_argument('output', nargs='?', type=argparse.FileType('a'), default=sys.stdout,
                    help="Destination of generated thumnail, stdout by default.")

args = parser.parse_args()
input_file_reader: io.BufferedReader = args.input
output_file: io.TextIOWrapper = args.output
merge: bool = args.merge
resize: bool = args.size.lower() != 'keep'
size: tuple = (220, 124)
if resize:
    try:
        size = tuple(int(dim) for dim in args.size.strip().split('x'))
        if len(size) != 2 or size[0] <= 0 or size[1] <= 0:
            raise SyntaxError
    except:
        raise SyntaxError(
            f"SIZE should be of format '<int>x<int>', found '{args.size}'")
crop: bool = args.crop


# Constants & global variables
MAX_THUMBNAIL_LINE_LENGTH: int = 78


# Code
# Image resizing
image = Image.open(input_file_reader)

if resize:

    if crop:
        width, height = image.size
        aspect_ratio_target = size[1] / size[0]
        aspect_ratio_current = height / width
        if aspect_ratio_current > aspect_ratio_target:
            offset = int((height - size[1] * width / size[0]) / 2)
            image = image.crop((0, offset, width, height - offset))
        elif aspect_ratio_current < aspect_ratio_target:
            offset = int((width - size[0] * height / size[1]) / 2)
            image = image.crop((offset, 0, width - offset, height))

    image = image.resize(size)

input_file_reader.close()
input_file = io.BytesIO()
image.save(input_file, format='png')


# Thumbnail generator
thumbnail_str = base64.b64encode(input_file.getvalue()).decode('utf-8')
thumbnail_len = len(thumbnail_str)
thumbnail_str = "; " + "\n; ".join(thumbnail_str[i:i + MAX_THUMBNAIL_LINE_LENGTH]
                                   for i in range(0, len(thumbnail_str), MAX_THUMBNAIL_LINE_LENGTH))
thumbnail_header = f";\n; thumbnail begin {size[0]}x{size[1]} {thumbnail_len}"
thumbnail_footer = f"; thumbnail end\n;"
input_file.close()

# Outputting
if merge:
    if output_file.name == '<stdout>':
        raise SyntaxError("Output must be specified to use --merge")
    output_file = open(output_file.name, 'r', encoding='utf-8')
    if not output_file.readable():
        raise IOError("Output should be readable to use --merge")

    output_data = output_file.read()

    thumbnail_regex = f';\n; thumbnail begin {size[0]}x{size[1]} [0-9]+\n(; .+\n)+; thumbnail end\n;'
    thumbnail_full = '\n'.join((thumbnail_header, thumbnail_str, thumbnail_footer))
    output_data, rep_count = re.subn(thumbnail_regex, thumbnail_full, output_data)

    if rep_count == 0:
        output_data = thumbnail_full + '\n' + output_data

    output_file = open(output_file.name, 'w', encoding='utf-8')
    output_file.write(output_data)
else:
    output_file.write(thumbnail_header + '\n')
    output_file.write(thumbnail_str + '\n')
    output_file.write(thumbnail_footer + '\n')

output_file.close()
