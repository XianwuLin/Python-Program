#!/usr/bin/python
#!coding=utf-8

import tornado.web
import handler
import os

from tornado.options import define, options

define('port', default=80, help='run on the given port', type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
        (r"/", handler.MainHandler),
        (r"/(\d{4}/\d{2}/\d{2}/\w+)", handler.ShowBlogHandler),   
        (r"/categories/?", handler.CategoriesHandler),
        (r"/about/?", handler.AboutHandler),
        (r"/tags/\S*", handler.ShowTagsHandler),
        ]
        settings = {
            "autoescape":None,
            "static_path": os.path.join(os.path.dirname(__file__), "static"), 
            "template_path":os.path.join(os.path.dirname(__file__), "templates"),
            "cookie_secret": "TDEW9gm3RgKVkdQ9o/1Z+GIyjwZzCEfIm7tALIje1ew=",
            "login_url": "/login",
            'debug': True,
                }
        tornado.web.Application.__init__(self, handlers, **settings)
