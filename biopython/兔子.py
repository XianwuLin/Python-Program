# -*- coding: utf-8 -*-
#！/usr/bin/python

'''
斐波那契 兔子问题
有一对兔子，每月生k对兔子，生下的兔子第二个月开始也是每个月生k对兔子，问n各月后兔子的总数。

f(n) = f(n-1) + f(n-2) * k
'''

k = 4; n = 35
f = [1 for i in range(0,n)]
f[1] = f[0] * (k + 1)
for i in range(2,n):
	f[i] = f[i-1] + f[i-2] * k
print [f[i] for i in range(0,n)]
