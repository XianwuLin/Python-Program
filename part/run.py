#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-11-19 10:25:35
# @Author  : Xianwu Lin
# @Email    : linxianwusx@gmail.com
import nlpir
import tornado.ioloop
import tornado.web
import tornado.websocket

from tornado.options import define, options, parse_command_line

define("port", default=80, help="run on the given port", type=int)
class IndexHandler(tornado.web.RequestHandler):
    def part_from_string(self,string):
        if not string:
            return ""
        part = []
        for t in nlpir.Seg(string):
            part.append(t[0])

        part_string = " ".join(part)
        return part_string

    def get(self,string):
        if not string:
            self.write("")
        self.write(self.part_from_string(string))

    def post(self,_):
        string = self.request.body
        if not string:
            self.write("")
        self.write(self.part_from_string(string))

app = tornado.web.Application([
    (r'/(\S*)', IndexHandler),
])

if __name__ == '__main__':
    parse_command_line()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
