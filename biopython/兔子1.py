#!/usr/bin/python
n = 96; k = 19;
f = [0 for i in range(n+1)]
f[0] = 1; f[1] = 1; f[2] = 1
for i in range(k-2):
	f[i+3] = f[i+1] +f[i]
for i in range(k+1,n+1):
	for j in range(k-1):
		f[i] += f[i-2-j]
print f
