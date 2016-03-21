#!/usr/bin/env python

__author__ = "Michael C. Nelson"
__copyright__ = "Copyright 2016, Michael C. Nelson/University of Connecticut"
__credits__ = ["Created using demo code from the BioPython tutorial."]
__license__ = "GPL3"
__version__ = "2.0"

import sys
import argparse
import gzip
from Bio import SeqIO

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', required=True, help="The input file to search through. [REQUIRED]", metavar='Input.fastq')
parser.add_argument('-o', '--output', required=True, help="The output fastq to create. [REQUIRED]", metavar='Output.fastq.gz')
parser.add_argument('-l', '--lower', required=True, help="The lower length limit. [REQUIRED]", metavar='240')
parser.add_argument('-u', '--upper', required=True, help="The upper length limit. [REQUIRED]", metavar='260')
args = parser.parse_args()

INPUT_FILE = args.input
OUTPUT_FILE = args.output
LOWER = int(args.lower)
UPPER = int(args.upper)

if INPUT_FILE.endswith('.fastq'):
	input_iterator = SeqIO.parse(open(INPUT_FILE), "fastq")
elif INPUT_FILE.endswith('.fastq.gz'):
	input_iterator = SeqIO.parse(gzip.open(INPUT_FILE), "fastq")

highs = (record for record in input_iterator if len(record.seq) > LOWER)
lows = (record for record in highs if len(record.seq) < UPPER)

output_handle = open(OUTPUT_FILE, "w")
SeqIO.write(lows, output_handle, "fastq")
output_handle.close()

