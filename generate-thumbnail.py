#!/bin/python3
import argparse

# Arguments parsing
parser = argparse.ArgumentParser(
    description="A simple python script that transforms a png into a thumbnail for Prusa GCode"
)
parser.add_argument('-m', '--merge', action='store_true')
parser.add_argument('-r', '--resize', nargs='?', default='220x124')
parser.add_argument('input', nargs='?', type=argparse.FileType('r'))
parser.add_argument('output', nargs='?', type=argparse.FileType('w'))
args = parser.parse_args()
