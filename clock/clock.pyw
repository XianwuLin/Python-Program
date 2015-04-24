# -*- coding: utf-8 -*-
#__author__ = 'Victor'


import time
import thread
import mp3
import easygui

field = easygui.multenterbox(u"请输入时间", u"闹钟", [u"小时", u"分钟"])
name = easygui.enterbox(u"提醒", u"闹钟")
if name == "":
    name = u"时间到！"
if field[1] == "":
    field[1] = 0
while (True):
    hours_now,minutes_now = time.localtime()[3],time.localtime()[4]
    if hours_now == int(field[0]) and minutes_now == int(field[1]):
        thread.start_new_thread(mp3.mp3, (30,))
        if easygui.msgbox(name, u"闹钟"):
            exit(0)
        break
    time.sleep(1)
