#!/usr/bin/env python
import sys
import os

if len(sys.argv) !=3:
    print ('python %s <input.fa> <output>' % (sys.argv[0]))
    sys.exit()
from Bio import SeqIO
raw, out = sys.argv[1:]
out_h = open(out, 'w')
for seq_record in SeqIO.parse(raw, 'fasta'):
    seq = seq_record.seq.lstrip().rstrip()
    if seq:
        out_h.write('>'+seq_record.id+'\n'+str(seq)+'\n')
    else:
        print(seq_record.id+' has no seq')
out_h.close()

        

    





