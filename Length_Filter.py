#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

import sys
from Bio import SeqIO

try:
    INPUT_FILE = sys.argv[1]
    OUTPUT_FILE = sys.argv[2]
    LOWER = int(sys.argv[3])
    UPPER = int(sys.argv[4])

except IndexError:
    print "Usage: Length_Filter.py <input fastq file> <output fastq file> <lower length cut-off> <upper length cut-off>"
    raise SystemExit

input_iterator = SeqIO.parse(open(INPUT_FILE), "fastq")

highs = (record for record in input_iterator if len(record.seq) > LOWER)
lows = (record for record in highs if len(record.seq) < UPPER)

#print "There were %i sequences < INPUT bp." % len(keepers)

output_handle = open(OUTPUT_FILE, "w")
SeqIO.write(lows, output_handle, "fastq")
output_handle.close()
