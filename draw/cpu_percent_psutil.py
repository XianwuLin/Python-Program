from Tkinter import *
import psutil


def redraw(p,side):
    w.delete("all")
    w.create_line(0 + side, 0 + side, 0 + side, 200 + side)
    w.create_line(0 + side, 0 + side, 300 + side, 0 + side)
    w.create_line(0 + side, 200 + side, 300 + side, 200 + side)
    w.create_line(300 + side, 0 + side, 300 + side, 200 + side)
    
    now_cpu_percent = round(psutil.cpu_percent(), 0)
    p = p[1:] + [now_cpu_percent]
    for i in xrange(100-1):
        w.create_line(i*3 + side, 200-p[i]*2 + side, (i+1)*3 + side, 200-p[i+1]*2 + side)
    
    w.after(500,redraw,p,5)
    
p = [0] * 100
root = Tk()
root.geometry('310x210')
w = Canvas(root, width = 310, height = 210)
w.pack()
redraw(p,5)

w.mainloop()
