from database.DB import DB
from tornado.options import options

class WorldDocuments(DB):

    def __init__(self,host=None,port=None,db=None):
        if host is None:
            DB.__init__(self,options.mongo_host,options.mongo_port,options.mongo_db)
        else:
            DB.__init__(self,host,port,db)

    def getWorldAT(self,collection, t=0,delta=60):
        self.gettimeboundaries(t,delta)
        self.collection = collection
        self.querry = {
            "meta.time": {
                "$gte":self.time_lower,
                "$lt":self.time_upper
            }
        }
        return self

if __name__ == "__main__":
    pd = WorldDocuments('127.0.0.1', 27017,"beta");
    pd.getChunksAT(
            "testACCOUNT_chunks",
            "world",
            1479993634 #1479205639
        )
    pd.set_sort("time",-1)
    pd.set_limit(0)

    pd.execute()

    print pd.count()
