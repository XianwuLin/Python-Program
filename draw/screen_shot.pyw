# -*- coding: utf-8 -*-
#! /usr/bin/python

from PIL import ImageGrab
import time
def screen_shot():
    time.sleep(5)
    im = ImageGrab.grab()
    im.save(u"截图.jpg")

if __name__ == "main":
    import easygui
    easygui.msgbox("Capture the screen after 5s!")
    screen_shot()
