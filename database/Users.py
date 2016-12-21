import time

from database.DB import DB
from tornado.options import options

class UserDocuments(DB):

    def __init__(self,host=None,port=None,db=None):
        if host is None:
            DB.__init__(self,options.mongo_host,options.mongo_port,options.mongo_db)
        else:
            DB.__init__(self,host,port,db)


    def add_user(self, username,hashed_password,salt,email):
        date = int(time.time())
        self.db.users.insert_one(
            {
                "username" : username,
                "password" : hashed_password,
                "email" : email,
                "salt" : salt,
                "created_at" : date
            }
        );
    def update_user(self, username,hashed_password,salt,email):
        print {"username": username};
        result = self.db.users.update_one({"username": username},
                                                {"$set":{
                                                    "password" : hashed_password,
                                                    "email" : email,
                                                    "salt" : salt,
                                                }
                                            });
        print result;

    def get_user(self, username):
        return self.db.users.find_one({"username" : username})



if __name__ == "__main__":
    pd = UserDocuments('127.0.0.1', 27017,"beta");
    pd.getAllPlayerEvents(
        "testACCOUNT_events",
        "9ac16c7f-6ef7-4df3-af4a-934b9e89d1a4",
        1479205639
    ).filter("EventType",["PlayerMoveEvent"]).execute()

    print pd.refine(["playerName"]).toJson()



    #    print pd.getE"playerUUID" : "9ac16c7f-6ef7-4df3-af4a-934b9e89d1a4",ventsWithType("testACCOUNT_events","PlayerMoveEvent").toJson()