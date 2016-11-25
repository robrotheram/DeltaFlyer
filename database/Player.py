from database.DB import DB
from tornado.options import options

class PlayerDocuments(DB):

    def __init__(self,host=None,port=None,db=None):
        if host is None:
            DB.__init__(self,options.mongo_host,options.mongo_port,options.mongo_db)
        else:
            DB.__init__(self,host,port,db)

    def get_by_player_UUID(self,collection, uuid, t=0,delta=60):
        self.gettimeboundaries(t,delta)
        self.collection = collection
        self.querry = {
            "playerUUID" : uuid,
            "meta.time": {
                "$gte":self.time_lower,
                "$lt":self.time_upper
            }
        }
        return self


if __name__ == "__main__":
    pd = PlayerDocuments('127.0.0.1', 27017,"beta");
    pd.getAllPlayerEvents(
            "testACCOUNT_events",
            "9ac16c7f-6ef7-4df3-af4a-934b9e89d1a4",

        ).filter("EventType",["PlayerMoveEvent"]).execute()

    print pd.refine(["playerName"]).toJson()



    #    print pd.getE"playerUUID" : "9ac16c7f-6ef7-4df3-af4a-934b9e89d1a4",ventsWithType("testACCOUNT_events","PlayerMoveEvent").toJson()