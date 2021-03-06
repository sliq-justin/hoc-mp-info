import sys
from os import environ
import urllib
import json

import xmltodict

import Member

# basic Flask
from flask import Flask

# persistence
from flask.ext.pymongo import PyMongo
from pymongo import MongoClient

# general app stuff
app = Flask(__name__)
app.debug = False

# config and settings
# use remote db or local?
USE_REMOTE_DB = True
DB_URL = ""
DB_NAME = ""

if (environ.has_key("MONGO_DBNAME") and environ.has_key("MONGO_DBURL")):
    # probably running on Heroku
    DB_NAME = environ["MONGO_DBNAME"]
    DB_URL = environ["MONGO_DBURL"]
else:
    # running locally
    import config
    from config import DevelopmentConfig, ProductionConfig

    if USE_REMOTE_DB is True:
        app.config.from_object(config.ProductionConfig)
        DB_NAME = ProductionConfig.MONGO_DBNAME
        DB_URL = ProductionConfig.MONGO_DBURL
    else:
        app.config.from_object(config.DevelopmentConfig)
        DB_NAME = DevelopmentConfig.MONGO_DBNAME
        DB_URL = DevelopmentConfig.MONGO_DBURL

# db 
client = MongoClient(DB_URL) # pass mongourl into constructor
db = client[DB_NAME]         # pass db name into client
members = db.members                                # which model to use 

# routes - general
@app.route("/")
def hello_world():
    return "Hello, World!"

# routes - member
# db = ourcommons
# collection = members (may have bills, motions, etc. some day)
@app.route("/members/<member_id>")
def get_member_information(member_id):
    # validate member_id:
    if len(member_id) < 2:
        return json.dumps({"message":"invalid member number"}) # should be "400 - Bad Request"

    # 1 check db for requested item
    # 1.1 if it exists:
    #   1.1.1 return it
    # 1.2 if it does not exist:
    #   1.2.1 fetch from remote
    #   1.2.2 store in db
    #   1.2.3 return it

    # 1.
    member_json = Member.Member().find_by_id(member_id, members)

    # 1.1 item found
    # 1.1.1 returning it
    if member_json is not None:
        print "member %s info found - returning as JSON" % member_id
        return member_json

    # 1.2 item not found
    print "member %s info not found - look up and save" % member_id

    # 1.2.1 fetching from remote
    link = "http://www.ourcommons.ca/Parliamentarians/en/members/%s/ExportRoles?current=True&output=XML" % member_id
    member_dict = xmltodict.parse(urllib.urlopen(link).read())

    # 1.2.2 storing in db
    member_json = Member.Member()
    member_json.add_to_cache(member_id, member_dict, members)

    # 1.2.2.1 sanitize db:
    # remove all that xml nonsense
    sanitize_db()

    # 1.2.3 return new member data
    return Member.Member().find_by_id(member_id, members)

@app.route("/members/<member_id>/update")
def update_cached_member_data(member_id):
    # validate member_id:
    if len(member_id) < 2:
        return json.dumps({"message":"invalid member number"}) # should be "400 - Bad Request"

    # fetch data from remote
    link = "http://www.ourcommons.ca/Parliamentarians/en/members/%s/ExportRoles?current=True&output=XML" % member_id
    member_dict = xmltodict.parse(urllib.urlopen(link).read())

    # store in db
    member_json = Member.Member()
    member_json.update(member_id, member_dict, members)

    # sanitize db
    sanitize_db()

    # return new member data
    return Member.Member().find_by_id(member_id, members)

@app.route("/sanitize")
def sanitize_db():
    members.update_many({"MemberOfParliamentRole.@xmlns:xsd":"http://www.w3.org/2001/XMLSchema"}, {"$unset":{"MemberOfParliamentRole.@xmlns:xsd":"http://www.w3.org/2001/XMLSchema"}})
    members.update_many({"MemberOfParliamentRole.@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"}, {"$unset":{"MemberOfParliamentRole.@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"}})

    members.update_many({"CaucusMemberRoles.@xmlns:xsd":"http://www.w3.org/2001/XMLSchema"}, {"$unset":{"CaucusMemberRoles.@xmlns:xsd":"http://www.w3.org/2001/XMLSchema"}})
    members.update_many({"CaucusMemberRoles.@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"}, {"$unset":{"CaucusMemberRoles.@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"}})

    members.update_many({"ParliamentaryPositionRoles.@xmlns:xsd":"http://www.w3.org/2001/XMLSchema"}, {"$unset":{"ParliamentaryPositionRoles.@xmlns:xsd":"http://www.w3.org/2001/XMLSchema"}})
    members.update_many({"ParliamentaryPositionRoles.@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"}, {"$unset":{"ParliamentaryPositionRoles.@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"}})

    members.update_many({"CommitteeMemberRoles.@xmlns:xsd":"http://www.w3.org/2001/XMLSchema"}, {"$unset":{"CommitteeMemberRoles.@xmlns:xsd":"http://www.w3.org/2001/XMLSchema"}})
    members.update_many({"CommitteeMemberRoles.@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"}, {"$unset":{"CommitteeMemberRoles.@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"}})

    members.update_many({"ProfileParliamentaryAssociationsandInterparliamentaryGroupRoles.@xmlns:xsd":"http://www.w3.org/2001/XMLSchema"}, {"$unset":{"ProfileParliamentaryAssociationsandInterparliamentaryGroupRoles.@xmlns:xsd":"http://www.w3.org/2001/XMLSchema"}})
    members.update_many({"ProfileParliamentaryAssociationsandInterparliamentaryGroupRoles.@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"}, {"$unset":{"ProfileParliamentaryAssociationsandInterparliamentaryGroupRoles.@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"}})
    
    return json.dumps({"message":"db cleanup complete"})

# startup
if __name__ == "__main__":
    port = int(environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
