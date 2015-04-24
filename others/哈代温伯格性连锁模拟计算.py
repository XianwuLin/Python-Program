#! /usr/bin/python
# -*- coding: GBK -*-

from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
import random
import math
import numpy as np
import matplotlib.pyplot as plt
print "哈代-温伯格性连锁基因模拟计算"
sonf=1;
sonm=4;
choice_type=[0,0]
gam=[0,0]
f=[5000,0,0]
m=[0,5000]
precentf=[1.0,0,0]
precentm=[0,1]
times=6;
times = input ("请输入子代数：")
A1f=[0] * (times+1)
A1m=[0] * (times+1)
A1a=[0] * (times+1)
A1f[0] = 1
A1m[0] = 0
x=np.arange(0, times+1, 1)
for j in xrange(times):
	f=[0,0,0]
	m=[0,0]
	for i in xrange (5000):
		#下一代雌性
		dice1=random.random() #雌性配子
		if dice1 < precentf[0] :
			choice_type[0]=1
		elif dice1 >= precentf[0] and dice1 < precentf[0]+ precentf[1]:
			choice_type[0]=random.choice([1,2])
		else:
			choice_type[0]=2

		dice2=random.random() #雄性配子
		if dice2 < precentm[0]:
			choice_type[1]=1
		else:
			choice_type[1]=2

		if choice_type[0]==choice_type[1]: #下一代配子基因型
			if choice_type[0]==1:
				sonf=1;
				f[0] +=1
			else:
				sonf=3
				f[2] +=1
		else:
			sonf=2
			f[1] +=1

		#下一代为雄性
		dice3=random.random() #只有雌性配子
		if dice3 < precentf[0] :
			sonm=4
		elif dice3 >= precentf[0] and dice3 < precentf[0]+ precentf[1]:
			sonm=random.choice([4,5])
		else:
			sonm=5
		if sonm==4:
			m[0] +=1
		else:
			m[1] +=1

	for i in range (3):
		precentf[i] = f[i] / 5000.0
	for i in range (2):
		precentm[i] = m[i] / 5000.0

	A1f[j+1] = precentf[0] + precentf[1] / 2 
	A1m[j+1] = precentm[0]
for i in range(times+1):
	A1a[i] = A1f[i] * 2.0 / 3.0 + A1m[i] * 1.0 / 3.0

plt.plot(x,A1f,"r:,",label="Female",linewidth=2)
plt.plot(x,A1m,"b--",label="Male",linewidth=2)
plt.plot(x,A1a,"k-",label="Combined",linewidth=2)
plt.title(u'哈代-温伯格规律性连锁基因模拟计算')
plt.xlabel(u'世代数')
plt.ylabel(u'A1基因频率')
plt.xticks(range(len(x)))
plt.yticks(np.arange(0, 1.1, 0.1))
plt.grid(True)
plt.legend()
plt.show()
