<<<<<<< HEAD
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import sys
import requests
import locale
from urllib import urlencode

def fetch(query_str=''):
    query_str = query_str.strip("'").strip('"').strip()
    if not query_str:
        query_str = 'python'

    query = {
        'q': query_str.encode("utf-8")
    }
    url = 'http://fanyi.youdao.com/openapi.do?keyfrom=linxianwu201&key=829523590&type=data&doctype=json&version=1.1&%s' % urlencode(
        query)
    req = requests.get(url)
    html = req.content.decode("utf8", 'ignore')
    return html


def parse(html):
    try:
        d = json.loads(html)
    except:
        print '翻译出错，请输入合法单词'
    try:
        print "translate:\n    ---> {0}".format(d["translation"][0])
    except Exception as e:
        print "translate:\n    ---> {no translate}"

    try:
        print "dict:\n",
        if d.get('errorCode') == 0:
            explains = d.get('basic').get('explains')
            for i in explains:
                print "     --->%s" % i
        else:
            print '无法翻译'
    except Exception as e:
        print "     --->{no dict}"


def main():
    try:
        s = " ".join(sys.argv[1:]).decode(sys.stdin.encoding or locale.getpreferredencoding(True))
    except IndexError:
        s = u'python'
    parse(fetch(s))


if __name__ == '__main__':
    main()
=======
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import sys
import requests
import locale
from urllib import urlencode

def fetch(query_str=''):
    query_str = query_str.strip("'").strip('"').strip()
    if not query_str:
        query_str = 'python'

    query = {
        'q': query_str.encode("utf-8")
    }
    url = 'http://fanyi.youdao.com/openapi.do?keyfrom=linxianwu201&key=829523590&type=data&doctype=json&version=1.1&%s' % urlencode(
        query)
    req = requests.get(url)
    html = req.content.decode("utf8", 'ignore')
    return html


def parse(html):
    try:
        d = json.loads(html)
    except:
        print '翻译出错，请输入合法单词'
    try:
        print "translate:\n    ---> {0}".format(d["translation"][0])
    except Exception as e:
        print "translate:\n    ---> {no translate}"

    try:
        print "dict:\n",
        if d.get('errorCode') == 0:
            explains = d.get('basic').get('explains')
            for i in explains:
                print "     --->%s" % i
        else:
            print '无法翻译'
    except Exception as e:
        print "     --->{no dict}"


def main():
    try:
        s = " ".join(sys.argv[1:]).decode(sys.stdin.encoding or locale.getpreferredencoding(True))
    except IndexError:
        s = u'python'
    parse(fetch(s))


if __name__ == '__main__':
    main()
>>>>>>> d0490cbf9752d48faa3576514bbb54e4e7d6319d
