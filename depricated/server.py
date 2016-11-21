from bson import ObjectId
from pymongo import MongoClient
client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.beta
cursor = db["testserver_worlds"].find()
for document in cursor:
    document["loaded"] = []
    for id in document["chunks"]:
        #print(id)
        chunks = db["testserver_chunks"].find_one({"_id":ObjectId(id)})
        document["loaded"].append(chunks)
        id = chunks
        #print(id)

    print("\n\n")
    print(document)