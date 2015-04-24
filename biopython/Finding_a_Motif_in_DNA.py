#!/usr/bin/python
f = open("temp.txt")
f_out = open("out.txt", 'w')
seq_1 = f.readline(); seq_1 = seq_1[0:-1]
seq_2 = f.readline(); seq_2 = seq_2[0:-1]
#print len(seq_2)
f.close()

seq_len = len(seq_2)
temp = 0

for i in range(0, len(seq_1)-len(seq_2)):
	temp +=1
	if not cmp(seq_1[i:seq_len + i], seq_2):
		f_out.write(str(temp) + " ")

f_out.close()
#	else:
#		print i,"*****",
#		print seq_1[i:seq_len + i] , "*****" , seq_2
