#!/usr/bin/python
from Bio import SeqIO
f = open('temp.txt', 'w')
handle = open("rosalind_gc.txt")
for seq_record in SeqIO.parse(handle,"fasta"):
	f.writelines(seq_record.id + "\n")
	f.writelines(str(float(seq_record.seq.count('G') + seq_record.seq.count('C')) / len(seq_record.seq) * 100) + "\n")
handle.close()
f.close()
