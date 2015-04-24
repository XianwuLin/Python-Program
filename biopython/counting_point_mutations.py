#!/usr/bin/python
f = open("rosalind_hamm.txt","r")
array = f.readlines()

string_a = array[0]
string_b = array[1]

distance = 0
for i in range(len(string_a)):
	if string_a[i] != string_b[i]:
		distance += 1

print distance
