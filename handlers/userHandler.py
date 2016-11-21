import tornado.web
from auth.jwtauth import jwtauth
@jwtauth
class UserHandler(tornado.web.RequestHandler):
    def get(self):
        # Contains user found in previous auth
        if self.request.headers.get('auth'):
            self.write('ok')



import jwt

import datetime
from handlers.auth.jwtauth import jwtauth
SECRET = 'my_secret_key'

class AuthHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.encoded = jwt.encode({
            'some': 'payload',
            'a': {2: True},
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=22)},
            SECRET,
            algorithm='HS256'
        )
    def get(self):
        response = {'token': self.encoded}
        self.write(response)
