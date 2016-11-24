import tornado.web
from auth.jwtauth import jwtauth

class EventTypeHandler(tornado.web.RequestHandler):
    def get(self,type):
        self.write('ok '+type)

class EventHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('ok')
