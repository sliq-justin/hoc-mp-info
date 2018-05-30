import sys
from os import environ
import urllib
import json

import xmltodict

import Member, Role, Work

# basic Flask
from flask import Flask

# persistence
from flask.ext.pymongo import PyMongo
from pymongo import MongoClient

# general app stuff
app = Flask(__name__)
app.debug = True

# config and settings
# use remote db or local?
USE_REMOTE_DB = False
DB_URL = ""
DB_NAME = ""

if environ.has_key("IS_LOCAL"):
    print "local?"
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
else:
    print "remote?"
    # i.e. (environ.has_key("MONGO_DBNAME") and environ.has_key("MONGO_DBURL")) == True
    # probably running on Heroku
    DB_NAME = environ["MONGO_DBNAME"]
    DB_URL = environ["MONGO_DBURL"]

# db 
client = MongoClient(DB_URL)    # pass mongourl into constructor
db = client[DB_NAME]            # pass db name into client
members_collection = db.members            # which model to use 
work_collection = db.work
roles_collection = db.roles

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
    member_json = Member.Member().find_by_member_id(member_id, members_collection)

    # 1.1 item found
    # 1.1.1 returning it
    if member_json is not None:
        print "member %s info found - returning as JSON" % member_id
        return member_json

    # 1.2 item not found
    print "member %s info not found - look up and save" % member_id

    print "finished string parsing"

    # 1.2.2 storing in db
    member_json = Member.Member()
    member_json.add_to_cache(member_id, members_collection)

    # 1.2.2.1 sanitize db:
    # remove all that xml nonsense
    # sanitize_db_members()

    # 1.2.3 return new member data
    # return Member.Member().find_by_member_id(member_id, members_collection)
    return json.dumps({"message":"member info not implemented"})

# routes - member - roles
# db = ourcommons
# collection = roles

@app.route("/members/<member_id>/roles")
def get_member_roles(member_id):
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
    roles_json = Role.Role().find_by_member_id(member_id, roles_collection)

    # 1.1 item found
    # 1.1.1 returning it
    if roles_json is not None:
        print "member %s roles found - returning as JSON" % member_id
        return roles_json

    # 1.2 item not found
    print "member %s roles not found - look up and save" % member_id

    # 1.2.1 fetching from remote
    link = "http://www.ourcommons.ca/Parliamentarians/en/members/%s/ExportRoles?current=True&output=XML" % member_id
    roles_dict = xmltodict.parse(urllib.urlopen(link).read())

    # 1.2.2 storing in db
    roles_json = Role.Role()
    roles_json.add_to_cache(member_id, roles_dict, roles_collection)

    # 1.2.2.1 sanitize db:
    # remove all that xml nonsense
    sanitize_db_roles()

    # 1.2.3 return new member data
    return Role.Role().find_by_member_id(member_id, roles_collection)

@app.route("/members/<member_id>/update-roles")
def update_cached_member_data(member_id):
    # validate member_id:
    if len(member_id) < 2:
        return json.dumps({"message":"invalid member number"}) # should be "400 - Bad Request"

    # fetch data from remote
    link = "http://www.ourcommons.ca/Parliamentarians/en/members/%s/ExportRoles?current=True&output=XML" % member_id
    roles_dict = xmltodict.parse(urllib.urlopen(link).read())

    # store in db
    roles_json = Role.Role()
    roles_json.update(member_id, roles_dict, roles_collection)

    # sanitize db
    sanitize_db_roles()

    # return new member data
    return Role.Role().find_by_member_id(member_id, roles_collection)

# routes - member - work
# db = ourcommons
# collection = work

@app.route("/members/<member_id>/work")
def get_member_work(member_id):
    # return "work for member %s" % member_id
    # validate member_id:
    if len(member_id) < 2:
        return json.dumps({"message":"invalid member number"})

    member_work = Work.Work().find_by_id(member_id, work_collection)

    # 1.1 item found
    # 1.1.1 returning it
    if member_work is not None:
        print "member %s work found - returning as JSON" % member_id
        return member_work

    print "member %s work not found - look up and save" % member_id

    # fetch data from remote
    link = "http://www.ourcommons.ca/Parliamentarians/en/publicationsearch?per=%s&pubType=37&xml=1" % member_id
    work_dict = xmltodict.parse(urllib.urlopen(link).read())

    member_work = Work.Work()
    member_work.add_to_cache(member_id, work_dict, work_collection)

    return json.dumps(work_dict)

# housecleaning
@app.route("/sanitize")
def sanitize_db():
    sanitize_db_members()
    sanitize_db_roles()
    sanitize_db_work()

@app.route("/members/sanitize")
def sanitize_db_members():
    # sanitize members collection
    # ...
    # return json.dumps({"message":"db cleanup not implemented - members"})
    pass

@app.route("/members/roles/sanitize")
def sanitize_db_roles():
# sanitize roles collection
    roles_collection.update_many({"MemberOfParliamentRole.@xmlns:xsd":"http://www.w3.org/2001/XMLSchema"}, {"$unset":{"MemberOfParliamentRole.@xmlns:xsd":"http://www.w3.org/2001/XMLSchema"}})
    roles_collection.update_many({"MemberOfParliamentRole.@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"}, {"$unset":{"MemberOfParliamentRole.@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"}})

    roles_collection.update_many({"CaucusMemberRoles.@xmlns:xsd":"http://www.w3.org/2001/XMLSchema"}, {"$unset":{"CaucusMemberRoles.@xmlns:xsd":"http://www.w3.org/2001/XMLSchema"}})
    roles_collection.update_many({"CaucusMemberRoles.@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"}, {"$unset":{"CaucusMemberRoles.@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"}})

    roles_collection.update_many({"ParliamentaryPositionRoles.@xmlns:xsd":"http://www.w3.org/2001/XMLSchema"}, {"$unset":{"ParliamentaryPositionRoles.@xmlns:xsd":"http://www.w3.org/2001/XMLSchema"}})
    roles_collection.update_many({"ParliamentaryPositionRoles.@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"}, {"$unset":{"ParliamentaryPositionRoles.@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"}})

    roles_collection.update_many({"CommitteeMemberRoles.@xmlns:xsd":"http://www.w3.org/2001/XMLSchema"}, {"$unset":{"CommitteeMemberRoles.@xmlns:xsd":"http://www.w3.org/2001/XMLSchema"}})
    roles_collection.update_many({"CommitteeMemberRoles.@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"}, {"$unset":{"CommitteeMemberRoles.@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"}})

    roles_collection.update_many({"ProfileParliamentaryAssociationsandInterparliamentaryGroupRoles.@xmlns:xsd":"http://www.w3.org/2001/XMLSchema"}, {"$unset":{"ProfileParliamentaryAssociationsandInterparliamentaryGroupRoles.@xmlns:xsd":"http://www.w3.org/2001/XMLSchema"}})
    roles_collection.update_many({"ProfileParliamentaryAssociationsandInterparliamentaryGroupRoles.@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"}, {"$unset":{"ProfileParliamentaryAssociationsandInterparliamentaryGroupRoles.@xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"}})
    
    return json.dumps({"message":"db cleanup complete - roles"})

@app.route("/members/work/sanitize")
def sanitize_db_work():
    # sanitize work collection
    # ...
    return json.dumps({"message":"db cleanup not implemented - work"})

# startup
if __name__ == "__main__":
    port = int(environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
