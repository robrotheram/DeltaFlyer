import tornado.web
import tornado
import hashlib, uuid
import datetime
from pymongo import MongoClient
import jwt
import time
from auth.jwtauth import jwtauth
from database.Users import UserDocuments


@jwtauth
class UserHandler(tornado.web.RequestHandler):
    def get(self):
        # Contains user found in previous auth
        if self.request.headers.get('auth'):
            self.write('ok')

class RegisterHandler(tornado.web.RequestHandler):
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        try:
            username = data["username"]
            password = data["password"]
            email = data["email"]
            date = int(time.time())
        except Exception, e:
            json = {"error":"invalid json"}
            self.write(json)
            self.finish()
            return

        if UserDocuments().get_user(username) is None:
            salt = uuid.uuid4().hex
            hashed_password = hashlib.sha512(password + salt).hexdigest()
            UserDocuments().add_user(username,hashed_password,salt,email)

            json = {"msg":"User registers :) "}
            self.write(json)
            self.finish()
            return

        else :
            json = {"error":"user exits"}
            self.write(json)
            self.finish()
            return




class AuthHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.encoded = jwt.encode({
            'some': 'payload',
            'a': {2: True},
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)},
            'secret_string',
            algorithm='HS256'
        )
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        try:
            username = data["username"]
            password = data["password"]
        except Exception, e:
            json = {"error": "invalid json"}
            self.write(json)
            self.finish()
            return


        result = UserDocuments().get_user(username)
        hashed_password = hashlib.sha512(password + result["salt"]).hexdigest()
        if hashed_password == result["password"] :
            response = {"login":True,"token":self.encoded}
            self.write(response)
        else:
            response = {"login":False, "msg":"username and/or password invalid"}
            self.write(response)