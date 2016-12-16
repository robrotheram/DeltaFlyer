import math
import tornado.web
import tornado
import hashlib, uuid
import datetime
from pymongo import MongoClient
import jwt
import time
from auth.jwtauth import jwtauth, secret_key
from database.Users import UserDocuments
from tornado.options import define, options


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*");
        self.set_header("Access-Control-Allow-Credentials", "true");
        self.set_header("Access-Control-Allow-Methods", "GET,HEAD,OPTIONS,POST,PUT");
        self.set_header("Access-Control-Allow-Headers", "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers");


    def options(self):
        # no body
        self.set_status(204)
        self.finish()

@jwtauth
class UserHandler(tornado.web.RequestHandler):
    def get(self):
        # Contains user found in previous auth
        if self.request.headers.get('auth'):
            self.write('ok')

class RegisterHandler(BaseHandler):
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

class AuthHandler(BaseHandler):

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
        if result is None:
            self.write({"login":False, "msg":"username and/or password invalid"})
            self.finish();

        hashed_password = hashlib.sha512(password + result["salt"]).hexdigest()
        if hashed_password == result["password"] :

            exp_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=int(options.token_age))

            encoded = jwt.encode({'username':username, 'exp': exp_time},secret_key, algorithm='HS256')
            exp_time = (exp_time - datetime.datetime(1970,1,1)).total_seconds()
            try:
                print exp_time.strftime('%S')
            except Exception, e:
                print e

            response = {
                "login":True,
                "username":username,
                "email":result["email"],
                "exp":math.floor(exp_time),
                "token":encoded,
            }
            print response
            self.write(response)
        else:
            response = {"login":False, "msg":"username and/or password invalid"}
            self.write(response)