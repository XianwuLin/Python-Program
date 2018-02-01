#coding:utf-8 
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

authorizer = DummyAuthorizer()
authorizer.add_user('admin', 'password', './', perm='elradfmw')

authorizer.add_anonymous('./')
handler = FTPHandler
handler.authorizer = authorizer
server = FTPServer(('0.0.0.0', 2121), handler)
server.serve_forever()