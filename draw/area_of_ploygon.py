#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   Victor Lin
#   E-mail  :   linxianwusx@gmail.com
#   Date    :   14/12/04 13:22:48
#

def polyArea1(pts): #定积分
	s=0
	_len=len(pts)
	x,y=zip(*pts)
	j=_len-1
	for i in range(_len):
		s = s + (y[i]+y[j])*(x[i]-x[j])
		j = i
	return abs(s/2.)

def polyArea2(pts): #向量
	s=0
	_len=len(pts)
	x,y=zip(*pts)
	j=_len-1
	for i in range(_len):
		s=s+(x[j]*y[i]-x[i]*y[j])
		j=i
	return abs(s/2.)

print polyArea1([[0,0],[0,1],[1,1],[1,0]])
print polyArea2([[0,0],[0,1],[1,1],[1,0]])
