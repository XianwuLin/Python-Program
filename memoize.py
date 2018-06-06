#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
这里构造了一个缓存函数的装饰器，可以缓存一个函数的调用结果，可以指定过期时间
参考资料：http://book.pythontips.com/en/testing/function_caching.html

memozie 最好传递一个unique_name参数，指定缓存函数的名称，否则不同的函数的缓存结果容易混在一起。
"""

import functools
from unqlite import UnQLite
import time
import json
import pickle

mem_cache_db = UnQLite()
def memoize(function=None, unique_name="unique", timeout=0):
    if not function:
        return functools.partial(memoize, unique_name=unique_name, timeout=timeout)
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        wargs = str(args) + str(kwargs)
        now = time.time()
        if mem_cache_db.exists(unique_name+wargs): # 已缓存
            data = json.loads(mem_cache_db[unique_name+wargs])
            if not timeout: #timeout=0 永不过期
                return pickle.loads(data["result"])
            else:
                if now - data["time"] < timeout: #未过期
                    return pickle.loads(data["result"])
                else: #消极过期
                    data = function(*args, **kwargs)
                    load_data = {"time": now, "result": pickle.dumps(data)}
                    mem_cache_db[unique_name+wargs] = json.dumps(load_data)
                return data
        else: # 未缓存
            data = function(*args, **kwargs)
            load_data = {"time": now, "result": pickle.dumps(data)}
            mem_cache_db[unique_name+wargs] = json.dumps(load_data)
            return data
    return wrapper


def remove_memoize(unique_name):
    """清除缓存"""
    keys_list = list()
    for key in mem_cache_db.keys():
        if key.startswith(unique_name):
            keys_list.append(key)
    for key in keys_list:
        mem_cache_db.delete(key)


@memoize(unique_name="unique", timeout=2)
def fibonacci(n):
    if n < 2: return n
    return fibonacci(n - 1) + fibonacci(n - 2)


old = time.time()
print fibonacci(n=30)
print time.time() - old
