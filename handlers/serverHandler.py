import tornado.web
from auth.jwtauth import jwtauth
@jwtauth
class ServerHandler(tornado.web.RequestHandler):
    def get(self):
        # Contains user found in previous auth
        if self.request.headers.get('auth'):
            self.write('ok')
