import json

from bson import json_util
from pymongo import MongoClient
from bson.json_util import dumps

class EventDocuments:

    def __init__(self,host,port,db):
        client = MongoClient(host,port)
        self.db = client[db]
        self.json_docs = []

    def filter(self, cursor):
        self.json_docs = []
        for doc in cursor:
            doc["time"] = doc["meta"]["time"]
            del doc["meta"]
            del doc["_id"]
            self.json_docs.append(doc)

    def getEventsWithType(self,serverName,type,time,delta):
        less_than_time = time - delta
        self.filter(
            self.db[serverName].find(
                {
                    "EventType":type,
                    "meta.time": {
                        "$gte":less_than_time,
                        "$lt":time
                    }
                }
            )
        )
        return self

    def getEvents(self,serverName,time,delta):
        less_than_time = time - delta
        self.filter(
            self.db[serverName].find(
                {
                    "meta.time": {
                        "$gte":less_than_time,
                        "$lt":time
                    }
                }
            )
        )
        return self

    def toJson(self):
        return dumps(self.json_docs)

if __name__ == "__main__":
    ed = EventDocuments('192.168.1.173', 27017,"beta");
    print ed.getEventsWithType("testACCOUNT_events","PlayerMoveEvent",1479205639,1).toJson()