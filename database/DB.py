import time
from pymongo import MongoClient
from bson.json_util import dumps

class DB:
    def __init__(self,host,port,db):
        client = MongoClient(host,int(port))
        self.db = client[db]
        self.json_docs = []
        self.querry = None;
        self.collection = None;
        self.sort = {"field":"_id","direction":1}
        self.limit = 0

    def clean(self, cursor):
        self.json_docs = []
        for doc in cursor:
            if "meta" in doc:
                doc["time"] = doc["meta"]["time"]
                del doc["meta"]
                del doc["_id"]
            self.json_docs.append(doc)

    def gettimeboundaries(self, t=0,delta=0):
        self.time_upper = t


        if self.time_upper == 0 :
            self.time_upper = int(time.time())

        self.time_lower = (self.time_upper - delta)


    def refine(self, list):
        for doc in self.json_docs:
            for k in doc.keys():
                if k not in list:
                    del doc[k]
        return self


    def filter(self, field, list, exclude=False):
        if exclude:
            self.querry[field] = {"$nin": list }
        else:
            self.querry[field] = {"$in": list }

        return self


    def set_sort(self,field="_id", direction=1):
        self.sort["field"] = field
        self.sort["direction"] = direction

    def set_limit(self,limit=0):
        self.limit = limit;

    def count(self):
        return len(self.json_docs)
    def execute(self):
        if self.querry is not None and self.collection is not None:
            self.clean(
                self.db[self.collection].find(self.querry).sort(self.sort["field"],self.sort["direction"]).limit(self.limit)
            )
        else:
            print "ERROR!!!!!!"
        return self


    def getResult(self):
        return self.json_docs

    def toJson(self):
        return dumps(self.json_docs)