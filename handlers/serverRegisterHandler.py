import tornado.web
import random
import hashlib
import jwt

from auth.jwtauth import jwtauth
from database.Server import ServerDocuments
from auth.serverjwtauth import serverjwtauth


@jwtauth
class ServerRegisterHandler(tornado.web.RequestHandler):
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
            private_key = (hashlib.sha512(bytes(serverName))).hexdigest()

            print private_key

            public_key = jwt.encode({'serverName': serverName}, private_key, algorithm='HS256')

            ServerDocuments().add_server(serverName, description, ip_address, public_key, private_key)

            json = {"msg": "server registers :)","auth_token" : public_key}
            self.write(json)
            self.finish()
            return

        else:
            json = {"error": "Server exits"}
            self.write(json)
            self.finish()
            return


@serverjwtauth
class ServerHandler(tornado.web.RequestHandler):
    def get(self):
        serverName =  self.request.headers.get("serverName")
        if serverName:
            self.write(serverName);
        else:
            self.write("nano");