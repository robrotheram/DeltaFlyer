from database.DB import DB
from tornado.options import options

class ChuckDocuments(DB):

    def __init__(self,host=None,port=None,db=None):
        if host is None:
            DB.__init__(self,options.mongo_host,options.mongo_port,options.mongo_db)
        else:
            DB.__init__(self,host,port,db)

    def getChunksAT(self,collection,w, x,z, t=0):
        self.gettimeboundaries(t,0)
        self.collection = collection
        self.querry = {
            "Time": {
                "$lt":self.time_upper
            },
            "location.world":w,
            "location.x":int(x),
            "location.z":int(z)

        }
        print self.querry

        return self

#{"time":{"$lt":1479993634},"location.world":"world","location.x":10,"location.z":-11}).sort({"time":-1}).limit(1)

if __name__ == "__main__":
    pd = ChuckDocuments('127.0.0.1', 27017,"beta");
    pd.getChunksAT(
            "testACCOUNT_chunks",
            "world",
            10,
            -11,
            1479993634 #1479205639
        )
    pd.set_sort("time",-1)
    pd.set_limit(0)

    pd.execute()

    print pd.count()
    print pd.toJson()



    #    print pd.getE"playerUUID" : "9ac16c7f-6ef7-4df3-af4a-934b9e89d1a4",ventsWithType("testACCOUNT_events","PlayerMoveEvent").toJson()