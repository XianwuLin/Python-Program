#! /usr/bin/python
# -*- coding: GBK -*-
from math import pi
import re
from enthought.traits.api import HasTraits,Str,Float
from enthought.traits.ui.api import View, Item
from enthought.traits.ui.menu import OKButton, CancelButton

class Window(HasTraits):
	function = Str
	x_min = Str
	x_max = Str
	y_min = Str
	y_max = Str

view1 = View(
	Item(name = 'function',label = u'y=',tooltip = u'乘号要写出来'),
	Item(name = 'x_min',label = 'x最小值'),
	Item(name = 'x_max',label = 'x最大值'),
	Item(name = 'y_min',label = 'y最小值'),
	Item(name = 'y_max',label = 'y最大值'),
	resizable = True,
    width = 400,
    buttons = [OKButton, CancelButton])
wiw=Window()
wiw.x_min = '-pi'
wiw.x_max = 'pi'
wiw.y_min = '-pi'
wiw.y_max = 'pi'
wiw.configure_traits(view=view1)

out_function = re.sub('\^','**',wiw.function)
out_function = re.sub('\s+','',out_function)
f=open(u'绘图实例.py', 'w')
f.write('#! /usr/bin/python\n')
f.write('from pylab import *\n')
f.write('x = arange(' + str(wiw.x_min) + ',' + str(wiw.x_max) + ',0.001)\n')
f.write('y = '+str(out_function)+'\n')
f.write('plt.plot(x,y)\n')
f.write('plt.title("y = ' + str(wiw.function) + '")\n')
f.write('plt.xlabel(u\'x\')\n')
f.write('plt.ylabel(u\'y\')\n')
f.write('plt.axis([' + str(wiw.x_min) + ',' + str(wiw.x_max) + ','  + str(wiw.y_min) + ',' + str(wiw.y_max) + '])\n')
f.write('plt.grid(True)\n')
f.write('plt.show()\n')
f.close()

execfile('绘图实例.py')
