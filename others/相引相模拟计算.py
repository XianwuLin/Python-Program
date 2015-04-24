#! /usr/bin/python
# -*- coding: GBK -*-

import random
import math
print "相引相模拟计算(10000次)"
print ""
grup=10000
son=[0,0,0,0]
class item:
    def _init_(self):
        self.gam1=""
        self.gam2=""

while(1):
    a=item()
    ref_in=""
    while (1):
        ref_in = raw_input("请输入重组率（输入q退出）:\n")
        if ref_in == "q":
            exit(0)
        else:
            try:
               ref =float(ref_in)
            except:
                print "请输入正确的重组率！"
                continue
            if ref > 0.5 or ref < 0:
                print "请输入正确的重组率！"
                continue
            else:
                for t in range(4):
                    son[t]=0
                break
        
    i=grup
    while(i):
        dice=random.randint(0,100)/100.0
        if dice<ref:
            a.gam1='Ab'
            a.gam2='aB'
        else:
            a.gam1='AB'
            a.gam2='ab'
        son_temp_1=random.choice([a.gam1,a.gam2])
        
        dice=random.randint(0,100)/100.0
        if dice<ref:
            a.gam1='Ab'
            a.gam2='aB'
        else:
            a.gam1='AB'
            a.gam2='ab'
        son_temp_2=random.choice([a.gam1,a.gam2])
        
        son_temp=son_temp_1 + son_temp_2
        if son_temp.find('A')!=-1 and son_temp.find('B')!=-1:
            son[0] +=1
        elif son_temp.find('A')!=-1 and son_temp.find('B')==-1:
            son[1] +=1
        elif son_temp.find('A')==-1 and son_temp.find('B')!=-1:
            son[2] +=1
        elif son_temp.find('A')==-1 and son_temp.find('B')==-1:
            son[3] +=1
        i=i-1
    print ""
    print "类型：		   A_B_ \tA_bb \taaB_ \taabb"
    print "模拟实验数据:  ","  ",son[0],"\t",son[1],"\t",son[2],"\t",son[3]
    print "孟德尔理论计算:","  ",grup*9/16,"\t",grup*3/16,"\t",grup*3/16,"\t",grup*1/16
    print "理论重组率: \t %.2f%%" % (ref * 100)
    cal_ref=1 - 2 * math.sqrt(float(son[3])/grup)
    print "计算重组率: \t %.2f%%" % (cal_ref * 100)
    if ref !=0:
        err= (abs(cal_ref - ref)) / ref * 100
	print "相对误差: \t %.1f%%" %err
    else:
	print "绝对误差: \t %.3f" %(abs(cal_ref - ref))
    print ""
