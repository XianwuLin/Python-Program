#!/usr/bin/env python
# coding: utf-8
from inspect import currentframe

DEBUG = True

def get_linenumber():
    cf = currentframe()
    return str(cf.f_back.f_back.f_lineno)
def dbgPrint(msg):
    if DEBUG:
        print get_linenumber(),msg