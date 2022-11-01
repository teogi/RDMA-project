#!/bin/python
import sys
from argparse import ArgumentParser as Parser

parser = Parser()
parser.add_argument("-b","--bandwidth")
arg = parser.parse_args()

