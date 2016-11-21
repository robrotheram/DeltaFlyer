import tornado.web
import tornado
import hashlib, uuid
import datetime
from pymongo import MongoClient
import jwt
import time
from auth.jwtauth import jwtauth

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

        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha512(password + salt).hexdigest()
        self.write(hashed_password)

        client = MongoClient('192.168.1.173', 27017)
        db = client.beta
        result = db.users.insert_one(
            {
                "username" : username,
                "password" : hashed_password,
                "email" : email,
                "salt" : salt,
                "created_at" : date
            }
        );
        client.close();


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

        client = MongoClient('192.168.1.173', 27017)
        db = client.beta
        result = db.users.find_one({"username" : username});
        hashed_password = hashlib.sha512(password + result["salt"]).hexdigest()
        if hashed_password == result["password"] :
            response = {"login":"True","token":self.encoded}
            self.write(response)
        else:
            self.write("NO")