from flask.ext.pymongo import PyMongo
import json

class Work:
    def __init__(self):
        self.MemberId = 0
        self.FullText = {}

    def find_by_id(self, member_id, mongoCollection):
        result = mongoCollection.find_one({"id": member_id}, {"_id":False})

        if result is not None:
            return json.dumps(result)
        else:
            return None

    def add_to_cache(self, member_id, dataDict, mongoCollection):
        self.MemberId = member_id
        self.FullText = dataDict

        mongoCollection.insert_one({"id":self.MemberId, \
        "FullText":self.FullText})

    def update(self, member_id, dataDict, mongoCollection):
        self.MemberId = member_id
        self.FullText = dataDict

        mongoCollection.find_one_and_update({"id":str(self.MemberId)},
        {"$set":{"FullText":self.FullText}},
        {"upsert":True, "returnNewDocument":True})
