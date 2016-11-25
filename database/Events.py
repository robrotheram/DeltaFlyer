from database.DB import DB
from tornado.options import options

class EventDocuments(DB):

    def __init__(self,host=None,port=None,db=None):
        if host is None:
            DB.__init__(self,options.mongo_host,options.mongo_port,options.mongo_db)
        else:
            DB.__init__(self,host,port,db)

    def getEvents(self,collection,t=0,delta=60):
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
    #1479205639
    ed = EventDocuments('127.0.0.1', 27017,"beta");
    ed.getEvents("testACCOUNT_events",0,(800000))
    ed.execute()

    print ed.refine(["EventType"]).toJson()


    #.filter("EventType",["CreatureSpawnEvent"])



