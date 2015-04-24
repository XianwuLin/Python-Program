# -*- coding: GBK -*-
#! /usr/bin/python

a = [0.25, 0.5, 0.25] #AA、Aa、aa的初始比例为1:2:1
loop = 100
print "Calculate The Effect Of Removing The Recessive Gene"
print"Num\t\tAA\tAa"

for i in range ( 1, loop ) :
#去除隐性个体
    a[2] = 0
    a[1] = a[1] / ( a[1] + a[0] )
    a[0] = a[0] / ( a[1] + a[0] )

#打印基因型值
    print "Num ", i, ":\t%.3f" % a[0], "\t%.3f" % a[1]

#如果杂合率小于0.05则停止运算
    if a[1] <= 0.05:
        print "Total", i ,"steps."
        break

#遗传
    a[0] = ( a[0] * a[0] ) + ( a[0] * a[1] )
    a[1] =                 ( a[0] * a[1] )
    a[2] =                               ( a[1] * a[1] )
