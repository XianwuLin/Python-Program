#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   Victor Lin
#   E-mail  :   linxianwusx@gmail.com
#   Date    :   14/12/05 19:58:06
from logger import *
import cv2
import thread
import tornado.ioloop
import tornado.web
import tornado.websocket
import base64
import json
import psutil
import time
import redis

from tornado.options import define, options, parse_command_line

define("port", default=80, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def percent(self):
        while self.thread_run:
            self.type = 'cpu_percent'
            self.data= round(psutil.cpu_percent(), 0)
            self.write_message( json.dumps({'type':self.type, 'data':self.data}) )
            time.sleep(0.5)

    def cam(self):
        self.capture = cv2.VideoCapture(0)
        _ret, self.frame = self.capture.read()
        while (self.frame is None):
            _ret, self.frame = self.capture.read()

        while self.thread_run:
            _ret, self.frame = self.capture.read()
            self.img = cv2.imencode('.jpg', self.frame)[1].tostring()
            self.data = base64.b64encode(self.img)
            self.type = 'cam'
            self.write_message( json.dumps({'type':self.type, 'data':self.data}) )
            time.sleep(2)
        self.capture.release()

    def erweima(self, dt):
        import uuid
        self.type = 'erweima'
        self.uuid = str(uuid.uuid1())
        self.r.set(self.uuid, dt.encode('utf8'))
        self.write_message( json.dumps({'type':self.type, 'data':'http://192.168.1.104/erweima/' + self.uuid}) )

    def open(self):
        self.thread_run = True
        logging.info("Socket open!")

    def on_message(self, message):
        c_msg = message
        self.r = redis.Redis(host='localhost', port=6379, db=0) 
        if c_msg == "cam":
            thread.start_new_thread(self.cam,())
        elif c_msg == "cpu_percent":
            thread.start_new_thread(self.percent,())
        else:
            self.get_data = c_msg.split('/'*6)
            print self.get_data
            if self.get_data[1] == 'erweima':
                self.erweima(self.get_data[0])

        logging.info("%s is send!" % c_msg)

    def on_close(self):
        self.thread_run = False
        self.r.save()
        logging.info("Socket close!")

class Geterweima(tornado.web.RequestHandler):
    def get(self,uuid):
        r = redis.Redis(host='localhost', port=6379, db=0)
        data = r.get(uuid)
        if data == "":
            data = u"二维码错误！"
        self.write(data)

app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/socket', WebSocketHandler),
    (r'/erweima/(\S+)',Geterweima),
])

if __name__ == '__main__':
    parse_command_line()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
