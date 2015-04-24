# -*- coding: utf-8 -*-
#!/usr/bin/python
from Bio import SeqIO
from Bio.Seq import Seq
f = open("temp.txt","r")

sum_line = []
for seq_re in SeqIO.parse(f,"fasta"):  #导入数据到数组字符串
	sum_line.append(seq_re.seq)
f.close()
len_line = len(sum_line[0])  #Seq序列长度

trans_line = ['' for i in range(len_line)]  #生成转置的字符串数组

temp = -1
for i in trans_line:  #转置字符串数组
	temp += 1
	for j in sum_line:
		trans_line[temp] += j[temp:temp + 1]
	trans_line[temp] = Seq(str(trans_line[temp]))  #将字符串数组转化为Seq序列 

date_out = [[0 for column in range(len_line)] for row in range(4)]
string_out = ""

for i in range(len_line): 
	date_out[0][i] = trans_line[i].count("A")
	date_out[1][i] = trans_line[i].count("C")
	date_out[2][i] = trans_line[i].count("G")
	date_out[3][i] = trans_line[i].count("T")
	temp = max(date_out[0][i],date_out[1][i],date_out[2][i],date_out[3][i])
	if temp == date_out[0][i]:
		string_out += "A"
	elif temp == date_out[1][i]:
		string_out += "C"
	elif temp == date_out[2][i]:
		string_out += "G"
	else:
		string_out += "T"

f = open("out.txt", 'w')
f.write(string_out)
f.write("\n")
date_a_out = ["A","C","G","T"]
for i in range(4):
	f.write(date_a_out[i])
	f.write(":")
	for j in range(len_line):
		f.write(" ")
		f.write(str(date_out[i][j]))
	f.write("\n")
f.close()
