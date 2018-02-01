#!coding=utf-8
import functools
import hashlib
import pickle

import redis

FUNC_CACHE_HEAD = "FUNC_CACHE_HEAD"
funcqueue = redis.StrictRedis(host='127.0.0.1', port=3306, db=0, password='')

def memoize(function=None, unique_name="unique", timeout=10):
    """缓存函数"""
    if not function:
        return functools.partial(memoize, unique_name=unique_name, timeout=timeout)
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        wargs = str(args) + str(kwargs)
        md5_c = hashlib.md5()
        md5_c.update(FUNC_CACHE_HEAD + "{0}".format(unique_name+wargs))
        memozie_key = md5_c.hexdigest()
        data = funcqueue.get(memozie_key)
        if data is None:
            data = function(*args, **kwargs)
            data = pickle.dumps(data)
            funcqueue.set(memozie_key, data)
        funcqueue.expire(memozie_key, timeout)
        return pickle.loads(data)
    return wrapper

def remove_memoize(unique_name):
    """清除缓存"""
    keys_list = funcqueue.keys(FUNC_CACHE_HEAD + "{0}*".format(unique_name))
    for key in keys_list:
        funcqueue.delete(key)
