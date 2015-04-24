#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   Victor Lin
#   E-mail  :   linxianwusx@gmail.com
#   Date    :   14/12/05 16:30:49
#

import os, sys
import easygui
import thread
import mp3
try:
    from tkinter import *
except ImportError:  #Python 2.x
    PythonVersion = 2
    from Tkinter import *
    from tkFont import Font
    from ttk import *
    #Usage:showinfo/warning/error,askquestion/okcancel/yesno/retrycancel
    from tkMessageBox import *
    #Usage:f=tkFileDialog.askopenfilename(initialdir='E:/Python')
    #import tkFileDialog
    #import tkSimpleDialog
else:  #Python 3.x
    PythonVersion = 3
    from tkinter.font import Font
    from tkinter.ttk import *
    from tkinter.messagebox import *
    #import tkinter.filedialog as tkFileDialog
    #import tkinter.simpledialog as tkSimpleDialog    #askstring()

class Application_ui(Frame):
    #这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title(u'番茄闹钟')
        self.master.resizable(0,0)
        self.master.wait_visibility(self.master)
        self.master.wm_attributes('-topmost', 1)
        self.master.geometry('120x90+1100+530')
        self.createWidgets()

    def createWidgets(self):
        self.top = self.winfo_toplevel()

        self.style = Style()

        self.style.configure('TCommand1.TButton', font=(u'微软雅黑',9))
        self.Command1 = Button(self.top, text=u'来一个番茄', command=self.Command1_Cmd, style='TCommand1.TButton')
        self.Command1.place(relx=0.1, rely=0.5, relwidth=0.700, relheight=0.400)

        self.style.configure('TLabel1.TLabel', anchor='w', foreground='#FF0000', font=(u'微软雅黑',20))
        self.Label1 = Label(self.top, justify='center', style='TLabel1.TLabel')
        self.Label1.place(relx=0.2, rely=0.1, relwidth=0.700, relheight=0.400)


class Application(Application_ui):
    #这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None):
        Application_ui.__init__(self, master)
        self.state = 1

    def Command1_Cmd(self, event=None):
        if self.state == 1:
            self.k = 0 # k is the timer, make timer to zero and start the clock
            self.Command1["state"] = "disabled"
            self.total_time = 25 * 60
            self.after(1000,self.abc)
        elif self.state == 2:
            self.k = 0 # k is the timer, make timer to zero and start the clock
            self.Command1["state"] = "disabled"
            self.total_time = 5 * 60
            self.after(1000,self.abc)
            return

    def abc(self):
        self.Label1["text"] = str((self.total_time - self.k) / 60) + ":" + str((self.total_time - self.k) % 60)
        self.Label1.update()
        self.k += 1
        if self.k == self.total_time:
            self.Command1["state"] = "normal"
            self.Label1["text"] = u"小番茄"
            thread.start_new_thread(mp3.mp3, (3,))
            easygui.msgbox("时间到！")
            if self.state == 1:
                self.Command1["text"] = u"番茄好了"
                self.state = 2
                return
            elif self.state == 2:
                self.Command1["text"] = u"来一个番茄"
                self.state =1
                return
            self.k = 0

        self.after(1000,self.abc)

if __name__ == "__main__":
    top = Tk()
    Application(top).mainloop()

