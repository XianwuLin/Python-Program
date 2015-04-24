# -*- coding: utf-8 -*-
#!/usr/bin/python
from Bio import SeqIO
from Bio.Seq import Seq
from Bio import AlignIO

handle = open("Overlap.txt")
f_out = open("out.txt","w")
seq_record = SeqIO.parse(handle,"fasta") #读取数据
date = [[j for j in range(0)]for i in range(2)]

for i in seq_record:
	date[0].append(i.id)
	date[1].append(str(i.seq))

for i in range(len(date[0])):
	for j in range(len(date[0])):
		if date[0][i] != date[0][j]:  #确保不与自己比较
			if not cmp(str(date[1][i])[-3:], str(date[1][j])[0:3]): #数据比较
				temp = date[0][i] + " " + date[0][j] + "\n"
				f_out.write(temp)
handle.close()
f_out.close()
