import string

import tornado.web
import random
import hashlib
import jwt

from auth.jwtauth import jwtauth
from database.Server import ServerDocuments
from auth.serverjwtauth import serverjwtauth
from basehandler import BaseHandler


@jwtauth
class ServerAPIKeyRegen(BaseHandler):
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        print data
        try:
            serverName = data["serverName"]
        except Exception, e:
            json = {"error": "invalid json"}
            self.write(json)
            self.finish()
        if ServerDocuments().get_server(serverName) is not None:
            username = self.request.headers.get("username")
            salt = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))
            private_key = str("" + (hashlib.sha512(bytes(salt))).hexdigest())
            print private_key

            public_key = jwt.encode({'serverName': serverName}, private_key, algorithm='HS256')
            ServerDocuments().update_server_key(serverName,username, public_key, str(private_key))
            json = {"msg": "server key regened :)","publicKey" : public_key}
            self.write(json)
            self.finish()
        else:
            json = {"ERROR":"No servers exists"}
            self.write(json)
            self.finish()

@jwtauth
class ServerRegisterHandler(BaseHandler):
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        try:
            serverName = data["serverName"]
            description = data["description"]
            ip_address = data["ip_address"]

        except Exception, e:
            json = {"error": "invalid json"}
            self.write(json)
            self.finish()
            return

        if ServerDocuments().get_server(serverName) is None:
            private_key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(100))

            print private_key

            public_key = jwt.encode({'serverName': serverName}, private_key, algorithm='HS256')
            username = self.request.headers.get("username")
            ServerDocuments().add_server(serverName, username, description, ip_address, public_key, private_key)

            json = {"msg": "server registers :)","auth_token" : public_key}
            self.write(json)
            self.finish()
            return

        else:
            json = {"error": "Server exits"}
            self.write(json)
            self.finish()
            return
@jwtauth
class ServerUpdateHandler(BaseHandler):
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        try:
            username = self.request.headers.get("username")
            if data.has_key("serverNameOld") :
                serverNameOld = data["serverNameOld"]
            else:
                serverNameOld = ""
            serverName = data["serverName"]
            description = data["description"]
            ip_address = data["ip_address"]

        except Exception, e:
            json = {"error": "invalid json"}
            self.write(json)
            self.finish()
            return

        if ServerDocuments().get_server(serverNameOld) is not None:
            private_key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(100))
            public_key = jwt.encode({'serverName': serverName}, private_key, algorithm='HS256')
            ServerDocuments().update_server(serverNameOld, serverName, username, description, ip_address,public_key, private_key)
            data = {
                "server_name":serverName,
                "ip_address":ip_address,
                "description":description,
                "public_key":public_key,
            }
            self.finish({"servers":data})
            return
        else:
            private_key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(100))
            public_key = jwt.encode({'serverName': serverName}, private_key, algorithm='HS256')
            username = self.request.headers.get("username")
            ServerDocuments().add_server(serverName, username, description, ip_address, public_key, private_key)
            data = {
                "server_name":serverName,
                "ip_address":ip_address,
                "description":description,
                "public_key":public_key,
            }
            self.finish({"servers":data})


@jwtauth
class ServerListHandler(BaseHandler):
    def get(self):
        username = self.request.headers.get("username")
        data = []
        print "hi 1"
        doc = ServerDocuments().get_one_servers_by_user(username)
        print(doc)
        if doc is not None:
            print "hi 3"
            data = {
                "server_name":doc["serverName"],
                "public_key":doc["public_key"],
                "ip_address":doc["ip_address"],
                "description":doc["description"],
                "status":"ALIVE"
            }
            self.finish({"servers":data})
        else:
            json = {"ERROR": "No servers Exist"}
            self.finish(json)






@serverjwtauth
class ServerHandler(BaseHandler):
    def get(self):
        serverName =  self.request.headers.get("serverName")
        if serverName:
            self.write(serverName);
        else:
            self.write("nano");