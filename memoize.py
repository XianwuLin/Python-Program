#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
这里构造了一个缓存函数的装饰器，可以缓存一个函数的调用结果，可以指定过期时间
参考资料：http://book.pythontips.com/en/testing/function_caching.html

memozie 最好传递一个unique_name参数，指定缓存函数的名称，否则不同的函数的缓存结果容易混在一起。
"""

import functools
import time


def memoize(function=None, unique_name="unique", timeout=0):
    if not function:
        return functools.partial(memoize, unique_name=unique_name, timeout=timeout)
    memo = {}
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        wargs = str(args) + str(kwargs)
        if unique_name not in memo:
            memo[unique_name] = dict()
        if wargs in memo[unique_name]:
            if timeout == 0:  #timeout=0 永不过期
                return memo[unique_name][wargs]["result"]
            else:
                if time.time() - memo[unique_name][wargs]["timeout"] < timeout: #未过期
                    return memo[unique_name][wargs]["result"]
                else:  #消极过期
                    rv = function(*args, **kwargs)
                    memo[unique_name][wargs] = {"timeout":time.time(),  #缓存的时间戳
                                    "result": rv}   #缓存的结果
                    return rv
        else: #不在缓存中
            rv = function(*args, **kwargs)
            memo[unique_name][wargs] = {"timeout":time.time(),  #缓存的时间戳
                               "result": rv}   #缓存的结果
            return rv
    return wrapper


@memoize(unique_name="unique", timeout=2)
def fibonacci(n):
    if n < 2: return n
    return fibonacci(n - 1) + fibonacci(n - 2)


old = time.time()
print fibonacci(n=30)
print time.time() - old
