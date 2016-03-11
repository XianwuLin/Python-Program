#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, sys
import time
import datetime
import ntplib
import threading

if sys.version_info[0] == 2:
    from Tkinter import *
    from tkFont import Font
    from ttk import *
    #Usage:showinfo/warning/error,askquestion/okcancel/yesno/retrycancel
    from tkMessageBox import *
    #Usage:f=tkFileDialog.askopenfilename(initialdir='E:/Python')
    #import tkFileDialog
    #import tkSimpleDialog
else:  #Python 3.x
    from tkinter import *
    from tkinter.font import Font
    from tkinter.ttk import *
    from tkinter.messagebox import *
    #import tkinter.filedialog as tkFileDialog
    #import tkinter.simpledialog as tkSimpleDialog    #askstring()

class Application_ui(Frame):
    #这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('毫秒级北京时间')
        self.master.geometry('700x300')
        self.createWidgets()

    def createWidgets(self):
        self.top = self.winfo_toplevel()

        self.style = Style()

        self.style.configure('TLabel1.TLabel', anchor='w', font=('宋体',17))
        self.Label1 = Label(self.top, text='北京时间：', style='TLabel1.TLabel')
        self.Label1.place(relx=0.083, rely=0.108, relwidth=0.362, relheight=0.16)

        self.style.configure('TLabel2.TLabel', anchor='w', font=('宋体',30), foreground='red')
        self.Label2 = Label(self.top, text='获取北京时间中……', style='TLabel2.TLabel')
        self.Label2.place(relx=0.128, rely=0.30, relwidth=0.696, relheight=0.316)

        self.style.configure('TLabel3.TLabel', anchor='w', font=('宋体',9), foreground='#333')
        self.Label3 = Label(self.top, text='*本机毫秒级同步到北京时间', style='TLabel3.TLabel')
        self.Label3.place(relx=0.75, rely=0.78, relwidth=0.696, relheight=0.316)

        self.style.configure('TCommand1.TButton', font=('宋体',17))
        self.Command1 = Button(self.top, text='刷新', command=self.Command1_Cmd, style='TCommand1.TButton')
        self.Command1.place(relx=0.178, rely=0.70, relwidth=0.285, relheight=0.16)

        self.style.configure('TCommand2.TButton', font=('宋体',17))
        self.Command2 = Button(self.top, text='退出', command=self.Command2_Cmd, style='TCommand2.TButton')
        self.Command2.place(relx=0.638, rely=0.70, relwidth=0.285, relheight=0.16)


class Application(Application_ui):
    #这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None):
        Application_ui.__init__(self, master)
        threading.Thread(target=self.update_time,).start()

    def Command1_Cmd(self, event=None):
        #TODO, Please finish the function here!
        threading.Thread(target=self.update_time,).start()

    def Command2_Cmd(self, event=None):
        #TODO, Please finish the function here!
        exit(0)

    def showtime(self):
        self.Label2["text"]  = str(datetime.datetime.fromtimestamp(time.time()))[:-3]
        self.after(5,self.showtime)

    def update_time(self):
        try:
            c = ntplib.NTPClient()
            response = c.request('cn.ntp.org.cn')
            ts = response.tx_time
            _date = time.strftime('%Y-%m-%d',time.localtime(ts))
            _time = time.strftime('%X',time.localtime(ts))
            os.system('date {} && time {}'.format(_date,_time))
            self.after(5,self.showtime)
        except:
            self.Label2["text"]  = u"请检查网络……"

if __name__ == "__main__":
    top = Tk()
    Application(top).mainloop()



