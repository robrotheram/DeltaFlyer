import pprint
import time

from database.DB import DB
from tornado.options import options

class ServerDocuments(DB):

    def __init__(self,host=None,port=None,db=None):
        if host is None:
            DB.__init__(self,options.mongo_host,options.mongo_port,options.mongo_db)
        else:
            DB.__init__(self,host,port,db)


    def add_server(self, name,username, description,host,public_key,private_key):
        date = int(time.time())
        self.db.servers.insert_one(
            {
                "serverName"  : name,
                "username"    : username,
                "description" : description,
                "ip_address"  : host,
                "public_key"  : public_key,
                "private_key" : private_key,
                "created_at"  : date
            }
        );

    def update_server_key(self, name,username, public_key,private_key):
        result = self.db.servers.update_one({"serverName"  : name, "username": username},{"$set":{
            "public_key"  : public_key,
            "private_key" : private_key,
        }});
        print private_key
        print public_key

    def update_server(self, serverNameOld, serverName, username, description,host,public_key,private_key):
        print {"serverName": serverNameOld, "username": username};
        result = self.db.servers.update_one({"serverName": serverNameOld, "username": username},
                                    {"$set":{
                                        "serverName": serverName,
                                        "description": description,
                                        "ip_address": host,
                                        "public_key"  : public_key,
                                        "private_key" : private_key,
                                        }
                                    });
        print result;


    def get_server(self, serverName):
        return self.db.servers.find_one({"serverName" : serverName})

    def get_serverByPublic(self, publicKey):
        return self.db.servers.find_one({"public_key": publicKey})

    def get_servers_by_user(self, username):
        return self.db.servers.find({"username": username})

    def get_one_servers_by_user(self, username):
        print "hi 2"
        return self.db.servers.find_one({"username": username})
