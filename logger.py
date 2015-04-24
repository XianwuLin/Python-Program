#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author  :  Victor Lin
# Date    :  12/04/2014 10:50
import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s --- %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='log.txt',
                filemode='a')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s: %(levelname)s --- %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
