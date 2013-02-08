#!/usr/bin/env python

import sys

INFILE = sys.argv[1]
OUTFILE = sys.argv[2]

nbe = file(INFILE).read()
nbe = nbe.replace('\r', '')
nbe = nbe.replace('\\r', '')
nbe = nbe.replace('\\n', ' ')
nbe = nbe.replace('|||', '|')
nbe = nbe.replace('||', '|')
nbe = nbe.replace('  ', ' ')

fd = open(OUTFILE, 'w')
fd.write(nbe)
fd.close()

